#include "queuel.h"
#include <errno.h>
#include <string.h>

extern int errno;

struct _Queue {
    List* list;
    destroy_element_function_type destroy_element_function;
    copy_element_function_type copy_element_function;
    print_element_function_type print_element_function;
};

/*Private functions*/
int function_not_used(const void *pelem, const void *pelem2){return 0;}


/**------------------------------------------------------------------
Initializes the queue: reserves memory for it and initializes all its elements to NULL.
------------------------------------------------------------------*/
Queue* queue_ini(destroy_element_function_type f1, copy_element_function_type f2, print_element_function_type f3){
    Queue *new=NULL;
    new=(Queue*)malloc(sizeof(Queue));
    if(!new) {
        fprintf(stderr, "Error opening file: %s\n", strerror(errno));
        return NULL;
        }
    new->destroy_element_function=f1;
    new->copy_element_function=f2;
    new->print_element_function=f3;
    new->list=list_ini(f1, f2, f3, function_not_used);
    if(!(new->list)){free(new);}
    return new;
}
/**------------------------------------------------------------------
Free the queue, freeing all its elements.
------------------------------------------------------------------*/
void queue_destroy(Queue *q){
    if(!q){return;}

    list_destroy(q->list);
    free(q);
}
/**------------------------------------------------------------------
Checks if the queue is empty.
------------------------------------------------------------------*/
Bool queue_isEmpty(const Queue *q){
    if(!q){return TRUE;}
    if(list_isEmpty(q->list)==TRUE){return TRUE;}
    return FALSE;
}
/**------------------------------------------------------------------
Checks if the queue is full.
------------------------------------------------------------------*/
Bool queue_isFull(const Queue* queue){
    if(!queue){return TRUE;}
    return FALSE;
}
/**------------------------------------------------------------------
PUSH a new node in the queue, reserving new memory for it and making a copy of the received element.
------------------------------------------------------------------*/
Queue* queue_insert(Queue *q, const void* pElem){
    /*PUSH CODE*/
    if(!q || !pElem){return NULL;}
    if(list_insertLast(q->list,pElem)==ERROR){return NULL;}
    return q;
}
/**------------------------------------------------------------------
POPS an element from the queue. Returns the pointer directly to the element (does not make a copy).
------------------------------------------------------------------*/
void* queue_extract(Queue *q){
    void *temp=NULL;
    if(!q || queue_isEmpty(q)==TRUE){return NULL;}
    temp=list_extractFirst(q->list);
    return temp;
}
/**------------------------------------------------------------------
Returns the number of queue elements.
------------------------------------------------------------------*/
int queue_size(const Queue *q){
    if(!q){return -1;}

    return list_size(q->list);
}
/**------------------------------------------------------------------
Prints all the queue, returning the number of written characters.
------------------------------------------------------------------*/
int queue_print(FILE *pf, const Queue *q){
    int printed=0;
    if(!pf || !q){return -1;}
    if(list_isEmpty(q->list)==TRUE){
        printed+=fprintf(pf, "Queue is empty\n");
        return printed;
    }
    fprintf(pf, "Queue with %d elements: ", list_size(q->list));
    return list_print(pf, q->list);
}
