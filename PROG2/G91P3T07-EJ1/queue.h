#ifndef QUEUE_H
#define QUEUE_H

#include <stdio.h>
#include <stdlib.h>

#define MAXQUEUE 1000


#include "types.h"

typedef struct _Queue Queue;
/* Types of function pointers supported by the queue. Note: they could be in elem_functions.h and include it here */
typedef void (*destroy_element_function_type)(void*);
typedef void (*(*copy_element_function_type)(const void*));
typedef int (*print_element_function_type)(FILE *, const void*);
/**------------------------------------------------------------------
Initializes the queue: reserves memory for it and initializes all its elements to NULL.
------------------------------------------------------------------*/
Queue* queue_ini(destroy_element_function_type f1, copy_element_function_type f2, print_element_function_type f3);
/**------------------------------------------------------------------
Free the queue, freeing all its elements.
------------------------------------------------------------------*/
void queue_destroy(Queue *q);
/**------------------------------------------------------------------
Checks if the queue is empty.
------------------------------------------------------------------*/
Bool queue_isEmpty(const Queue *q);
/**------------------------------------------------------------------
Checks if the queue is full.
------------------------------------------------------------------*/
Bool queue_isFull(const Queue* queue);
/**------------------------------------------------------------------
Inserts a new node in the queue, reserving new memory for it and making a copy of the received element.
------------------------------------------------------------------*/
Queue* queue_insert(Queue *q, const void* pElem);
/**------------------------------------------------------------------
Extracts an element from the queue. Returns the pointer directly to the element (does not make a copy).
------------------------------------------------------------------*/
void * queue_extract(Queue *q);
/**------------------------------------------------------------------
Returns the number of queue elements.
------------------------------------------------------------------*/
int queue_size(const Queue *q);
/**------------------------------------------------------------------
Prints all the queue, returning the number of written characters.
------------------------------------------------------------------*/
int queue_print(FILE *pf, const Queue *q);



#endif /* QUEUE_H */