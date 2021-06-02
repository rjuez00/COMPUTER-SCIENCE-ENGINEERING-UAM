 
/**
 * @file http.c
 * @author Rodrigo Juez
 *         Kevin de la Coba
 * @brief Fichero donde se define el comportamiento del modulo
 * encargado interpretar las peticiones HTTP
 * @version 1.0
 * @date 2021-02-21
 * 
 * @copyright Copyright (c) 2021
 * 
 */

#include "http.h"
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include "picohttpparser.h"
#include "cgi.h"
#include "log.h"
#include "response.h"

#define MAX_HEADERS 100
#define MAX_PATH 200
#define MAX_METHOD 10
#define MAX_CSIZE_LEN 13
#define MAX_HTML_LEN 131072 #megabyte
#define MAX_CODESTRING 50



/**
 * @brief Función que comprueba si las cabeceras son correctas
 * 
 * @param headers Cabeceras a comprobar
 * @param num_headers Numero de cabeceras
 * @return int 0 OK, -1 ERROR
 */
int check_header(struct phr_header* headers, size_t num_headers);



int parse_request(int cliente, char *request, char* server_signature, char* server_root) {
    int pret, minor_version;
    size_t method_len, path_len, num_headers;
    char *method, *path, *args = NULL;
    struct phr_header headers[MAX_HEADERS];
    int method_int = -1;

    if (cliente <= 0 || request == NULL || server_signature == NULL || server_root == NULL) return -1;
    
    /* Numero máximo de cabeceras */
    num_headers = (sizeof(headers) / sizeof(headers[0]));

    /* Parseamos la request */
    pret = phr_parse_request(request, (ssize_t) strlen(request), (const char**)&method, &method_len,(const char**) &path, &path_len, &minor_version, headers, &num_headers, (size_t) 0);
    method[method_len] = '\0';
    path[path_len] = '\0';
    
    /* En caso de éxito */
    if (pret > 0) {

        /* La versión de HTTP no es soportada */
        if (minor_version != 1)
            return http_response(cliente, 505, server_signature, server_root, method_int, path, args);


        short cmp_head = strncmp("HEAD", method, 4);
        /* Comprobamos el método GET = 1 POST = 2 OPTIONS = 3 HEAD =4*/
        if (strncmp("OPTIONS", method, 7) == 0 || strncmp("/*", path, 2) == 0) {

            /* En caso de recibir options no hay parametros */
            method_int = 3;
        } else if( (strncmp("GET", method, 3) == 0) || cmp_head == 0){
            if (cmp_head == 0) method_int = 4;
            else method_int = 1;
            char *token = NULL;
            
            token = strtok(path, "?");
            token = strtok(NULL, "?");
            
            /* En caso de haber parametros en la petición las guardamos */
            if (token != NULL) {
                args = (char *)malloc((sizeof(char)*strlen(token))+1);
                if (args == NULL) {
                    log_error("malloc", errno);
                    return http_response(cliente, 500, server_signature, server_root, method_int, path, args);

                }
                strcpy(args, token);
                args[strlen(token)] = '\0';
            }
            
        } else if (strcmp("POST", method) == 0) {
            char* token = NULL; /*al parecer existen los métodos GET/POST que te pasan argumentos por la uri en un post*/
            token = strtok(path, "?");
            token = strtok(NULL, "?");
            args = NULL;
            if (token != NULL) {
                args = (char *)malloc((sizeof(char)*strlen(token))+1);
                if (args == NULL) {
                        log_error("malloc", errno);
                        return http_response(cliente, 500, server_signature, server_root, method_int, path, args);

                    }
                    strcpy(args, token);
                    args[strlen(token)] = '\0';
            }

            /* En caso de POST los parametros de la petición están en el objeto */
            method_int = 2;
            int len_arguments = 0;
            if (args != NULL) {
                len_arguments = strlen(args);
                args = (char*)realloc(args, sizeof(char) * (len_arguments + (strlen(request+pret)+3)));
                if (args == NULL) {
                    log_error("malloc", errno);
                    return http_response(cliente, 500, server_signature, server_root, method_int, path, args);
                }
                strcat(args, "&");
                strcat(args, request+pret);
            }
            else {
                args = (char*)malloc(sizeof(char) * (strlen(request+pret)+1));
                if (args == NULL) {
                    log_error("malloc", errno);
                    return http_response(cliente, 500, server_signature, server_root, method_int, path, args);
                }
                strcpy(args, request+pret);
            }
        } else {

            /* En caso de error al parsear respondemos al cliente con el error 405 */
            return http_response(cliente, 405, server_signature, server_root, method_int, path, args);
        }
        
        /* Comprobamos los headers */
        int check_header_temp = check_header(headers, num_headers);

        /* Enviamos una respuesta con un código dependiendo de los headers */
        if(check_header_temp == -1)  return http_response(cliente, 400, server_signature, server_root, method_int, path, args);

        /* Hay un connection close asi que sirvo la peticion y cierro la conexion (-2)*/
        else if ( check_header_temp == 1 ) { 
            /* En caso de que los headers estén bien respondemos */
            if( http_response(cliente, 200, server_signature, server_root, method_int, path, args) == -1) {
                log_error_msg("Error al responder.");
                return http_response(cliente, 500, server_signature, server_root, method_int, path, args);
            }

            /* La petición está incompleta */
            return -2;
        }

        /* Respondemos al cliente con 200 OK */
        return http_response(cliente, 200, server_signature, server_root, method_int, path, args);
    }
    else if (pret == -1) {
        /* Respondemos al cliente con 400 bad request en caso de error de parseo */
        return http_response(cliente, 400, server_signature, server_root, method_int, path, NULL);
    }
    else if (strlen(request) == sizeof(request)) {
        /* En caso de que el payload sea demasiado grande  */
        return http_response(cliente, 413, server_signature, server_root, method_int, path, NULL);
    }
    else if (pret == -2) {
        /* Petición incompleta */
        return -2;
    } else {
        /* Bad request */
        return http_response(cliente, 400, server_signature, server_root, method_int, path, NULL);
    }
    return 0;
}

