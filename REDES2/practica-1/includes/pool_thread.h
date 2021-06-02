/**
 * @file socket.h
 * @author Rodrigo Juez
 *         Kevin de la Coba
 * @brief Fichero donde se manejan el pool de threads
 * @version 1.0
 * @date 2021-02-17
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#ifndef POOL_THREAD_H
#define POOL_THREAD_H

#include <string.h>
#include "servidor.h"

/**
 * @brief Función que crea los hilos
 * 
 * @param server_fd Descriptor a cerrar
 * @return int  0 OK, -1 ERROR 
 */
int pool_handler(int num_threads, Servidor *server);

/**
 * @brief Función que cierra los hilos
 * 
 * @param server_fd Descriptor a cerrar
 * @return int  0 OK, -1 ERROR 
 */
int kill_threads(Servidor *server);

/**
 * @brief Función que ejecuta el hilo hijo
 * 
 * @param server_fd Struct con la informacion del servidor
 * @return NULL
 */
void* child_function(void *server_arg);



#endif