/** 
 * @brief Module for handeling strings
 * 
 * @file string.c
 * @author Rodrigo Juez
 * @copyright GNU Public License
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include "string.h"

extern int errno;

void string_destroy(void *e){
    char *destroy;
    if(!e) {
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument of string_destroy: %s\n", strerror(errno));        
        
        return;
    }

    destroy=e;
    free(destroy);
}

void* string_copy(const void *e){
    char* new=NULL;
    if(!e) {
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument of function string_copy : %s\n", strerror(errno));        
        return NULL;
    }

    new=(char*)malloc( (strlen((char*)e) + 1) *sizeof(char));
    if(!new) {
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in memory allocation in string_copy: %s\n", strerror(errno));        
        
        return NULL;

    }
    strcpy(new, (char*)e);
    return new;
}

int string_print(FILE *pf, const void* e){
    if(!e) {
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument of function string_print: %s\n", strerror(errno));        
        
        return -1;
    }
    return fprintf(pf, "%s ", (char*)e);
}

int string_cmp(const void *e1, const void *e2){
    if(!e1||!e2) {
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument of function string_cmp: %s\n", strerror(errno));        
                
        return -1;
    }

    return strcmp((char*)e1, (char*)e2);
}