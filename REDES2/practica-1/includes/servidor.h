/**
 * @file servidor.h
 * @author Kevin de la Coba
 *         Rodrigo Juez
 * @brief Fichero que define los prototipos de las funciones del servidor
 * @version 0.1
 * @date 2021-02-18
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#ifndef SERVIDOR_H
#define SERVIDOR_H

#include <pthread.h> 
#include <semaphore.h>
#include <fcntl.h>        
#include <sys/stat.h>    


typedef struct Servidor {
    int server_fd;
    int num_threads;
    pthread_t *threads;
    sem_t *sem;
    char* server_root;
    char* server_signature;
} Servidor;

/**
 * @brief Función que inicia un servidor reservando memoria y creando un socket
 * 
 * @param filename Nombre del archivo
 * @return Servidor* Estructura del servidor
 */
Servidor* server_init(char* filename);

/**
 * @brief Función que maneja los hilos para su ejecución
 * 
 * @param num_threads Número de threads a crear
 * @param server Estructura con los datos del servidor
 * @return int 0 OK, -1 ERROR
 */
int pool_handler(int num_threads, Servidor *server);

/**
 * @brief Función que mata los threads
 * 
 * @param server Estructura doonde se encuentran los threads
 * @return int 0 OK, -1 ERROR
 */
int kill_threads(Servidor *server);

/**
 * @brief Función que libera memoria del servidor
 * 
 * @param server Servidor a liberar
 * @return int 0 OK, -1 ERR
 */
int server_free(Servidor* server);

/**
 * @brief Función para la ejecución de los hilos
 * 
 * @param server_fd Descriptor del fichero del socket
 * @return NULL
 */
void *child_function(void *server_fd);

#endif