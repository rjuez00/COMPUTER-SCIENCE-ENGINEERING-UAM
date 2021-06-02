#ifndef NEWSTATE_H
#define NEWSTATE_H

#include "afnd.h"
#include "types.h"

typedef struct _NewState NewState;


NewState* NewState_create(BOOL inicial, int* nd_states, int length, AFND* old_afnd);
BOOL compare_NewState(NewState* state, NewState* state2);
void NewState_destroy(NewState* state);
char* NewState_getname(NewState* state);
int* NewState_getstates(NewState* state);
int NewState_getstateslen(NewState* state);
int NewState_gettype(NewState* state);


#endif /* NEWSTATE */
