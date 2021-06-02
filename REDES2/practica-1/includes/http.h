/**
 * @file http.h
 * @author Rodrigo Juez
 *         Kevin de la Coba
 * @brief Fichero que define los prototipos de las funciones http
 * @version 1.0
 * @date 2021-02-21
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#ifndef HTTP_H
#define HTTP_H

/**
 * @brief Función que parsea una petición 
 * 
 * @param request Request enviada por el cliente
 * @param method Variable pasada por referencia para guardar el método de la petición
 * @param path Variable pasada por referencia para guardar el path del recurso que se pide
 * @param num_headers Variable pasada por referencia donde se guardan el numero de headers recibidos
 * @param error Variable pasada por referencia donde se va a guardar el código de error
 *              -1 Error
 *              -2 La petición esta incompleta
 * @return int Código de error
 */
int parse_request(int cliente, char *request, char* server_signature, char* server_root) ;

/**
 * @brief Función que crea una respuesta HTTP
 * 
 * @param code Codigo de la respuesta
 * @param cabeceras Cabeceras a incluir
 * @param htmlcontent htmlcontent de las respuestas
 * @param server_signature Signature del servidor
 * @param server_root Raiz del servidor
 * @param method Método HTTP usado
 * @param path Path al archivo pedido
 * @param arguments Argumentos
 * @return char* Respuesta
 */
int http_response(int cliente, int code, char* server_signature, char* server_root, int method, char *path, char* arguments);
#endif