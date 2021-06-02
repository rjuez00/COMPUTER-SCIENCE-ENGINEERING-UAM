/**
 * @file servidor.c
 * @author Kevin de la Coba
 *         Rodrigo Juez
 * @brief Fichero donde se define el comportamiento del Servidor
 * @version 1.0
 * @date 2021-02-18
 * 
 * @copyright Copyright (c) 2021
 * 
 */

#include <stdlib.h>
#include <confuse.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h> 
#include <errno.h>
#include <pthread.h> 
#include "socket.h" 
#include "servidor.h"
#include "pool_thread.h"
#include "log.h"

#define TAM_MAX_STRING 100
#define SEM_NAME "sem_server"

/**
 * @brief Función que obtiene la configuración del servidor
 * 
 * @param filename Archivo donde se encuentra la configuracion
 * @param server_root Variable pasada por referencia para guardar la string del server root
 * @param max_clients Variable pasada por referencia para guardar el número máximo de clientes
 * @param listen_port Variable pasada por referencia para guardar el puerto de escucha del servidor
 * @param server_signature Variable pasada por referencia para guardar la firma del servidor
 * @return int 0 OK, -1 ERROR
 */
int parse_configuration(char* filename, char** server_root, long int* max_clients, long int* listen_port, char** server_signature, char* daemon);


void do_daemon(void){
    pid_t pid;
    pid = fork();
    
    if (pid < 0) exit(EXIT_FAILURE);
    if (pid > 0) exit(EXIT_SUCCESS);
    
    log_ini();

    if(setsid() < 0){
        log_error_msg("Error creating a new SID for the child process.");
        exit(EXIT_FAILURE);
    }

    /*if((chdir("/")) < 0){
        log_error_msg("Error changing the current working directory = \"/\"");
        exit(EXIT_FAILURE);
    }*/
    
    log_msg("Closing standard file descriptors");
    close(STDIN_FILENO); close(STDOUT_FILENO); close(STDERR_FILENO);
}


Servidor *server_init(char* filename) {
    int server_fd = 0;
    Servidor *server = NULL;
    char *server_root = NULL, *server_signature = NULL, daemon = 0;
    long int max_clients = -1, listen_port= -1;

    /* Obtenemos la configuración del server */
    if(parse_configuration(filename, &server_root, &max_clients, &listen_port, &server_signature, &daemon) == -1) {
        log_error("parse_configuration", errno);
        return NULL;
    }

    if(daemon == 1){
        printf("demonizando\n");
        do_daemon();
    }

    if (listen_port < 0) {
        log_error_msg("port not valid");
        return NULL;
    }
    
    /* Reservamos memoria para el servidor */
    server = (Servidor*)malloc(sizeof(Servidor));
    if (server == NULL) {
        log_error("malloc", errno);
        return NULL;
    }
    /* Asignamos valores */
    server->num_threads = 0;

    /* Reservamos memoria para los pids */
    server->threads = (pthread_t*)malloc(max_clients*sizeof(pthread_t));
    if (server->threads == NULL) {
        log_error("malloc", errno);
        free(server);
        server = NULL;
        return NULL;
    }

    /* Inicializamos el socket del server */
    if ((server_fd = create_server_socket(listen_port, max_clients*2)) == -1) {
        log_error_msg("Error en create_server_socket");
        server_free(server);
        return NULL;
    }
    server->server_fd = server_fd;

    /* Inicializamos el semáforo del servidor */
    if ((server->sem = sem_open(SEM_NAME, O_CREAT | O_EXCL, S_IRUSR | S_IWUSR, 0)) == SEM_FAILED) {
        log_error("sem_open", errno);
		exit(EXIT_FAILURE);
	}
	sem_unlink(SEM_NAME);

    if (pool_handler(max_clients, server) == -1) {
        log_error_msg("Error en Pool handler");
        server_free(server);
        return NULL;
    }
    server->server_root = server_root;
    server->server_signature = server_signature;
    return server;
}


int server_free(Servidor* server){
    if (server->threads != NULL) {
        free(server->threads);
        server->threads = NULL;
    }

    if (server->sem != NULL) sem_close(server->sem);

    free(server->server_root);
    free(server->server_signature);

    if (server != NULL) {
        free(server);
        server = NULL;
    }    
    return 0;
} 


int parse_configuration(char* filename, char** server_root, long int* max_clients, long int* listen_port, char** server_signature, char* daemon){
    char* server_root_temp = NULL, *server_signature_temp = NULL;
    static cfg_bool_t daemon_temp = cfg_false;

    /* Estableciendo los campos a parsear */
    cfg_opt_t opts[] = {
        CFG_SIMPLE_STR("server_root", &server_root_temp),
        CFG_SIMPLE_STR("server_signature", &server_signature_temp),
        CFG_SIMPLE_INT("max_clients", max_clients),
        CFG_SIMPLE_INT("listen_port", listen_port),
        CFG_SIMPLE_BOOL("daemon", &daemon_temp),
        CFG_END()
    };
    cfg_t *cfg;

    /* set default value for the server option */
    cfg = cfg_init(opts, 0);
    if(cfg == NULL){
        log_error("cfg_init", errno);
        return -1;
    }

    /* Parseando */
    if (cfg_parse(cfg, filename) == -1){
        log_error("cfg_parse", errno);
        return -1;
    }
    
    /* Reservamos memoria para la ruta del servidor */
    *server_root = (char*)malloc((strlen(server_root_temp)+1) * sizeof(char));
    if (server_root == NULL) {
        log_error("malloc", errno);
        return -1;
    }
    
    /* Reservamos memoria para el nombre del servidor */
    *server_signature = (char*)malloc((strlen(server_signature_temp)+1) * sizeof(char));
    if(server_signature == NULL){
        log_error("malloc", errno);
        return -1;
    }

    /* Copiamos el nombre y la ruta del servidor */
    strcpy (*server_signature, server_signature_temp);
    strcpy (*server_root, server_root_temp);
    *daemon = daemon_temp ? 1 : 0;

    log_msg("Parsed configuration file:\n");
    log_msg_and_info("\t server_root:", *server_root);
    log_msg_and_info_int("\t max_clients", *max_clients);
    log_msg_and_info_int("\t listen_port", *listen_port);
    log_msg_and_info("\t server_signature", *server_signature);
    log_msg_and_info_int("\t daemon", *daemon);
    
    /* Liberamos recursos de las variables temporales */
    free(server_root_temp);
    free(server_signature_temp);
    cfg_free(cfg);
    return 0;
}