#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "hash.h"


void HashTable_insert_b(HashTable* table, char* key, int value) {
    HashTable_insert(table, key, value, 0, 0, 0);
}

int main(int argc, char* argv[]){
    HashTable* table;
    
    table = HashTable_new(1);
    printf("---- Tabla Creada ----\n");

    HashTable_insert_b(table, "uno", 1);
    HashTable_insert_b(table, "dos", 2);
    HashTable_insert_b(table, "tres", 3);
    HashTable_insert_b(table, "cuatro", 4);
    HashTable_insert_b(table, "diez", 10);
    HashTable_insert_b(table, "dieziuno", 11);
    HashTable_insert_b(table, "once", 11);
    HashTable_insert_b(table, "once", 11);
    HashTable_insert_b(table, "once", 11);
    HashTable_insert_b(table, "doce", 12);
    printf("---- Elementos Insertados ----\n");

    HashTable_display(table);

    printf("uno is %d\n", DataItem_get_value(HashTable_search(table, "uno")));
    printf("dos is %d\n", DataItem_get_value(HashTable_search(table, "dos")));
    printf("dieziuno is %d\n", DataItem_get_value(HashTable_search(table, "dieziuno")));
    printf("once is %d\n", DataItem_get_value(HashTable_search(table, "once")));
    printf("unexistant doesnt exist: %s\n", HashTable_search(table, "unexistant") == NULL ? "true" : "false");
    printf("---- Búsquedas en tabla hechas ----\n");

    HashTable_delete(table, "cuatro");
    HashTable_delete(table, "once");
    HashTable_delete(table, "doce");
    
    printf("---- Eliminando Elementos ----\n");
    printf("once doesnt exist: %s\n", HashTable_search(table, "once") == NULL ? "true" : "false");

    HashTable_display(table);

    HashTable_free(table);
    printf("---- Tabla Liberada ----\n");

    return 0;
}