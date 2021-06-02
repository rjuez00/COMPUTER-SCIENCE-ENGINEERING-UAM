#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <errno.h>
#include <syslog.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h> 
#include "log.h"

#define READ 0
#define WRITE 1
#define BUFFER_SIZE 1024

int call_cgi(char* filename, char* arguments, char pyORphp,char **htmlcontent){
    pid_t pid;
    int child_in[2];
    int child_out[2];
    int valread = 0;
    
    if(!filename){
        return -1;
    }

    /* Timeout para STDOUT */
    struct timeval tv;
    tv.tv_sec = 2;
    tv.tv_usec = 0;

    fd_set rfds;

    /* Inicializando valores */
    if (pipe(child_in) == -1) {
        log_error("pipe", errno);
        return -1;
    }
    if (pipe(child_out) == -1) {
        log_error("pipe", errno);
        return -1;
    }

    FD_ZERO(&rfds);
    FD_SET(child_out[READ], &rfds);

      
    /* Creamos el proceso hijo */
    pid = fork();
    if(pid != 0){
        /* Ejecución del padre */
        /* Cerramos el extremo de lectura de la tuberia para mandar
        al hijo los argumenntos */
        close(child_in[READ]);
        
        /* Cerramos el extremo de escritura de la tuberia para recibir
        el output */
        close(child_out[WRITE]);
        
        /* Si hay algo que escribir lo escribimos por la tubería */
        if(arguments != NULL)
            write(child_in[WRITE], arguments, strlen(arguments));
        close(child_in[WRITE]);

        valread = select(child_out[READ]+1, &rfds, NULL, NULL, &tv);
        if (valread != 1){
            log_error("fallo del select en cgi", errno);  
            (*htmlcontent) = (char*)realloc(*htmlcontent, (sizeof(char))); 
            (*htmlcontent)[0] = '\0';
            return -1;
            }



        /* Esperamos al hijo */
        wait(NULL);

        
        /* Leemos el contenido de la tubería que el hijo  */
        int already_read = 0;
        (*htmlcontent) = NULL;
        do {
            (*htmlcontent) = (char*)realloc(*htmlcontent, ((already_read+BUFFER_SIZE+1) * sizeof(char))); 
            if (*htmlcontent == NULL) {
                log_error("realloc", errno);    
                return -1;
            }

            valread = read(child_out[READ], (*htmlcontent)+already_read, BUFFER_SIZE);
            
            if (valread > 0) { // Exito al leer
                already_read += valread;

                if(valread != BUFFER_SIZE){
                    break;
                }
            }
            else if (valread < 0) { // ERROR al leer
                log_error("read", errno);    
                return -1;
            }

        } while(valread == BUFFER_SIZE);
        (*htmlcontent)[already_read] = '\0';

        return 0;
    }

    /* Ejecución del hijo */
    /* Cerrando extremos de tuberías para */
    close(child_out[READ]);
    close(child_in[WRITE]);

    /* Redirigiendo la tuberia a STDIN */
    dup2(child_in[READ], STDIN_FILENO);
    /* Redirigiendo la tuberia a STDOUT */
    dup2(child_out[WRITE], STDOUT_FILENO);

    /* Ejecutando el script */
    if (pyORphp == 1) return execlp("python3", "python3", filename /*arguments*/, (char *)NULL);
    if (pyORphp == 2) return execlp("php", "php", filename /*arguments*/, (char *)NULL);    
    return -1;
}