#ifndef NODE_H_
#define NODE_H_
#include <stdlib.h>
#include <stdio.h>
#include "types.h"

typedef struct _String String;

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "string.h"

void string_destroy(void *e);
void* string_copy(const void *e);
int string_print(FILE *pf, const void* e);
int string_cmp(const void *e1, const void *e2);

#endif /* STRING_H_ */
