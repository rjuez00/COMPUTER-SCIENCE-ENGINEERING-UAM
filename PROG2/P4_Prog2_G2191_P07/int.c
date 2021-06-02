/** 
 * @brief Module for handeling ints
 * 
 * @file int.c
 * @author Rodrigo Juez and Enmanuel Abreu Gil 
 * @copyright GNU Public License
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "int.h"
extern int errno;
void int_destroy(void* e){
    if(!e){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function int_destroy: %s\n", strerror(errno));        
        
        return;
        }
    free(e);
}
void* int_copy(const void* e){
    int *new;
    if(!e){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function int_copy: %s\n", strerror(errno));  
        return NULL;
    }
    new=(int*)malloc(sizeof(int));
    if(!new){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in memory allocation in int_copy: %s\n", strerror(errno));  
        
        return NULL;
    }
    *new=*((int*)e);
    return new;
}
int int_print(FILE * f, const void* e){
    int cuantt=0;
    if(!f || !e){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function int_print: %s\n", strerror(errno));  

        return 0;}
    cuantt+=fprintf(f, " %d", *((int*)e));
    return cuantt;
}
int int_cmp(const void* e1, const void* e2){
    if(!e1 || !e2){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function int_cmp: %s\n", strerror(errno));  
        return -99999;}
    return *((int*)e1) - *((int*)e2);
}
void* int_ini (){
    int *new;
    new=(int*)malloc(sizeof(int));
    if(!new){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in memory allocation in int_ini: %s\n", strerror(errno));  
        return NULL;}
    *new=0;
    return (void*)new;
}
void* int_setInfo (void *e, int v){
    if(!e){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function int_setInfo: %s\n", strerror(errno));  
        return NULL;}
    *((int*)e)=v;
    return e;
}