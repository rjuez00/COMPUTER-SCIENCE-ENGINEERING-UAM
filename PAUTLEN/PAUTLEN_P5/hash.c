#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>
#include "hash.h"

#define DEFAULT_SIZE 40

struct _DataItem {
    char *key;
    int data;
    
    short elementcategory; /* PARAMETERS, FUNCTION or VARIABLE*/
    short type; /* INT or BOOLEAN*/
    short size; /* size for VECTOR*/
    short category; /*VECTOR or SCALAR*/
    short num_params;
    short pos_param;
    short num_local_variables;
    /* if pos_local_variable is -1, it's a global
       variable. if it's more than 0, it's a
       local variable */
    short pos_local_variable;
    struct _DataItem* next;
};

struct _HashTable {
    DataItem **hashArray;
    int entries; //number of entries
    int size;    //physical size 
};

int hashCode(char *key, int size) {
    int i;
    unsigned int hash = 0;
    size_t length;

    length = strlen(key);

    for (i = 0; i < length; i++) {
        hash += key[i];
    }
    
    return hash % size;
}

DataItem *DataItem_new(char *key, int data, short elementcategory, short type, short category,
                       short num_params, short pos_param, short num_local_variables,
                       short pos_local_variables) {
    DataItem *new_data_item = NULL;
    char *new_key = NULL;
    size_t keylength = -1;
    if (!key) {
        fprintf(stderr, "key can't be null in DataItem_new\n");
        return NULL;
    }
    keylength = strlen(key);
    if (keylength <= 0) {
        fprintf(stderr, "key can't have size 0 or less in DataItem_new\n");
        return NULL;
    }

    new_data_item = (DataItem *)malloc(sizeof(DataItem));
    if (new_data_item == NULL)
        return NULL;

    new_key = (char *)malloc((strlen(key) + 1) * sizeof(char));
    if (new_key == NULL) {
        free(new_data_item);
        return NULL;
    }
    strncpy(new_key, key, keylength);
	new_key[keylength] = '\0';
    new_data_item->key = new_key;
    new_data_item->data = data;
    new_data_item->next = NULL;
    new_data_item->elementcategory = elementcategory;
    new_data_item->type = type;
    new_data_item->category = category;
    new_data_item->num_params = num_params;
    new_data_item->pos_param = pos_param;
    new_data_item->num_local_variables = num_local_variables;
    new_data_item->pos_local_variable = pos_local_variables;

    return new_data_item;
}

void DataItem_free(DataItem *data_item) {
	if(data_item)
	{
		free(data_item->key);
		free(data_item);
	}
}

HashTable *HashTable_new(int size) {
    HashTable *returnvalue = NULL;
    returnvalue = (HashTable *)malloc(sizeof(HashTable));
    if (!returnvalue) {
        fprintf(stderr, "Cant malloc HashTable in HashTable_new\n");
        return NULL;
    }
    returnvalue->size = size > 0 ? size : DEFAULT_SIZE;
    returnvalue->entries = 0;
    returnvalue->hashArray = NULL;
    returnvalue->hashArray = (DataItem **)calloc(sizeof(DataItem *), returnvalue->size);

    if (!returnvalue->hashArray) {
        fprintf(stderr, "Cant malloc hashArray in HashTable_new\n");
        free(returnvalue);
        return NULL;
    }
    return returnvalue;
}

void HashTable_free(HashTable *hashTable) {
    int i;
    DataItem* current;
    DataItem* next;

    if (!hashTable) {
        fprintf(stderr, "No hash table to free.\n");
        return;
    }

    for (i = 0; i < hashTable->size; i++) {
        if(hashTable->hashArray[i] == NULL) continue;
        current = hashTable->hashArray[i];
		while(current != NULL){
			next = current->next;
            DataItem_free(current);
			current = next;
        }
    }

    free(hashTable->hashArray);
    free(hashTable);
    return;
}


