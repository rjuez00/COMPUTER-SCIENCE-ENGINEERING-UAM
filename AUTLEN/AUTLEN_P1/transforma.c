#include <stdlib.h>
#include "newstate.h"
#include "types.h"
#include "transforma.h"

typedef struct {
    int n_rows;
    int n_entradas;
    NewState ***estados;
} Table;

Table* Table_Create(NewState* initial, int n_entradas);
BOOL Table_Add_Transition(Table* table, NewState* og, int entrada, NewState* dest);
void Table_Free(Table* table);

void Table_Print(Table* table);

/**
 * Recibe un array de in dinámico de tamaño size, le aumenta el tamaño en uno y mete un elemento nuevo al final.
 * No introduce elementos repetidos.
 */
int* append_int(int* array, int* size, int element){
    short flag_initialized = 1;

    if(!array)
        flag_initialized=0;

    /* Mira si está repetido el elemento */
    if(flag_initialized == 1) 
        for (int i=0; i<*size; i++)
            if(array[i] == element)
                return array;
    
    ++(*size);
    
    if(!flag_initialized)
        array = (int*)malloc((*size) * sizeof(int));
    else
        array = (int*)realloc(array, (*size) * sizeof(int));
    
    if (!array) {
        fprintf(stderr, "Error in realloc or malloc in int append");
        return NULL;
    }
    
    array[(*size)-1] = element;
    return array;
}

/**
 *  IMPORTANTE: AFNDCierraLTransición tiene que haber sido llamada antes de llamar a esta funcion
 */
int* funcion_conjunto_lambda(AFND* p_afnd, int* estados, int* size) {
    int num_estados_afnd = AFNDNumEstados(p_afnd);

    /* Itera por todos los estados en el mismo nuevo estado por todas las entradas.
       Este proceso se repite hasta que el número de estados no aumenta (no hay estados a los
       que se puede transicionar con una transicion lambda) */
        
    for(int i=0; i<(*size); i++)
        for(int j=0; j< num_estados_afnd; j++)
            if(AFNDLTransicionIJ(p_afnd, estados[i], j))
                estados = append_int(estados, size, j);


    return estados;
}


/**
 * Recibe un estado formado por un conjunto de estados y una entrada.
 * Devuelve un nuevo estado (NewState) formado por los estados que
 * se conectan mediante la entrada al conjunto inicial
 * 
 * ALERTA: en el primer NewState llamar a funcion_conjunto_lambda antes que a esta función
 */

NewState* funcion_conjunto_simbolo(AFND* p_afnd, int* estados, int size, int entrada){
    int num_estados_afnd = AFNDNumEstados(p_afnd);
    int* nd_states = NULL;
    int sizearray = 0;

    for(int i=0; i<size; i++)
        for(int j=0; j<num_estados_afnd; j++)
            if(AFNDTransicionIndicesEstadoiSimboloEstadof(p_afnd, estados[i], entrada, j))
                nd_states = append_int(nd_states, &sizearray, j);
            

    if (!nd_states)
        return NULL;

    nd_states = funcion_conjunto_lambda(p_afnd, nd_states, &sizearray);
    
    return NewState_create(FALSE, nd_states, sizearray, p_afnd);
}

/**
 * Genera la tabla de datos intermedia a partir del afnd de entrada
 */
Table* genera_table(AFND* afnd){
    int* initial_states = NULL;
    int length = 0;
    
    int num_simbolos = AFNDNumSimbolos(afnd);
    int num_estados = AFNDNumEstados(afnd);
    NewState* target = NULL;

    /* Busca un estado inicial / inicial y final */
    for (int i=0; i<num_estados; ++i)
        if ( (AFNDTipoEstadoEn(afnd, i) == INICIAL) || (AFNDTipoEstadoEn(afnd, i)== INICIAL_Y_FINAL) )
            initial_states = append_int(initial_states, &length, i);
    
    /* Si no existe un nodo inicial */
    if(!initial_states){
        fprintf(stderr, "No hay estado inicial");
        return NULL;
    }
    /* Busca estados a los que puede moverse mediante una transicion lambda */
    initial_states = funcion_conjunto_lambda(afnd, initial_states, &length);
    
    /* Crea un nuevo estado inicial e inicializa la tabla con el */
    NewState* inicial = NewState_create(TRUE, initial_states, length, afnd);
    Table* tabla = Table_Create(inicial, num_simbolos);
    if (!tabla) {
        fprintf(stderr, "Error al crear al tabla\n");
        return NULL;
    }

    int curr_row = 0;
    
    while(curr_row < tabla->n_rows){
        /* fprintf(stderr, "%s\n", NewState_getname(tabla->estados[curr_row][0])); */
        for(int i=0; i<num_simbolos; i++){
            target = funcion_conjunto_simbolo(afnd, NewState_getstates(tabla->estados[curr_row][0]), NewState_getstateslen(tabla->estados[curr_row][0]), i);
            /* printf("\t%s\n", NewState_getname(target)); */
            if (target)
                Table_Add_Transition(tabla, tabla->estados[curr_row][0], i, target);
        }
        ++curr_row;
    }

    return tabla;
}


