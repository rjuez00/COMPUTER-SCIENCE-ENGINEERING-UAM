#include "pool_thread.h"
#include "http.h"
#include "picohttpparser.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h> 
#include <errno.h>
#include <pthread.h>
#include <semaphore.h>
#include "socket.h"
#include "log.h"


#define BUFFER_SIZE 1024


int pool_handler(int num_threads, Servidor *server) {

    if (num_threads <= 0) return -1;

    /* Creamos los threads asignandoles una tarea */
    for(int i = 0; i < num_threads; i++) {
        if (pthread_create(&server->threads[i], NULL, child_function, (void *)server) != 0) {
            /* En caso de error, matamos los threads */
            if (kill_threads(server) == -1) {
                log_error_msg("Error en Kill_threads");
                return -1;
            }
            log_error("pthread_create", errno);
            return -1;
        }
        server->num_threads++;
    }

    return 0;
}


int kill_threads(Servidor *server) {

    if (server == NULL) return -1;

    /* Matamos los threads */
    for(int i = 0; i < (server->num_threads); i++) {
        /* Acabamos la ejecución de un hilo */
        if (pthread_cancel(server->threads[i]) != 0) {
            log_error("pthread_cancel", errno);
            return -1;
        }

        /* Esperamos al hilo para cerrarlo correctamente */
        if (pthread_join(server->threads[i], NULL) != 0) {
            log_error("pthread_join", errno);
            return -1;
        }
    }
    return 0;
}


void* child_function(void *server_arg) {
    int cliente = 0, valread;
	char *buffer = NULL;
    Servidor* server = (Servidor *) server_arg;
    int number_working = -1;
    if (server_arg == NULL) return NULL;

    /* No permitimos que se cancele el hilo */
    if (pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, NULL) != 0) {
        log_error("pthread_setcancelstate", errno);
        return NULL;
    }

    /* Loop infinito para aceptar mensajes en el socket */
    while(1) {
        /* Permitimos que se cancele el hilo */
        if (pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL) != 0) {
            log_error("pthread_setcancelstate", errno);
            return NULL;
        }
        
        /* Accept actua como mutex */
        if ((cliente = accept_socket(server->server_fd)) == -1) {
            return NULL;
        } 

        /* No permitimos que se cancele el hilo */
        if (pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, NULL) != 0) {
            log_error("pthread_setcancelstate", errno);
        }
        
        /* Aumentamos el valor del semaforo para contar los threads que están trabajando */
        sem_post(server->sem);
        if (sem_getvalue(server->sem, &number_working) == -1) {
            log_error("sem_getvalue", errno);
        }
        log_msg_and_info_int("Hijos disponibles", server->num_threads - number_working);
        log_msg_and_info_int("Hijos trabajando", number_working);
        fflush(stdout);

        /* Establecemos un timeout */
        struct timeval tv;
        tv.tv_sec = 30;  /* 120 Secs Timeout */
        tv.tv_usec = 0;
        if (setsockopt(cliente, SOL_SOCKET, SO_RCVTIMEO, (struct timeval *)&tv, sizeof(struct timeval)) == -1) {
            log_error("setsockopt: %s", errno);
            return NULL;
        }

        /* Servidor lee el mensaje del cliente */
        while(1){
            int already_read = 0;

            /* Do while para leer el socket mientras llenamos un buffer */
            do {
                /* Buffer donde se lee el socket, se realoca dependiendo de como aumente el tamaño */
                buffer = (char*)realloc(buffer, ((already_read+BUFFER_SIZE+1) * sizeof(char))); 
                if (buffer == NULL) {
                    log_error("realloc: %s", errno);
                    return NULL;
                }

                /* Leyendo el socket */
                valread = recv(cliente, buffer+already_read, BUFFER_SIZE, 0);
                
                /* Exito en la lectura */
                if (valread > 0) {
                    already_read += valread;

                    /* Si lo que se ha leido es diferente al tamaño establecido del buffer,
                    significa que ya no hay más que leer */
                    if(valread != BUFFER_SIZE){
                        break;
                    }
                }
                /* Error en la lectura */
                else if (valread < 0) { 
                    if (errno == 11) break;
                    log_error("recv", errno);
                    if(buffer) free(buffer);
                    return NULL;
                }

            } while(valread == BUFFER_SIZE);
            buffer[already_read]='\0';

            /* Timeout con el cliente */
            if(valread < 0) {
                log_error_msg("se ha cerrado la conexion por timeout");
                fflush(stdout);
                break;
            }
            /* En caso de que se cierre el socket, la función devuelve 0 */
            else if (valread == 0){
                log_error_msg("conexion terminada\n");
                break;
            }
            log_msg("peticion recibida\n");
            
            /* Parseamos la request y respondemos si es necesario */
            int is_connection_closed = parse_request(cliente, buffer, server->server_signature, server->server_root);

            if( is_connection_closed == -1) {
                log_error_msg("Error procesando peticion\n");
            }
            else if ( is_connection_closed == -2 ){
                free(buffer);
                buffer = NULL;
                break;
            }
            free(buffer);
            buffer = NULL;
        }
        /* Cerramos el descriptor abierto con el cliente */
        close(cliente);

        /* Actualizamos el número disponible de hijos trabajando */
        sem_wait(server->sem);
        if (sem_getvalue(server->sem, &number_working) == -1) {
            log_error("No se ha podido obtener el valor del semáforo. sem_getvalue: %s", errno);
        }
        log_msg_and_info_int("Hijos disponibles", server->num_threads - number_working);
        log_msg_and_info_int("Hijos trabajando", number_working);

        /* Liberamos el buffer */
        if (buffer != NULL) {
            free(buffer);
            buffer = NULL;
        }

    }

    /* Liberamos el buffer */
    if (buffer != NULL) {
        free(buffer);
        buffer = NULL;
    }
    return NULL;
}