Status HashTable_insert(HashTable *table, char *key, int data, short elementcategory, short type, short category,
                       short num_params, short pos_param, short num_local_variables,
                       short pos_local_variables) {
    if (!table) {
        fprintf(stderr, "table is NULL in HashTable_insert\n");
        return ERROR;
    }
    if (!key) {
        fprintf(stderr, "key is NULL in HashTable_insert\n");
        return ERROR;
    }
    DataItem *item = DataItem_new(key, data, elementcategory, type, category, num_params,
                                  pos_param, num_local_variables, pos_local_variables);
    if (!item) {
        fprintf(stderr, "Can't malloc DataItem\n");
        return ERROR;
    }

    int hashIndex = hashCode(key, table->size);

    if(table->hashArray[hashIndex] == NULL){
        table->hashArray[hashIndex] = item;
        table->entries += 1;
    }
    else {
        DataItem* current = table->hashArray[hashIndex];
        
        for(; current != NULL ; current = current->next) {
            if(strcmp(current->key, key) == 0){
                DataItem_free(item);
                return ERROR;
            }
            if (current->next == NULL)
                break;
        }
        current->next = item;
    }
    return OK;
}


Status HashTable_delete(HashTable *table, char *key) {
    int hashIndex;
    DataItem* current = NULL;	
    
    if(!table){
        fprintf(stderr, "table is NULL in HashTable_delete\n");
        return ERROR;
    }
    if(!key){
        fprintf(stderr, "key is NULL in HashTable_delete\n");
        return ERROR;
    }
    
	hashIndex = hashCode(key, table->size);
    
	
	DataItem** before = &(table->hashArray[hashIndex]);
    for (current = table->hashArray[hashIndex]; current != NULL; before = &(current->next), current = current->next) {
        if (strcmp(current->key, key) == 0) {
			*before = current->next;
            DataItem_free(current);
            return OK;
        }
	}
    return ERROR;
}


DataItem* HashTable_search(HashTable *table, char *key) {
    int hashIndex;
	DataItem* current = NULL;
	if(!table || !key) {
		fprintf(stderr, "Error: the table or the key were NULL");
		return NULL;
	}
    
	hashIndex = hashCode(key, table->size);
	
    for(current = table->hashArray[hashIndex]; current != NULL; current = current->next) {
        if (strcmp(current->key, key) == 0)
            return current;
    }

    return NULL;
}

void DataItem_display(DataItem* item){
    if(!item) {
		fprintf(stderr, "item is NULL in DataItem_display");
		return;
	}
    printf("Key: %s, Value: %d, Type: %d, Category: %d, Element Category: %d\n", item->key, item->data, item->type, item->category, item->elementcategory);

}


void HashTable_display(HashTable* table) {
    if(!table) {
		fprintf(stderr, "table is NULL in HashTable_display");
		return;
	}
    DataItem* current = NULL;
	// printf("entramos al loop de size %d\n\n", table->size);
    for(int i = 0; i<table->size; ++i) {
        for(current = table->hashArray[i]; current != NULL; current = current->next)
            DataItem_display(current);
    }
    printf("\n");
}

char* DataItem_get_key(DataItem * item) {
	if(!item) return NULL;
	return item->key;
}

int DataItem_get_value(DataItem * item) {
	if(!item) return INT_MIN;
	return item->data;
}

int DataItem_get_element_category(DataItem * item) {
	if(!item) return INT_MIN;
	return item->elementcategory;
}

int DataItem_get_type(DataItem * item) {
	if(!item) return INT_MIN;
	return item->type;
}
int DataItem_get_category(DataItem * item) {
	if(!item) return INT_MIN;
	return item->category;
}

short DataItem_get_size(DataItem* item){
    return item->size;
}

short DataItem_get_num_params(DataItem * item) {
	return item->num_params;
}

short DataItem_get_pos_param(DataItem * item) {
	return item->pos_param;
}

short DataItem_get_num_local_variables(DataItem * item) {
	return item->num_local_variables;
}

short DataItem_get_pos_local_variable(DataItem * item) {
	return item->pos_local_variable;
}


void DataItem_set_size(DataItem* dataitem, short info){
    dataitem->size = info;
}

void DataItem_set_num_params(DataItem * item, short info) {
	item->num_params = info;
}

void DataItem_set_pos_param(DataItem * item, short info) {
	item->pos_param = info;
}

void DataItem_set_num_local_variables(DataItem * item, short info) {
	item->num_local_variables = info;
}

void DataItem_set_pos_local_variable(DataItem * item, short info) {
	item->pos_local_variable = info;
}