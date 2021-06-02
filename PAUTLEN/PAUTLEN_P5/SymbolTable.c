#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>
#include "SymbolTable.h"
#define SIZEOFHASH 100


struct _SymbolTable{
    HashTable* global;
    HashTable* local;
};


SymbolTable* SymbolTable_new(){
    SymbolTable* returnvalue = NULL;
    returnvalue = (SymbolTable*)malloc(sizeof(SymbolTable));
    if(!returnvalue){
        fprintf(stderr, "cant malloc in SymbolTable_new\n");
        return NULL;
    }
    returnvalue->global = HashTable_new(SIZEOFHASH);
    if(!returnvalue->global){
        fprintf(stderr, "cant create HashTable global in SymbolTable_new\n");
        free(returnvalue);
        return NULL;
    }
    returnvalue->local = NULL;
    return returnvalue;
}


void SymbolTable_free(SymbolTable* table){
    if(!table) return;
    HashTable_free(table->global);
    if(table->local) HashTable_free(table->local);
    free(table);
}


Status SymbolTable_to_global(SymbolTable* table){
    if(!table){
        fprintf(stderr, "table cant be NULL in SymbolTable_to_global\n");
        return ERROR;
    }
    if(!table->local){
        fprintf(stderr, "you already are in global scope!\n");
        return ERROR;
    }
    HashTable_free(table->local);
    table->local = NULL;
    return OK;
}


Status SymbolTable_to_local(SymbolTable* table, char* namefunction, int value, short type, short category, short num_params, short pos_param, short num_local_variables,
                       short pos_local_variables){
    Status returnValue;
    if(!table){
        fprintf(stderr, "table cant be NULL in SymbolTable_to_local\n");
        return ERROR;
    }
    
    if(!namefunction){
        fprintf(stderr, "namefunction cant be NULL in SymbolTable_to_local\n");
        return ERROR;
    }

    if (value >= 0){
        fprintf(stderr, "value cant be positive when changing scope in SymbolTable_to_local\n");
        return ERROR;
    }

    if(table->local){
        fprintf(stderr, "you already are in local scope!\n");
        return ERROR;
    }
    table->local = HashTable_new(SIZEOFHASH);
    if(!table->local){
        fprintf(stderr, "error when malloc in SymbolTable_to_local\n");
        return ERROR;
    }
    
    returnValue = HashTable_insert(table->local, namefunction, value, FUNCTION, type, category, num_params, pos_param, num_local_variables, pos_local_variables);
    returnValue &= HashTable_insert(table->global, namefunction, value, FUNCTION, type, category, num_params, pos_param, num_local_variables, pos_local_variables);
    
    return returnValue;
}

Status SymbolTable_add(SymbolTable * table, char* symbol, int value, short elementcategory, short type, short category,
                       short num_params, short pos_param, short num_local_variables,
                       short pos_local_variables) {
    HashTable * which = NULL;
    if (!table) {
        fprintf(stderr, "Table can't be NULL in SymbolTable_add\n");
        return ERROR;
    }
    if (!symbol) {
        fprintf(stderr, "Symbol can't be NULL in SymbolTable_add\n");
        return ERROR;
    }
    
    which = table->local ? table->local : table->global;
    return HashTable_insert(which, symbol, value, elementcategory, type, category,
                            num_params, pos_param, num_local_variables,
                            pos_local_variables);
}


DataItem* SymbolTable_get(SymbolTable * table, char* symbol) {
    DataItem* local;
    if(!table){
        fprintf(stderr, "There is no table in SymbolTable_get\n");
        return NULL;
    }
    if(!symbol){
        fprintf(stderr, "There is no symbol in SymbolTable_get\n");
        return NULL;
    }

    if(table->local != NULL) {
        local = HashTable_search(table->local, symbol);
        if(local) return local;
    }
    
    return HashTable_search(table->global, symbol);
}


void SymbolTable_display(SymbolTable* table){
    if(!table){
        return;
    }
    HashTable_display(table->global);
    if(table->local) HashTable_display(table->local);
}




