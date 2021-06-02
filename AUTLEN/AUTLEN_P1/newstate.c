#include <stdlib.h>
#include <string.h>
#include "newstate.h"

struct _NewState {
    int tipo;
    char* name;
    int length;
    int* nd_states;
    AFND* old_afnd;
};

int Sort(int* table, int length);


NewState* NewState_create(BOOL inicial, int* nd_states, int length, AFND* old_afnd){
    NewState* objectreturn = NULL;
    
    if(!nd_states || length <0){
        fprintf(stderr, "\tnd_states is null or length (%d) < 0\n", length);
        return NULL;
    }

    objectreturn  = (NewState*)malloc(sizeof(NewState));
    if (!objectreturn){
        printf("malloc ret null\n");
        return NULL;
    }

    Sort(nd_states, length);
    objectreturn->nd_states = nd_states;
    objectreturn->length = length;
    objectreturn->old_afnd = old_afnd;

    /* Crear el nombre del estado concatenando los nombres de los estados que lo forman */
    int required_size = 0;
    for (int i=0; i<length; ++i) {
        required_size += strlen(AFNDNombreEstadoEn(old_afnd, nd_states[i]));
    }
    ++required_size; /* \0 */
    objectreturn->name = (char *)malloc(required_size * sizeof(char));
    strcpy(objectreturn->name, "");
    for (int i=0; i<length; ++i) {
        strcat(objectreturn->name, AFNDNombreEstadoEn(old_afnd, nd_states[i]));
    }
    strcat(objectreturn->name, "\0");

    if (inicial) {

        objectreturn->tipo = INICIAL;
        for (int i=0; i<length; ++i) {
            if ( (AFNDTipoEstadoEn(old_afnd, nd_states[i]) == FINAL) || (AFNDTipoEstadoEn(old_afnd, nd_states[i]) == INICIAL_Y_FINAL) ) {
                objectreturn->tipo = INICIAL_Y_FINAL;
                break;
            }
        }

    } 
    else {

        objectreturn->tipo = NORMAL;
        for (int i=0; i<length; ++i) {
            if ( (AFNDTipoEstadoEn(old_afnd, nd_states[i]) == FINAL) || (AFNDTipoEstadoEn(old_afnd, nd_states[i]) == INICIAL_Y_FINAL) ) {
                objectreturn->tipo = FINAL;
                break;
            }
        }

    }
    
    return objectreturn;
}

void NewState_destroy(NewState* state){
    if (state) {
        free(state->name);
        free(state->nd_states);
        free(state);
    }
}

BOOL compare_NewState(NewState* state, NewState* state2){
    if(!state || !state2)
        return FALSE;
    
    if(state->length != state2->length)
        return FALSE;
    
    if (!strcmp(state->name, state2->name))
        return TRUE;
    
    /*for(int i=0; i<state->length; i++)
        if (state2->nd_states[i] != state->nd_states[i])
            return FALSE;*/
    return FALSE;
}

int Sort(int* table, int length){
    int ip = 0;
    int i, j, aux;
    if(!table || ip < 0 || length < 0){
        printf("ERROR in InsertSort input\n");
        return 1;
    }

    for(i = ip+1; i <= length-1; i++){
        aux = table[i];
        for(j = i-1; j >= ip; j--){
            if(table[j]>aux){
                table[j+1]=table[j]; 
            } else {break;}
        }

        table[j+1]=aux;

    }

    return 0;
}

char* NewState_getname(NewState* state) {
    if (!state) {
        return NULL;
    }
    return state->name;
}

int* NewState_getstates(NewState* state) {
    if (!state) {
        return NULL;
    }
    return state->nd_states;
}

int NewState_getstateslen(NewState* state) {
    if (!state) {
        return 0;
    }
    return state->length;
}

int NewState_gettype(NewState* state) {
    if (!state)
        return -1;

    return state->tipo;
}
