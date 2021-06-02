/**
 * @file main.c
 * @author Kevin de la Coba
 *         Rodrigo Juez
 * @brief Archivo donde se produce la ejecución del programa
 * @version 1.0
 * @date 2021-02-21
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include "log.h"
#include "servidor.h"
#include <signal.h>
#include <stdlib.h>
#include <syslog.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#define PORT 8080 

/**
 * @brief Manejador vacio para cuando el hilo padre reciba
 * una señal en concreto
 * 
 * @param sig Señal
 */
void manejador_vacio(int sig) {}

int main(int argc, char const *argv[]) 
{     
    sigset_t new_mask, old_mask;
    struct sigaction act;
    
    /* Los hijos ignoran todas las señales */
    if (sigfillset(&new_mask) == -1) {
        log_error("sigfillset", errno);
        return -1;
    }

    /* Bloqueo de las señales SIGUSR1 y SIGUSR2 en el proceso. */
    if (pthread_sigmask(SIG_BLOCK, &new_mask, &old_mask) < 0) {
        log_error("pthread_sigmask", errno);
        exit(EXIT_FAILURE);
    }

    /* Creando una mascara para el hilo padre, añadiendole a esta un manejador */
    if (sigfillset(&(act.sa_mask)) == -1) {
        log_error("sigfillset", errno);
        return -1;
    }

    /* El padre ignora todas las señales excepto sigint */
    if (sigdelset(&(act.sa_mask), SIGINT) == -1) {
        log_error("sigdelset", errno);
        return -1;
    }

    act.sa_flags = 0;
    act.sa_handler = manejador_vacio;
    if (sigaction(SIGINT, &act, NULL) < 0) {
        log_error("sigaction", errno);
        exit(EXIT_FAILURE);
    }

    /* Creamos el servidor */
    Servidor *server = server_init("server.conf");
    if (server == NULL) return -1;

    /* Suspendemos el hilo principal hasta que este reciba una señal concreta */
    sigsuspend(&old_mask);

    /* Matamos a los hilos y liberamos memoria */
    if (kill_threads(server) == -1){
        log_error_msg("Los hilos no se han cerrado correctamente");
    }
    server_free(server);

	return 0; 
} 
