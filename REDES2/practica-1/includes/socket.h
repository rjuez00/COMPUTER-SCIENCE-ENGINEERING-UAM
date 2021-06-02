/**
 * @file socket.h
 * @author Rodrigo Juez
 *         Kevin de la Coba
 * @brief Fichero donde se definen los prototipos de socket
 * @version 1.0
 * @date 2021-02-17
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#ifndef SOCKET_H
#define SOCKET_H

#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>

/**
 * @brief Función que crea un socket y le asigna una dirección determinada
 * El socket es del lado servidor
 * 
 * @param puerto Puerto en el que hay que establecer la conexión
 * @param tam_cola Tamaño de la cola en el socket
 * @return int File descriptor del socket, -1 ERROR
 */
int create_server_socket(int puerto, int tam_cola);

/**
 * @brief Función que acepta una conexión
 * 
 * @param server_fd Descriptor de fichero del socket del servidor
 * @return int 
 */
int accept_socket(int server_fd);

/**
 * @brief Función que cierra el descriptor de fichero del socket
 * 
 * @param server_fd Descriptor a cerrar
 * @return int  0 OK, -1 ERROR 
 */
int close_socket(int server_fd);


#endif