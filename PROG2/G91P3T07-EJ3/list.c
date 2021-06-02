#include "list.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

typedef struct _NodeList { /* Private EdD, necessary to implement list */
    void* info;
    struct _NodeList *next;
} NodeList; /* Private NodeList type */

struct _List {
    NodeList *last; /* The LEC points to the last node and the last to the first */
    
    destroy_element_function_type destroy_element_function;
    copy_element_function_type copy_element_function;
    print_element_function_type print_element_function;
    cmp_element_function_type cmp_element_function;
};

/* Initializes the list by saving memory and initialize all its elements.*/
List* list_ini (destroy_element_function_type f1, copy_element_function_type f2, print_element_function_type f3, cmp_element_function_type f4){
    List *new=NULL;
    if(!f1 || !f2 || !f3 || !f4){
        fprintf(stderr, "Error with functions passed to list: %s\n", strerror(errno));
        return NULL;
    }

    new=(List*)malloc(sizeof(List));
    if(!new){
        fprintf(stderr, "Error allocating memory: %s\n", strerror(errno));
        return NULL;}
    new->last=NULL;
    new->destroy_element_function=f1;
    new->cmp_element_function=f4;
    new->copy_element_function=f2;
    new->print_element_function=f3;
    return new;
}

/* Frees the list, freeing all its elements. */
void list_destroy (List* list){
    NodeList *traverse=NULL;
    NodeList *next=NULL;
    int size=0, i;
    if(!list){return;}
    if(list_isEmpty(list)){free(list); return;}

    size=list_size(list);
    traverse=list->last->next; /*first*/
    for(i=0; i<size; i++){
        next=traverse->next;
        traverse->next=NULL;
        list->destroy_element_function(traverse->info);
        traverse->info=NULL;
        free(traverse);
        traverse=next;        
    }
    list->last=NULL;
    free(list);

    
}

/* Inserts at the beginning of the list making a copy of the information received. */
Status list_insertFirst (List* list, const void *pelem){
    NodeList *oldfirst=NULL;
    NodeList *newfirst=NULL;
    if(!list || !pelem){return ERROR;}

    newfirst=(NodeList*)malloc(sizeof(NodeList));
    if(!newfirst){return ERROR;}
    newfirst->info=list->copy_element_function(pelem);

    if(list_isEmpty(list)==TRUE){
        list->last=newfirst;
        newfirst->next=newfirst;
        return OK;
    }
    
    oldfirst=list->last->next;
    newfirst->next=oldfirst;

    list->last->next=newfirst;
    return OK;    
}

/* Inserts at the end of the list making a copy of the information received. */
Status list_insertLast (List* list, const void *pelem){
    NodeList *newlast=NULL;
    if(!list || !pelem){return ERROR;}
    newlast=(NodeList*)malloc(sizeof(NodeList));
    if(!newlast){return ERROR;}
    newlast->info=list->copy_element_function(pelem);
    
    if(list_isEmpty(list)){
        newlast->next=newlast;
        list->last=newlast;
        return OK;
    }
    newlast->next=list->last->next;
    list->last->next=newlast;
    list->last=newlast;
    
    return OK;
}


/* Extracts from the beginning of the list, returning directly the pointer to the info field of the extracted node, node that is
finally released. BEWARE: after saving the address of the info field to be returned and before releasing the node, it sets the
info field of the node to NULL, so that it does not continue pointing to the info to be returned and, therefore, does not
release it when releasing the node */
void* list_extractFirst (List* list){
    void* extractedelem=NULL;
    NodeList* newfirst=NULL;
    if(list_isEmpty(list)){return NULL;}
    extractedelem=list->last->next->info;
    list->last->next->info=NULL;

    if(list->last->next==list->last){
        free(list->last->next);
        list->last=NULL;
    }
    else {
        newfirst=list->last->next;
        list->last->next=newfirst->next;
        free(newfirst);
    }
    return extractedelem;
}

/* Extracts from the end of the list, directly returning the pointer to the info field of the extracted node, node that is finally
released. BEWARE: after saving the address of the info field to be returned and before releasing the node, it sets the info
field of the node to NULL, so that it does not continue pointing to the info to be returned and, therefore, does not release it
when releasing the node */
void* list_extractLast (List* list){
    NodeList *first=NULL;
    NodeList *oldLast=NULL;
    NodeList *newLast=NULL;
    void *elemtoextract=NULL;
    int size=0, i;
    if(!list){return NULL;}
    first=list->last->next;
    elemtoextract=list->last->info;
    list->last->info=NULL;
    oldLast=list->last;
    size=list_size(list);
    if(size==1){
        free(list->last);
        list->last=NULL;
        return elemtoextract;

    }
    size=size-2;

    newLast=first;
    for(i=0; i<size; i++){
        newLast=newLast->next;
    }
    
    list->last=newLast;
    list->last->next=first;

    free(oldLast);
    return elemtoextract;
}

/* Checks if a list is empty or not. */
Bool list_isEmpty (const List* list){
    if(!list){return TRUE;}
    if(list->last==NULL){return TRUE;}
    return FALSE;
}

/* Returns the information stored in the i-th node of the list. In case of error, returns NULL. */
const void* list_get (const List* list, int index){
    int size=0;
    int i;
    NodeList *traverse=NULL;
    if(!list || index <0){return NULL;}
    size=list_size(list);
    if(index>=size){return NULL;}
    traverse = list->last->next;
    for(i=0; i<index; i++){
        traverse=traverse->next;
    }
    return traverse;
}

/* Returns the number of elements in a list. */
int list_size (const List* list){
    NodeList *traverse=NULL;
    int cuantt=0;
    if(!list){return 0;}
    if(list_isEmpty(list)==TRUE){return 0;}
    traverse=list->last->next;
    cuantt++;
    while(traverse!=list->last){
        traverse=traverse->next;
        cuantt++;
    }
    return cuantt;
}

/* Prints a list returning the number of written characters. */
int list_print (FILE *fd, const List* list){
    int size=0;
    int i;
    int printed=0;
    Bool empty;
    NodeList *traverse=NULL;
    if(!fd || !list){return 0;}
    size=list_size(list);
    empty=list_isEmpty(list);
    if(empty==TRUE){return 0;}

    traverse=list->last->next;
    for(i=0; i<size; i++){
        printed+=list->print_element_function(fd, traverse->info);
        printed+=fprintf(fd," ");
        traverse=traverse->next;
    }
    fprintf(fd,"\n");
    return printed;
}

/* Inserts in order in the list making a copy of the element. */
Status list_insertInOrder (List *list, const void *pelem){
    NodeList *middle=NULL;
    NodeList *traverse=NULL;

    if(!list|| !pelem){return ERROR;}
    middle=(NodeList*)malloc(sizeof(NodeList));
    if(!middle){return ERROR;}
    middle->info=list->copy_element_function(pelem);

    if(list_isEmpty(list)){
        list->last=middle;
        middle->next=middle;
        return OK;
    }
    traverse=list->last->next;
    if(list->cmp_element_function(pelem, traverse->info)<0){
        list->destroy_element_function(middle->info);
        free(middle);
        return list_insertFirst(list, pelem);
    }
    while(traverse!=list->last && (list->cmp_element_function(pelem, traverse->next->info)>0)){
        traverse=traverse->next;
    }
    if(traverse==list->last){
        list->last=middle;
    }
    middle->next=traverse->next;
    traverse->next=middle;
    
    return OK;
}