AFND * AFNDTransforma(AFND* afnd) {
    Table* tabla = genera_table(afnd);
    Table_Print(tabla);
    
    AFND *afd = AFNDNuevo("determinista", tabla->n_rows, tabla->n_entradas);
    for(int i=0; i<tabla->n_entradas; i++)
        AFNDInsertaSimbolo(afd, AFNDSimboloEn(afnd, i));
    
    for(int i=0; i<tabla->n_rows; i++){
        AFNDInsertaEstado(afd, NewState_getname(tabla->estados[i][0]), NewState_gettype(tabla->estados[i][0]));
    }

    for(int i=0; i<tabla->n_rows; i++)
        for(int j=0; j<tabla->n_entradas; j++)
            if (tabla->estados[i][j+1])
                AFNDInsertaTransicion(afd, NewState_getname(tabla->estados[i][0]), AFNDSimboloEn(afnd, j), NewState_getname(tabla->estados[i][j+1]));
   
    Table_Free(tabla);

    return afd;
}


Table* Table_Create(NewState* initial, int n_entradas){
    Table* table = NULL;
    table = (Table*)malloc(sizeof(Table));
    if(!table)
        return NULL;
    
    table->n_rows = 1;
    table->n_entradas = n_entradas;


    table->estados = (NewState ***)calloc(table->n_rows, sizeof(NewState **)); 
    table->estados[0] = (NewState **)calloc(n_entradas+1, sizeof(NewState *));
    
    
    table->estados[0][0] = initial;
    return table;
}

/* Cambiar comparacion a funcion newstate compare y hacer free */
BOOL Table_Add_Transition(Table* table, NewState* og, int entrada, NewState* dest){
    int flag_found = -1;
    int flag_dest  = -1;
    if(!table || !og || !dest){
        fprintf(stderr, "argument null in add_transition\n");
        return FALSE;
    }

    for(int i=0; i<(table->n_rows); i++)
        if(compare_NewState(table->estados[i][0], og))
            flag_found = i;
        
            
        

    if (flag_found == -1){
        table->n_rows +=1;
        table->estados = realloc(table->estados, table->n_rows * sizeof(NewState*));
        if(!table->estados) {
            fprintf(stderr, "Compra más RAM: https://www.pccomponentes.com/memorias-ram \n");
            return FALSE;
        }
        
        table->estados[table->n_rows-1] = (NewState **)calloc(table->n_entradas+1, sizeof(NewState*));
        if(!table->estados[table->n_rows-1]){
            fprintf(stderr, "Compra más RAM: https://www.pccomponentes.com/memorias-ram \n");
            return FALSE;
        }
        table->estados[table->n_rows-1][0] = og;
        flag_found = table->n_rows -1;
    }





    for(int i=0; i<(table->n_rows); i++)
        if(compare_NewState(table->estados[i][0], dest)){
            NewState_destroy(dest);
            dest = table->estados[i][0];
            flag_dest = i;
        }
    

    if (flag_dest == -1){
        table->n_rows +=1;
        table->estados = realloc(table->estados, table->n_rows * sizeof(NewState*));
        if(!table->estados) {
            fprintf(stderr, "Compra más RAM: https://www.pccomponentes.com/memorias-ram \n");
            return FALSE;
        }
        
        table->estados[table->n_rows-1] = (NewState **)calloc(table->n_entradas+1, sizeof(NewState*));
        if(!table->estados[table->n_rows-1]){
            fprintf(stderr, "Compra más RAM: https://www.pccomponentes.com/memorias-ram \n");
            return FALSE;
        }
        table->estados[table->n_rows-1][0] = dest;
    }

    table->estados[flag_found][entrada+1] = dest;
    
    return TRUE;
}

void Table_Free(Table* table){
    if (table) {
        for(int i=0; i< table->n_rows; i++){
            NewState_destroy(table->estados[i][0]);
            free(table->estados[i]);
        }
        free(table->estados);
        free(table);
    }
}

void Table_Print(Table* table){
    if (table) {
        printf("Original State | Transitions\n");
        for(int i=0; i< table->n_rows; i++){
            printf("%s |", NewState_getname(table->estados[i][0]));
            for(int j=0; j< table->n_entradas; j++){
                if (table->estados[i][j+1]) {
                    printf("%s ", NewState_getname(table->estados[i][j+1]));
                } else {
                    printf("Vacío ");
                }
            }
            printf("\n");
        }
    }
}
