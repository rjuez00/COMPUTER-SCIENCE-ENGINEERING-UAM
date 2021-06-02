#ifndef _ALFA_H
#define _ALFA_H

#define MAX_LONG_ID 100
#define MAX_TAMANIO_VECTOR 64

#define TRUE 1
#define FALSE 0
/* Element category */
#define VARIABLE 1
#define PARAMETER 2
#define FUNCTION 3

/* Basic data type */
#define INT 1
#define BOOLEAN 2

/* Category */
#define SCALAR 1
#define VECTOR 3

typedef struct _typeattr {
    char lexema[MAX_LONG_ID+1];
    int tipo;
    int valor_entero;
    int es_direccion;
    int etiqueta;
    int num_parametros;
    int morfoerr;
} tipo_atributo;


#endif