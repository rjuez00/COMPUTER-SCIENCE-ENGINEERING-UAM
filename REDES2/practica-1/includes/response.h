/**
 * @file response.h
 * @author Rodrigo Juez
 *         Kevin de la Coba
 * @brief Archivo donde se definen los prototipos de las funciones
 * utilizadas para construir respuestas
 * 
 * @version 1.0
 * @date 2021-03-25
 * 
 * @copyright Copyright (c) 2021
 * 
 */

#ifndef RESPONSE_H
#define RESPONSE_H
/**
 * @brief Función privada que construye cabeceras para una respuesta
 * 
 * @param server Servidor
 * @param last_modified Fecha de la ultima modificación
 * @param content_length Longitud del contenido
 * @param content_type Tipo del contenido
 * @param allow Cabecera allow
 * @return char* Cabeceras en una string
 */
char *build_cabecera(char *server, char *last_modified, char *content_length, char *content_type, char *allow);


/**
 * @brief Función que en base a un codigo de error rellena variables
 * 
 * @param code Código de error
 * @param codestring String que contendra el mensaje correspondiente
 * @param path Path del archivo
 * @param arguments Argumentos de la peticion para un script
 * @param type Variable pasada por referencia donde se guarda el tipo
 * @param html_content Variable pasada por referencia que contendra el objeto
 * @param content_lenth Variable pasada por referencia que contendra la longitud del objeto
 * @param lastmodified_in Variable pasada por referencia para guardar una string con la fecha de modificación del objeto
 * @return int 0 OK, -1 ERR
 */
int translate_code(int code, char* codestring, char *path, char *arguments, char **type, char** html_content, long int* content_lenth, char **lastmodified_in, short method);


/**
 * @brief Función que guarda en un argumento la string con 
 * la ultima modificación de un archivo
 * 
 * @param path Path del archivo
 * @param date_now Fecha del archivo
 * @return int 0 OK, -1 ERR
 */
int getModifiedTime(char *path, char *date_now);


/**
 * @brief Función que comprueba si lo que hay que ejecutar es un script 
 * 
 * @param request Petición a comprobar
 * @return int 1 py, 2 php, 0 False
 */
int isScript(char *request);

/**
 * @brief Función privada para comprobar el formato de 
 * el objeto que se pide en la petición
 * 
 * @param path Path del objeto
 * @param isScript Variable pasada por referencia para comprobar
 * el objeto que se pide es un script.
 * 0 no es script, 1 Python, 2 php
 * @param isRoot Variable pasada por referencia para comprobar 
 * si el objeto que se nos pide es la página principal
 * @return char* Formato del objeto a responder
 */
char *return_format(char* path, char* isScript, char *isRoot);


/**
 * @brief Función privada para leer una página guardada 
 * en nuestro servidor
 * 
 * @param filename Nombre del archivo de la página web
 * @return char* String conteniendo la página web
 */
char *read_page(char *filename);
#endif
