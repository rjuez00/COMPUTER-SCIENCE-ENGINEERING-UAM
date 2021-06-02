
#ifndef HASH_H
#define HASH_H

#include "types.h"

/*Structs*/
typedef struct _HashTable HashTable;
typedef struct _DataItem DataItem;

/*Hash table functions*/
HashTable *HashTable_new(int size);
void HashTable_free(HashTable *hashTable);
Status HashTable_insert(HashTable *table, char *key, int data, short elementcategory, short type, short category);
Status HashTable_delete(HashTable *table, char *key);
/*
INT_MIN error
INT_MAX if not found
*/
DataItem* HashTable_search(HashTable *table, char *key);
void HashTable_display(HashTable* table);

/* DataItem functions
return INT_MIN if errors
*/
char* DataItem_get_key(DataItem * item); 
int DataItem_get_value(DataItem * item);
int DataItem_get_element_category(DataItem * item);
int DataItem_get_type(DataItem * item);
int DataItem_get_category(DataItem * item);

#endif