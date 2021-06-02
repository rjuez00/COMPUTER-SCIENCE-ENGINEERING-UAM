#include <stdio.h>
#include <stdlib.h>
#include "types.h"


typedef struct _List List;
/* Types of function pointers supported by the list. Note: they could be in elem_functions.h and include it here */
typedef void (*destroy_element_function_type)(void*);
typedef void*(*copy_element_function_type)(const void*);
typedef int (*print_element_function_type)(FILE *, const void*);
typedef int (*cmp_element_function_type)(const void*, const void*);
/* The last type of functions, cmp, will be those that serve to compare two elements, returning a positive, negative or zero
number according to the first argument greater, less or equal to the second */
/* Initializes the list by saving memory and initialize all its elements.*/
List* list_ini (destroy_element_function_type f1, copy_element_function_type f2, print_element_function_type f3,
cmp_element_function_type f4);
/* Frees the list, freeing all its elements. */
void list_destroy (List* list);
/* Inserts at the beginning of the list making a copy of the information received. */
Status list_insertFirst (List* list, const void *pelem);
/* Inserts at the end of the list making a copy of the information received. */
Status list_insertLast (List* list, const void *pelem);
/* Inserts in order in the list making a copy of the element. */
Status list_insertInOrder (List *list, const void *pelem);
/* Extracts from the beginning of the list, returning directly the pointer to the info field of the extracted node, node that is
finally released. BEWARE: after saving the address of the info field to be returned and before releasing the node, it sets the
info field of the node to NULL, so that it does not continue pointing to the info to be returned and, therefore, does not
release it when releasing the node */
void * list_extractFirst (List* list);
/* Extracts from the end of the list, directly returning the pointer to the info field of the extracted node, node that is finally
released. BEWARE: after saving the address of the info field to be returned and before releasing the node, it sets the info
field of the node to NULL, so that it does not continue pointing to the info to be returned and, therefore, does not release it
when releasing the node */
void * list_extractLast (List* list);
/* Checks if a list is empty or not. */
Bool list_isEmpty (const List* list);
/* Returns the information stored in the i-th node of the list. In case of error, returns NULL. */
const void* list_get (const List* list, int index);
/* Returns the number of elements in a list. */
int list_size (const List* list);
/* Prints a list returning the number of written characters. */
int list_print (FILE *fd, const List* list);