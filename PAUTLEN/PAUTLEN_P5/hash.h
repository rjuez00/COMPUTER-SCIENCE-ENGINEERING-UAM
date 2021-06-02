
#ifndef HASH_H
#define HASH_H

#include "alfa.h"

/*Structs*/
typedef struct _HashTable HashTable;
typedef struct _DataItem DataItem;


typedef enum {
    ERROR = 0,
    OK = 1
} Status;

/*Hash table functions*/
HashTable *HashTable_new(int size);
void HashTable_free(HashTable *hashTable);
Status HashTable_insert(HashTable *table, char *key, int data, short elementcategory, short type, short category,
                       short num_params, short pos_param, short num_local_variables,
                       short pos_local_variables);
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

short DataItem_get_size(DataItem* item);
short DataItem_get_num_params(DataItem * item);
short DataItem_get_pos_param(DataItem * item);
short DataItem_get_num_local_variables(DataItem * item);
short DataItem_get_pos_local_variable(DataItem * item);
void DataItem_set_size(DataItem* dataitem, short info);
void DataItem_set_num_params(DataItem * item, short info);
void DataItem_set_pos_param(DataItem * item, short info);
void DataItem_set_num_local_variables(DataItem * item, short info);
void DataItem_set_pos_local_variable(DataItem * item, short info);



#endif