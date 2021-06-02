#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H

#include "hash.h"

typedef struct _SymbolTable SymbolTable;

SymbolTable* SymbolTable_new();
void SymbolTable_free(SymbolTable* table);
Status SymbolTable_to_global(SymbolTable* table);
Status SymbolTable_to_local(SymbolTable* table, char* namefunction, int value, short type, short category, short num_params, short pos_param, short num_local_variables, short pos_local_variables);
Status SymbolTable_add(SymbolTable * table, char* symbol, int value, short elementcategory, short type, short category,
                       short num_params, short pos_param, short num_local_variables,
                       short pos_local_variables);
DataItem* SymbolTable_get(SymbolTable * table, char* symbol);
void SymbolTable_display(SymbolTable* table);


#endif