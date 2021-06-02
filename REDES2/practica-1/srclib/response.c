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

#define MAX_DATE 35
#define MAX_FILE_TYPE_LEN 30


char *build_cabecera(char *server, char *last_modified, char *content_length, char *content_type, char *allow) {
    char *cabecera = NULL, date_now[MAX_DATE];
    struct tm *local; 
    time_t rawtime;

    /* Obtenemos la hora actual */
    time(&rawtime);
    if ((local = localtime(&rawtime)) == NULL) {
        log_error("localtime", errno);
        return NULL;
    }
    if (strftime(date_now, MAX_DATE,"%a, %d %b %Y %X GMT", local) == -1) {
        log_error("strftime", errno);
        return NULL;
    }

    /* Concatenamos la fecha */
    cabecera = (char*)realloc(cabecera, strlen("Date: ")+strlen(date_now)+2+1);
    sprintf(cabecera, "Date: ");
    if (cabecera == NULL) {
        log_error("realloc", errno);
        return NULL;
    }
    if (strcat(cabecera, date_now) == NULL) {
        log_error("strcat", errno);
        return NULL;
    }
    if (strcat(cabecera, "\r\n") == NULL) {
        log_error("strcat", errno);
        return NULL;
    }
    
    /* Concatenamos el nombre del servidor */
    cabecera = (char*)realloc(cabecera, strlen(cabecera)+strlen("Server: ")+strlen(server)+2+1);
    if (cabecera == NULL) {
        log_error("realloc", errno);
        return NULL;
    }
    if (strcat(cabecera, "Server: ") == NULL) {
        log_error("strcat", errno);
        return NULL;
    }
    if (strcat(cabecera, server) == NULL) {
        log_error("strcat", errno);
        return NULL;
    }
    if (strcat(cabecera, "\r\n") == NULL) {
        log_error("strcat", errno);
        return NULL;
    }
    
    /* Concatenamos la última modificación */
    if(last_modified != NULL){
        /* Last-Modified */
        cabecera = (char*)realloc(cabecera, strlen(cabecera)+strlen("Last-Modified: ")+strlen(last_modified)+2+1);
        if (cabecera == NULL) {
            log_error("realloc", errno);
            return NULL;
        }
        if (strcat(cabecera, "Last-Modified: ") == NULL){
            log_error("strcat", errno);
            return NULL;
        }
        if (strcat(cabecera, last_modified) == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
        if (strcat(cabecera, "\r\n") == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
    }

    /* Concatenamos la longitud del objeto a enviar */
    if(content_length != NULL){
        cabecera = (char*)realloc(cabecera, strlen(cabecera)+strlen("Content-Length: ")+strlen(content_length)+2+1);
        if (cabecera == NULL) {
            log_error("realloc", errno);
            return NULL;
        }
        if (strcat(cabecera, "Content-Length: ") == NULL){
            log_error("strcat", errno);
            return NULL;
        }
        if (strcat(cabecera, content_length) == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
        if (strcat(cabecera, "\r\n") == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
    }

    /* Concatenando el tipo de objeto a enviar */
    if (content_type != NULL) {
        cabecera = (char*)realloc(cabecera, strlen(cabecera)+strlen("Content-Type: ")+strlen(content_type)+2+1);
        if (cabecera == NULL) {
            log_error("realloc", errno);
            return NULL;
        }
        if (strcat(cabecera, "Content-Type: ") == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
        if (strcat(cabecera, content_type) == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
        if (strcat(cabecera, "\r\n") == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
    }

    /* Concatenando metodos permitidos por el servidor */
    if (allow != NULL) {
        cabecera = (char*)realloc(cabecera, strlen(cabecera)+strlen("Allow: ")+strlen(allow)+2+1);
        if (cabecera == NULL) {
            log_error("realloc", errno);
            return NULL;
        }
        if (strcat(cabecera, "Allow: ") == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
        if (strcat(cabecera, allow) == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
        if (strcat(cabecera, "\r\n") == NULL) {
            log_error("strcat", errno);
            return NULL;
        }
    }

    return cabecera;
}

char *read_page(char *filename) {
    char *page = NULL;
    size_t filelen = 1024;
    FILE *pf = NULL;

    /* Abrimos el archivo con la página de error 400 */
    pf = fopen(filename, "r");
    if (pf == NULL) {
        log_error("fopen", errno);
        page = (char*)malloc(sizeof(char)*(strlen("<!DOCTYPE HTML><html><body><h1>404 Not found</h1><body></html>")+1));
        strcpy(page, "<!DOCTYPE HTML><html><body><h1>404 Not found</h1><body></html>");
        return page;
    }

    /* Obtenemos la longitud del archivo */
    fseek(pf, 0, SEEK_END);
    filelen = ftell(pf);
    rewind(pf);

    /* Leyendo la página a traves de el tamaño de un buffer */
    page = (char*)malloc((filelen+1)*sizeof(char));
    if (page == NULL) {
        fclose(pf);
        return NULL;
    }

    /* Inicializando la variable */
    memset(page, '\0', filelen);

    /* Leemos la página */
    fread(page, filelen, sizeof(char), pf);
    page[filelen] = '\0';

    fclose(pf);
    return page;
}

int translate_code(int code, char* codestring, char *path, char *arguments, char **type, char** html_content, long int* content_lenth, char **lastmodified_in, short method) {
    long int filelen = -1;
    FILE *pf = NULL;
    char *format = NULL;
    char isScript = 0, isRoot = 0;
    *lastmodified_in = NULL;

    /* Comprobamos el formato de la petición */
    if((format = return_format(path, &isScript, &isRoot)) == NULL) code = 415; // Si es NULL significa que la request esta mal formada 
    else if (strncmp(path, "htmlfiles/*", 11) == 0);
    else {
        pf = fopen(path, "rb"); // Abrimos el archivo en modo binario
        if (pf == NULL && errno == 2) {
            code = 404; // Si el archivo no esta cambiamos el código a not found
        }
        else if (pf == NULL) { // En caso de error salimos
            log_error("fopen", errno);
            return -1;
        } 
    }

    /* Reservamos memoria para el tipo de respuesta */
    *type = (char*)malloc(sizeof(char)*MAX_FILE_TYPE_LEN);
    if (*type == NULL) {
        log_error("malloc", errno);
        return -1; 
    }
    *type[0] = '\0';

    /* Dependiendo del codigo de error, establecemos una respuesta u otra */
    switch (code){
        case 415: 
            /* En caso de que se hubiese abierto un archivo lo cerramos, no es encesario */
            if (pf != NULL) fclose(pf);

            /* Código de respuesta */
            sprintf(codestring, "415 Unsupported Media Type");

            /* Objeto de la respuesta */
            *html_content = read_page("htmlfiles/errors/error415.html");
            if (html_content == NULL) {
                free(*type);
                return -1;
            }

            /* Formato de la respuesta */
            strcpy(*type, "text/html\0");

            /* Longitud de la respuesta */
            *content_lenth = strlen(*html_content);
            break;
        
        case 500: 
            /* En caso de que se hubiese abierto un archivo lo cerramos, no es encesario */
            if (pf != NULL) fclose(pf);

            /* Código de respuesta */
            sprintf(codestring, "500 Internal Server Error");

            /* Objeto de la respuesta */
            *html_content = read_page("htmlfiles/errors/error500.html");
            if (html_content == NULL) {
                free(*type);
                return -1;
            }

            /* Formato de la respuesta */
            strcpy(*type, "text/html\0");

            /* Longitud de la respuesta */
            *content_lenth = strlen(*html_content);
            break;

        case 505: 
            /* En caso de que se hubiese abierto un archivo lo cerramos, no es encesario */
            if (pf != NULL) fclose(pf);

            /* Código de respuesta */
            sprintf(codestring, "505 HTTP Version not supported");

            /* Objeto de la respuesta */
            *html_content = read_page("htmlfiles/errors/error505.html");
            if (html_content == NULL) {
                free(*type);
                return -1;
            }

            /* Formato de la respuesta */
            strcpy(*type, "text/html\0");

            /* Longitud de la respuesta */
            *content_lenth = strlen(*html_content);
            break;

        case 400: 
            /* En caso de que se hubiese abierto un archivo lo cerramos, no es encesario */
            if (pf != NULL) fclose(pf);

            /* Código de respuesta */
            sprintf(codestring, "400 Bad Request");

            /* Objeto de la respuesta */
            *html_content = read_page("htmlfiles/errors/error400.html");
            if (html_content == NULL) {
                free(*type);
                return -1;
            }

            /* Formato de la respuesta */
            strcpy(*type, "text/html\0");

            /* Longitud de la respuesta */
            *content_lenth = strlen(*html_content);
            break;
        case 404:
            /* En caso de que se hubiese abierto un archivo lo cerramos, no es encesario */
            if (pf != NULL) fclose(pf);

            /* Código de respuesta */
            sprintf(codestring, "404 Not found");

            /* Objeto de la respuesta */
            *html_content = read_page("htmlfiles/errors/error404.html");
            if (html_content == NULL) {
                free(*type);
                return -1;
            }

            /* Formato de la respuesta */
            strcpy(*type, "text/html\0");

            /* Longitud de la respuesta */
            *content_lenth = strlen(*html_content);
            break;
        case 413:
            /* En caso de que se hubiese abierto un archivo lo cerramos, no es encesario */
            if (pf != NULL) fclose(pf);

            /* Código de respuesta */
            sprintf(codestring, "413 Payload Too Large");

            /* Objeto de la respuesta */
            *html_content = read_page("htmlfiles/errors/error413.html");
            if (html_content == NULL) {
                free(*type);
                return -1;
            }

            /* Formato de la respuesta */
            strcpy(*type, "text/html\0");

            /* Longitud de la respuesta */
            *content_lenth = strlen(*html_content);
            break;
        case 405:
            /* En caso de que se hubiese abierto un archivo lo cerramos, no es encesario */
            if (pf != NULL) fclose(pf);

            /* Código de respuesta */
            sprintf(codestring, "405 Method Not Allowed");

            /* Objeto de la respuesta */
            *html_content = read_page("htmlfiles/errors/error405.html");
            if (html_content == NULL) {
                free(*type);
                return -1;
            }

            /* Formato de la respuesta */
            strcpy(*type, "text/html\0");

            /* Longitud de la respuesta */
            *content_lenth = strlen(*html_content);
            break;
        case 200:
            /* Si en la petición se pide ejecutar un script lo hacemos de otra forma */
            if (isScript == 1 || isScript == 2) {
                /* En caso de que se hubiese abierto el archivo del script lo cerramos */
                if (pf != NULL) fclose(pf);

                /* Establecemos el formato de la salida */
                strcpy(*type, "text/plain");
                
                /* Llamamos al cgi */
                if (call_cgi(path, arguments, isScript, html_content) == -1) {
                    free(*type);
                    log_error_msg("Error al llamar al CGI");
                    return translate_code(500, codestring, path, arguments, type, html_content, content_lenth, lastmodified_in, method);
                }

                /* Asignamos la última modificación */
                *lastmodified_in = (char*)malloc(sizeof(char)*(MAX_DATE+1));
                if (getModifiedTime(path, *lastmodified_in) == -1) {
                    log_error_msg("Error en getModifiedTime");
                    fclose(pf);
                    return -1;
                }

                /* Incluyendo el código */
                sprintf(codestring, "200 OK");

                /* Longitud de la salida */
                *content_lenth = strlen(*html_content);
                break;
            } else if (isRoot == 1) {
                /* En caso de que se hubiese abierto un archivo lo cerramos, no es encesario */
                if (pf != NULL) fclose(pf);

                /* Código de respuesta */
                sprintf(codestring, "200 OK");

                /* Objeto de la respuesta */
                *html_content = read_page("htmlfiles/index.html");
                if (html_content == NULL) {
                    free(*type);
                    return -1;
                }

                /* Formato de la respuesta */
                strcpy(*type, "text/html\0");

                /* Longitud de la respuesta */
                *content_lenth = strlen(*html_content);
                break;
            }
            /* Obtenemos la ultima modificación */
            *lastmodified_in = (char*)malloc(sizeof(char)*(MAX_DATE+1));
            if (getModifiedTime(path, *lastmodified_in) == -1) {
                log_error_msg("Error en getModifiedTime");
                fclose(pf);
                return -1;
            }

            /* Asignando el tipo de la respuesta*/
            strcpy(*type, format);
            sprintf(codestring, "200 OK");
            if (fseek(pf, 0, SEEK_END) == -1) {
                log_error("fseek", errno);
                fclose(pf);
                if((*type) != NULL) free(*type);
                return -1;
            }

            /* Calculamos el size del objeto */
            filelen = ftell(pf); // Calculamos el size del file
            if (filelen == -1) {
                log_error("ftell", errno);
                fclose(pf);
                if((*type) != NULL) free(*type);
                return -1;
            }
            
            rewind(pf);

            /* Reservamos memoria para el objeto a enviar */
            *html_content = (char *)malloc((filelen * sizeof(char)));
            if (*html_content == NULL) {
                log_error("malloc", errno);
                fclose(pf);
                if((*type) != NULL) free(*type);
                return -1;
            }

            /* Leemos el objeto */
            if (fread(*html_content, sizeof(char), filelen, pf) == -1) {
                log_error("fread", errno);
                fclose(pf);
                free(html_content);
                if((*type) != NULL) free(*type);
                return -1;
            }
            fclose(pf);
            *content_lenth = filelen;
            break;
        
        case 204:
            if (pf != NULL) fclose(pf);

            /* En caso de que no haya contenido */
            sprintf(codestring, "204 No Content");
            *html_content = NULL;
            if((*type) != NULL) free(*type);
            
            *lastmodified_in = (char*)malloc(sizeof(char)*(MAX_DATE+1));
            if (getModifiedTime(path, *lastmodified_in) == -1) {
                log_error_msg("Error en getModifiedTime");
                fclose(pf);
                if((*type) != NULL) free(*type);
                return -1;
            }
            *content_lenth = 0;

            *type = NULL;
            break;
        default:
            return -1;
    }
    return 0;
}

int isScript(char *request) {
    
    char *filetype = NULL;
    char *request_copy = NULL;

    if (request == NULL) return 0;

    request_copy = (char*)malloc(strlen(request)*sizeof(char));
    if (request_copy == NULL) {
        log_error("malloc", errno);
        return -1;
    }
    strcpy (request_copy, request );
    
    filetype = strtok(request_copy, ".");
    filetype = strtok(NULL, ".");
    int return_number = -1;
    
    if (strcmp(filetype, "py") == 0) return_number = 1;
    else if (strcmp(filetype, "php") == 0) return_number = 2;
 
    free(request_copy);
    return return_number;
}

int getModifiedTime(char *path, char* date_now) {
    struct stat attr;
    struct tm *local;

    /* Guardamos la información del archivo */
    stat(path, &attr);

    /* Obtenemos la hora del la ultima modificación */
    if ((local = localtime(&attr.st_mtime)) == NULL) {
        log_error("localtime", errno);
        return -1;
    }
    if (strftime(date_now, MAX_DATE,"%a, %d %b %Y %X GMT", local) == -1) {
        log_error("strftime", errno);
        return -1;
    }

    return 0;
}

char *return_format(char* path, char* isScript, char *isRoot) {
    short whereispunto = -1;

    /* Buscamos el punto dentro de la ruta del archivo a buscar */
    for(int i = strlen(path) -1; i>=0; i--)
        if(path[i] == '.'){
            whereispunto = i;
            break;
        }

    /* En caso de no encontrar punto comprobamos si es la página principal */
    if (whereispunto == -1) {
        if (strncmp(path, "htmlfiles/", 10) == 0 || strncmp(path, "htmlfiles", 9) == 0 ) {
            *isRoot = 1;
            return "text/html";
        } else return NULL;
    } 

    /* Guardamos la extensión del archivo */
    char* extension = &path[whereispunto+1];

    *isScript = 0;

    /* dependiendo de la extensión devolvemos un formato */
    if (!strcmp(extension, "html")) return "text/html";
    else if(!strcmp(extension, "gif")) return "image/gif";
    else if((!strcmp(extension, "jpeg")) || (!strcmp(extension, "jpg")) ) return "image/jpeg";
    else if(!strcmp(extension, "mpeg")) return "image/mpeg";
    else if(!strcmp(extension, "mpg")) return "image/mpeg";
    else if((!strcmp(extension, "doc")) || (!strcmp(extension, "docx"))) return "application/msword";
    else if(!strcmp(extension, "pdf")) return "application/pdf";
    else if(!strcmp(extension, "txt")) return "text/plain";
    else if(!strcmp(extension, "ico")) return "image/x-icon";
    else if(!strcmp(extension, "py")) {*isScript = 1; return "text/html";}
    else if(!strcmp(extension, "php")) {*isScript = 2; return "text/html";}

    return NULL;
}