int check_header(struct phr_header* headers, size_t num_headers) {
    /* Iteramos sobre los headers */
    for (int i = 0; i != num_headers; ++i) 
        /* Comprobamos el header host */
        if(strncmp(headers[i].name, "Host", headers[i].name_len) == 0) {
            for (int j = 0; j != num_headers; ++j) 
                /* Comprobamos los headers connection y close */
                if((strncmp(headers[j].name, "Connection", headers[j].name_len) == 0) && (strncmp(headers[j].value, "closed", headers[j].value_len) == 0)) return 1;
            return 0;
        }

    return -1;
}

int http_response(int cliente, int code, char* server_signature, char* server_root, int method, char *path, char* arguments) {
    char *response = NULL;
    char *cabeceras = NULL;
    char codestring[MAX_CODESTRING], *htmlcontent = NULL, content_size[MAX_CSIZE_LEN], *lastmodified_in = NULL, *filetype = NULL;
    char final_path[MAX_PATH];
    long int final_length = 0;
    long int contentt_length = 0;
    char *allow = "OPTIONS, GET, POST, HEAD";

    /* Escribiendo la línea de respuesta */
    response = (char*)malloc((strlen("HTTP/1.1 ")+1)*sizeof(char));
    if (response == NULL) {
        log_error("malloc", errno);
        return -1;
    }
    response[0] = '\0';

    /* Copiamos el path correcto añadiendo la ruta del servidor al principio */
    sprintf(response, "HTTP/1.1 ");
    sprintf(final_path, "%s%s", server_root, &path[1]);

    /* Comprobamos si la peticion es options */
    if(method != 3){ //no es options
        allow = NULL;
    }
    else{ //si que es options
        code = 204;
    }

    if (method == 4){
        code = 204;
    }

    /* Traducimos el codigo de error en el servidor */
    if(translate_code(code, codestring, final_path, arguments, &filetype, &htmlcontent, &contentt_length, &lastmodified_in, method) == -1){
        free(response);
        return http_response(cliente, 500, server_signature, server_root, 1, path, NULL);
    }
    sprintf(content_size, "%ld", contentt_length);
    
    /* En caso de OK las cabeceras son normales */
    if ((cabeceras = build_cabecera(server_signature, lastmodified_in, content_size, filetype, allow)) == NULL) {
        log_error_msg("Error en build_cabecera");
        if (filetype != NULL) free(filetype);
        if (lastmodified_in != NULL) free(lastmodified_in);
        free(response);
        return -1;
    }
    
    /* Escribiendo el código de error, +2  para el \r\n */
    response = (char*)realloc(response, strlen(response)+strlen(codestring)+2+1);
    if (response == NULL) return -1;

    /* Concatenamos el código de error */
    if (strcat(response, codestring) == NULL) {
        free(response);    
        free(htmlcontent);
        free(cabeceras);
        if (filetype != NULL) free(filetype);
        if (lastmodified_in != NULL) free(lastmodified_in);
        return -1;
    }
    /* Concatenamos \r\n */
    if (strcat(response, "\r\n") == NULL) {
        free(response); 
        if (filetype != NULL) free(filetype);
        if (lastmodified_in != NULL) free(lastmodified_in);
        return -1;
    }
    
    /* Escribiendo líneas de cabecera, +4  para el \r\n * 2 */
    response = (char*)realloc(response, strlen(response)+strlen(cabeceras)+3);
    if (response == NULL) {
        free(response);    
        free(htmlcontent);
        free(cabeceras);
        if (filetype != NULL) free(filetype);
        if (lastmodified_in != NULL) free(lastmodified_in);
        return -1;
    }
    /* Concatenamos las cabeceras */
    if (strcat(response, cabeceras) == NULL) {
        free(response);    
        free(htmlcontent);
        free(cabeceras);
        if (filetype != NULL) free(filetype);
        if (lastmodified_in != NULL) free(lastmodified_in);
        return -1;
    }
    /* Concatenamos \r\n 2 veces */
    if (strcat(response, "\r\n") == NULL) {
        free(response);    
        free(htmlcontent);
        free(cabeceras);
        if (filetype != NULL) free(filetype);
        if (lastmodified_in != NULL) free(lastmodified_in);
        return -1;
    }
       
    /* Enviamos el contenido por el socket */
    final_length = strlen(response);
    if (send(cliente, response, (size_t)final_length, 0) == -1) {
        perror("send");
        free(response);    
        free(htmlcontent);
        free(cabeceras);
        if (filetype != NULL) free(filetype);
        if (lastmodified_in != NULL) free(lastmodified_in);
        return -1;
    }

    /* Enviamos el objeto */
    if(contentt_length != 0){
        if (response == NULL) {   
            free(htmlcontent);
            free(cabeceras);
            if (filetype != NULL) free(filetype);
            if (lastmodified_in != NULL) free(lastmodified_in);
            return -1;
        }
        if (send(cliente, htmlcontent, (size_t)contentt_length, 0) == -1) {
            perror("send");
            free(response);    
            free(htmlcontent);
            free(cabeceras);
            if (filetype != NULL) free(filetype);
            if (lastmodified_in != NULL) free(lastmodified_in);
            return -1;
        }
    }

    /* Liberamos recursos usados para crear la respuesta */
    if(lastmodified_in != NULL) {
        free(lastmodified_in);
        lastmodified_in = NULL;
    }
    free(response);  
    response = NULL;  
    free(cabeceras);
    cabeceras = NULL;
    if(filetype != NULL) {
        free(filetype);
        filetype = NULL;
    }
    free(htmlcontent);
    htmlcontent = NULL;
    if(arguments) {
        free(arguments);
        arguments = NULL;
    }
    return 0;
}
