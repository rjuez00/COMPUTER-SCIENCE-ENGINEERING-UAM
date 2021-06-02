#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "int.h"

void int_destroy(void* e){
    if(!e){return;}
    free(e);
}
void* int_copy(const void* e){
    int *new;
    new=(int*)malloc(sizeof(int));
    if(!new){return NULL;}
    *new=*((int*)e);
    return new;
}
int int_print(FILE * f, const void* e){
    int cuantt=0;
    if(!f || !e){return 0;}
    cuantt+=fprintf(f, "%d", *((int*)e));
    return cuantt;
}
int int_cmp(const void* e1, const void* e2){
    if(!e1 || !e2){return -99999;}
    return *((int*)e1) - *((int*)e2);
}
void* int_ini (){
    int *new;
    new=(int*)malloc(sizeof(int));
    if(!new){return NULL;}
    *new=0;
    return (void*)new;
}
void* int_setInfo (void *e, int v){
    if(!e){return NULL;}
    *((int*)e)=v;
    return e;
}