#include "queue.h"
#include <errno.h>
#include <string.h>

extern int errno;

struct _Queue {
    void* items [MAXQUEUE];
    int front;
    int rear;
    destroy_element_function_type destroy_element_function;
    copy_element_function_type copy_element_function;
    print_element_function_type print_element_function;
};

/**------------------------------------------------------------------
Initializes the queue: reserves memory for it and initializes all its elements to NULL.
------------------------------------------------------------------*/
Queue* queue_ini(destroy_element_function_type f1, copy_element_function_type f2, print_element_function_type f3){
    int i=0;
    Queue *new=NULL;
    new=(Queue*)malloc(sizeof(Queue));
    if(!new) {
        fprintf(stderr, "Error opening file: %s\n", strerror(errno));
        return NULL;
        }

    for(i=0; i<MAXQUEUE; i++){
        new->items[i]=NULL;
    }
    new->front=0;
    new->rear=0; 

    new->destroy_element_function=f1;
    new->copy_element_function=f2;
    new->print_element_function=f3;
    return new;
}
/**------------------------------------------------------------------
Free the queue, freeing all its elements.
------------------------------------------------------------------*/
void queue_destroy(Queue *q){
    int i=0;
    if(!q){return;}

    for(i=q->front; i<q->rear; i++){
        q->destroy_element_function(q->items[i]);
    }

    q->front=0;
    q->rear=0;
   
    free(q);
}
/**------------------------------------------------------------------
Checks if the queue is empty.
------------------------------------------------------------------*/
Bool queue_isEmpty(const Queue *q){
    if(!q){return TRUE;}
    if(q->front == q->rear){return TRUE;}
    return FALSE;
}
/**------------------------------------------------------------------
Checks if the queue is full.
------------------------------------------------------------------*/
Bool queue_isFull(const Queue* queue){
    if(!queue){return TRUE;}
    if(queue->front == ((queue->rear)+1)%MAXQUEUE){
        return TRUE;
    }
    return FALSE;
}
/**------------------------------------------------------------------
PUSH a new node in the queue, reserving new memory for it and making a copy of the received element.
------------------------------------------------------------------*/
Queue* queue_insert(Queue *q, const void* pElem){
    /*PUSH CODE*/
    void *aux=NULL;
    if(!q || !pElem){return NULL;}
    if(queue_isFull(q)){return NULL;}
    aux=q->copy_element_function(pElem);
    q->items[q->rear]=aux;
    q->rear=(q->rear + 1)%MAXQUEUE;
    return q;
}
/**------------------------------------------------------------------
POPS an element from the queue. Returns the pointer directly to the element (does not make a copy).
------------------------------------------------------------------*/
void * queue_extract(Queue *q){
    void *temp=NULL;
    if(!q || queue_isEmpty(q)==TRUE){return NULL;}
    temp=q->items[q->front];
    q->items[q->front]=NULL;
    q->front=(q->front+1)% MAXQUEUE;
    return temp;
}
/**------------------------------------------------------------------
Returns the number of queue elements.
------------------------------------------------------------------*/
int queue_size(const Queue *q){
    int cuantt=0;
    if(!q){return -1;}
    cuantt=(q->rear - q->front)%MAXQUEUE;
    return cuantt;
}
/**------------------------------------------------------------------
Prints all the queue, returning the number of written characters.
------------------------------------------------------------------*/
int queue_print(FILE *pf, const Queue *q){
    int i=0;
    int printed=0;
    if(!pf || !q){return -1;}
    if(queue_isEmpty(q)){printed=fprintf(pf, "Queue is empty\n"); return printed;}
    fprintf(pf, "Queue with %d elements:\n", queue_size(q));
    for(i=q->front; i!=q->rear; i=(i+1)%MAXQUEUE){
        printed+=q->print_element_function(pf,q->items[i]);
        
    }
    fprintf(pf, "\n");
    return printed;
}