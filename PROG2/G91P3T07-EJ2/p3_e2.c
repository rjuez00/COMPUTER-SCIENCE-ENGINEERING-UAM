#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "types.h"
#include "int.h"
#include "list.h"

#define MAXQUEUE 12
extern int errno;
int main(int argc, char **argv) {
    void *use=NULL;
    List *list1=NULL;
    List *list2=NULL;
    int arg, i;

    if(argc<2 || argc>2){
        printf("Expecting %s <integer>\n", argv[0]); return (EXIT_FAILURE);
    }

    arg=atoi(argv[1]);
    use=int_ini();
    list1=list_ini(int_destroy, int_copy, int_print, int_cmp);
    list2=list_ini(int_destroy, int_copy, int_print, int_cmp);
    if(!list1 || !list2 || !use){
        fprintf(stderr, "ERROR ALLOCATING MEMORY: %s\n", strerror(errno));
    }
    for(i=arg; i>0; i--){
        int_setInfo(use, i);
        if(!(i%2)){
            list_insertFirst(list1, use);
        }
        else{
            list_insertLast(list1,use);
        }
        list_insertInOrder(list2,use);
    }
    printf("List 1: "); list_print(stdout, list1);
    printf("\n\n");
    printf("List 2: "); list_print(stdout, list2);
    int_destroy(use);
    list_destroy(list1);
    list_destroy(list2);
    printf("\n");
    return (EXIT_SUCCESS);
}   

