/** 
 * @brief Interface for the int module
 * 
 * @file int.h
 * @author Rodrigo Juez
 * @copyright GNU Public License
 */

#ifndef NODE_H_
#define NODE_H_
#include <stdlib.h>
#include <stdio.h>
#include "types.h"


void int_destroy(void* e);
void* int_copy(const void* e);
int int_print(FILE * f, const void* e);
int int_cmp(const void* e1, const void* e2);
void* int_ini ();
void* int_setInfo (void *e, int v);

#endif /* NODE_H_ */
