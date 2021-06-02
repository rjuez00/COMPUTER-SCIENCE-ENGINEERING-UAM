/**
 * @file socket.c
 * @author Rodrigo Juez
 *         Kevin de la Coba
 * @brief Archivo donde se maneja la librería socket.h, aquí
 * se crean y cierran los sockets del servidor y de los clientes.
 * @version 1.0
 * @date 2021-02-17
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h> 
#include <errno.h>
#include "socket.h"
#include "log.h"

int create_server_socket(int puerto, int tam_cola) {
    int server_fd; 
    int opt = 1; 
    
    if (puerto < 0) return -1;

    struct sockaddr_in address; 
    address.sin_family = AF_INET; 
    address.sin_addr.s_addr = INADDR_ANY; 
    address.sin_port = htons( puerto );
    
    /* Creando el socket */
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        log_error("socket", errno);
        return -1;
    }

    /* Configurando el socket */
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)) == -1) { 
        log_error("setsockopt", errno);
        return -1;
    }

    /* Hacemos bind, asignamos una direccion a un socket */
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) == -1) {
        log_error("bind", errno);
        return -1;
    }

    /* Escuchamos mediante el listen */
    if (listen(server_fd, tam_cola) == -1) {
        log_error("listen", errno);
        return -1;
    }

    return server_fd;
}

int accept_socket(int server_fd){
    int cliente = 0;

    /* Aceptamos una conexión */
    if ((cliente = accept(server_fd, NULL, NULL)) < 0)  { 
        log_error("accept", errno);
        return -1;
    } 

    return cliente; 
}

int close_socket(int server_fd) {

    if (server_fd < 0) return -1;

    /* Cerramos el descriptor */
    if (close(server_fd) != 0) {
        log_error("close", errno);
        return -1;
    }

    return 0;
}