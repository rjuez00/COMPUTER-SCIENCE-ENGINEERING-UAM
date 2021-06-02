/**
 * @file cgi.h
 * @author Rodrigo Juez
 *         Kevin de la Coba
 * @brief Archivo donde se definen los prototipos de las funciones
 * del CGI
 * @version 1.0
 * @date 2021-03-10
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#ifndef CGI_H
#define CGI_H

/**
 * @brief Función que llama a un ejecutable y ejecuta un script
 * 
 * @param filename Ruta al archivo
 * @param arguments Argumentos a pasar por STDIN
 * @param pyORphp Flag para saber si es python (1) or php (2)
 * @param htmlcontent Variable pasada por referencia para guardar el output
 * @return int -1 Error, 1 OK
 */
int call_cgi(char *filename, char* arguments, char pyORphp, char **htmlcontent);

#endif