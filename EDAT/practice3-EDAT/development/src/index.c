#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "index.h"

struct index_ {
  record_t** records;
  int n_records;
  char *path;
  type_t type;
};

struct record_{
  long* pos;
  int n_pos;
  int key;
  char *keystring;
    /*The best option would be to implement the key with a void pointer
    the problem is we would have to modify the arguments of index_put and then the main for ints would not 
    work so we do this as a workaround and to interfere the least in the main practice which is the one which
    will be graded the most*/
};

int record_bin_search(record_t** records, int n_records, int key, int *ppos);
int record_bin_search_string(record_t** records, int n_records, char* key, int *ppos);
record_t* create_record(int key, long firstpos);
record_t* create_record_string(char* key , long firstpos);

/* 
   Function: int index_create(char *path, int type)

   Creates a file for saving an empty index. The index is initialized
   to be of the specific type (in the basic version this is always INT)
   and to contain 0 entries.

   Parameters:
   path:  the file where the index is to be created
   type:  the type of the index (always INT in this version)

   Returns:
   1:   index created
   0:   parameter error or file creation problem. Index not created.
 */

int index_create(char *path, type_t type) {

  FILE* file = NULL;
  short flag=0; int cero = 0;
  if(!path) return 0;
  
  file = fopen(path, "w");
  if(!file) return 0;

  flag = fwrite(&type, sizeof(int), 1, file);
  if(flag<1) {fclose(file);
                  return 0;}
  flag = fwrite(&cero, sizeof(int), 1, file);
  if(flag<1) {fclose(file);
                  return 0;}
  fclose(file);
  return 1;
} /*adapted*/



/* 
   Opens a previously created index: reads the contents of the index
   in an index_t structure that it allocates, and returns a pointer to
   it (or NULL if the files doesn't exist or there is an error). 

   NOTE: the index is stored in memory, so you can open and close the
   file in this function. However, when you are asked to save the
   index, you will not be given the path name again, so you must store
   in the structure either the FILE * (and in this case you must keep
   the file open) or the path (and in this case you will open the file
   again).

   Parameters:
   path:  the file where the index is 

   Returns:
   pt:   index opened
   NULL: parameter error or file opening problem. Index not opened.

 */
index_t* index_open(char* path) {
  int flag=0, i, length;
  index_t* idx = NULL;
  FILE *file =NULL;
  
  if(!path) return NULL;
  
  idx = (index_t*)malloc(sizeof(index_t));
  if(!idx) return NULL;
  idx->path = path;

  file = fopen(path, "r");
  if(!file) {free(idx); return NULL;}

  flag = fread(&(idx->type), sizeof(type_t), 1, file);
  if(flag<0){
        fclose(file);
        free(idx);
        return NULL;
  }
  flag = fread(&(idx->n_records), sizeof(int), 1, file);
  if(flag<0){
        fclose(file);
        free(idx);
        return NULL;
  }

  idx->records=NULL;
  idx->records = (record_t**)malloc(sizeof(record_t*) * idx->n_records);
  if(!idx->records) {free(idx); return NULL;}

  for(i=0; i<idx->n_records; i++){
    if(idx->type == STR){
      idx->records[i]=NULL;
      idx->records[i] = (record_t*)malloc(sizeof(record_t));
      if(!idx->records[i]) {free(idx);  free(idx->records); return NULL;}
      
      flag = fread(&(length), sizeof(int), 1, file);
      if(flag<0){
            fclose(file);
            free(idx);
            return NULL;
      }
      idx->records[i]->key = -1;
      idx->records[i]->keystring = (char*)malloc(sizeof(char)*length);
      flag = fread(idx->records[i]->keystring, sizeof(char), length, file);
      if(flag<0){
            fclose(file);
            free(idx);
            return NULL;
      }

      idx->records[i]->n_pos = 0;
      flag = fread(&(idx->records[i]->n_pos), sizeof(int), 1, file);
      if(flag<0){
            fclose(file);
            free(idx);
            return NULL;
      }

      idx->records[i]->pos = (long*) malloc (sizeof(long)*(idx->records[i]->n_pos));
      flag = fread(idx->records[i]->pos, sizeof(long), idx->records[i]->n_pos, file);
      if(flag<0){
            fclose(file);
            free(idx);
            return NULL;
      }
    }


    if(idx->type == INT){  
      idx->records[i]=NULL;
      idx->records[i] = (record_t*)malloc(sizeof(record_t));
      if(!idx->records[i]) {free(idx);  free(idx->records); return NULL;}
      
      idx->records[i]->keystring=NULL;
      idx->records[i]->key = 0;
      flag = fread(&(idx->records[i]->key), sizeof(int), 1, file);
      if(flag<0){
            fclose(file);
            free(idx);
            return NULL;
      }

      idx->records[i]->n_pos = 0;
      flag = fread(&(idx->records[i]->n_pos), sizeof(int), 1, file);
      if(flag<0){
            fclose(file);
            free(idx);
            return NULL;
      }

      idx->records[i]->pos = (long*) malloc (sizeof(long)*(idx->records[i]->n_pos));
      flag = fread(idx->records[i]->pos, sizeof(long), idx->records[i]->n_pos, file);
      if(flag<0){
            fclose(file);
            free(idx);
            return NULL;
      }
    }
  }
  


  fclose(file);
  return idx;
} /*adapted*/


/* 
   int index_save(index_t* index);

   Saves the current state of index in the file it came from. Note
   that the name of the file in which the index is to be saved is not
   given.  See the NOTE to index_open.  

   Parameters:
   index:  the index the function operates upon

   Returns:
   1:  index saved
   0:  error saving the index (cound not open file)

*/
int index_save(index_t* idx) {
  FILE *file=NULL;
  int flag=0, i, length = 0;
  if(!idx) return 0;
  if(!(idx->path)) return 0;

  file = fopen(idx->path, "w");

  flag = fwrite(&(idx->type), sizeof(type_t), 1, file); 
  if(flag<1) {fclose(file);printf("ERROR");
              return 0;}
  flag = fwrite(&(idx->n_records), sizeof(int), 1, file); 
  if(flag<1) {fclose(file);printf("ERROR");
              return 0;}
  for(i=0; i<idx->n_records; i++){
    if(idx->type == STR){
      length = strlen(idx->records[i]->keystring) +1;

      flag = fwrite(&(length), sizeof(int), 1, file); 
      if(flag<1) {fclose(file);printf("ERROR");
                return 0;}
      flag = fwrite((idx->records[i]->keystring), sizeof(char), length, file); 
      if(flag<1) {fclose(file);printf("ERROR");
                return 0;}
      
      flag = fwrite(&(idx->records[i]->n_pos), sizeof(int), 1, file); 
      if(flag<1) {fclose(file);printf("ERROR");
                return 0;}
      flag = fwrite(idx->records[i]->pos, sizeof(long), idx->records[i]->n_pos, file); 
      if(flag<1) {fclose(file); printf("ERROR");
                  return 0;}
    }


    if(idx->type == INT){
      flag = fwrite(&(idx->records[i]->key), sizeof(int), 1, file); 
      if(flag<1) {fclose(file);printf("ERROR");
                return 0;}
      
      flag = fwrite(&(idx->records[i]->n_pos), sizeof(int), 1, file); 
      if(flag<1) {fclose(file);printf("ERROR");
                return 0;}
      flag = fwrite(idx->records[i]->pos, sizeof(long), idx->records[i]->n_pos, file); 
      if(flag<1) {fclose(file); printf("ERROR");
                  return 0;}
    }
  }

  
  fclose(file);
  return 0;
} /*adapted*/


/* 
   Function: int index_put(index_t *index, int key, long pos);

   Puts a pair key-position in the index. Note that the key may be
   present in the index or not... you must manage both situation. Also
   remember that the index must be kept ordered at all times.

   Parameters:
   index:  the index the function operates upon
   key: the key of the record to be indexed (may or may not be already
        present in the index)
   pos: the position of the corresponding record in the table
        file. This is the datum that we will want to recover when we
        search for the key.

   Return:
   n>0:  after insertion the file now contains n unique keys
   0:    error inserting the key

*/
int index_put(index_t *idx, int key, long pos) {
  int flag=0;
  FILE *file=NULL;
  record_t* newrec=NULL;
  int i=0, index = 0, flag_found = 0;

  if(!idx || key < 0 || pos < 0) return 0;
  
  /*SEARCH FOR THE KEY WITH                BINARY_SEARCH*/
  flag_found = record_bin_search(idx->records, (idx->n_records), key, &index);

  if(flag_found == 1){
    idx->records[index]->pos = (long*)realloc(idx->records[index]->pos, (idx->records[index]->n_pos+1) * sizeof(long));
    idx->records[index]->pos[(idx->records[index]->n_pos)] = pos;
    idx->records[index]->n_pos++;

  }

  if(flag_found == 0){
    newrec = create_record(key, pos);
    if(!newrec) return 0;

    idx->n_records++;
    idx->records=(record_t**)realloc(idx->records, idx->n_records * sizeof(record_t*));
    if(!(idx->records)){
      idx->n_records--;
      return 0;
    }
    for(i = (idx->n_records - 2); i >= index; i--){
      idx->records[i+1]=idx->records[i];
    }

    idx->records[index] = newrec;
    if(index == idx->n_records-2 && idx->records[idx->n_records - 1]->key < newrec->key){
      idx->records[idx->n_records-2]=idx->records[idx->n_records-1];
      idx->records[idx->n_records-1]= newrec;
    }
  }


  return idx->n_records;
}

int index_put_string(index_t *idx, char* key, long pos) {
  int flag=0;
  FILE *file=NULL;
  record_t* newrec=NULL;
  int i=0, index = 0, flag_found = 0;

  if(!idx || !key || pos < 0) return 0;
  
  /*SEARCH FOR THE KEY WITH                BINARY_SEARCH*/
  flag_found = record_bin_search_string(idx->records, (idx->n_records), key, &index);

  if(flag_found == 1){
    idx->records[index]->pos = (long*)realloc(idx->records[index]->pos, (idx->records[index]->n_pos+1) * sizeof(long));
    idx->records[index]->pos[(idx->records[index]->n_pos)] = pos;
    idx->records[index]->n_pos++;

  }

  if(flag_found == 0){
    newrec = create_record_string(key, pos);
    if(!newrec) {return 0;}

    idx->n_records++;
    idx->records=(record_t**)realloc(idx->records, idx->n_records * sizeof(record_t*));
    if(!(idx->records)){
      idx->n_records--;
      return 0;
    }
    for(i = (idx->n_records - 2); i >= index; i--){
      idx->records[i+1]=idx->records[i];
    }

    idx->records[index] = newrec;
    if(index == idx->n_records-2 && idx->records[idx->n_records - 1]->key < newrec->key){
      idx->records[idx->n_records-2]= idx->records[idx->n_records-1];
      idx->records[idx->n_records-1]= newrec;
    }
  }


  return idx->n_records;
}



/* 
   Function: long *index_get(index_t *index, int key, int* nposs);

   Retrieves all the positions associated with the key in the index. 

   Parameters:
   index:  the index the function operates upon
   key: the key of the record to be searched
   nposs: output paramters: the number of positions associated to this key
   
   Returns:

   pos: an array of *nposs long integers with the positions associated
        to this key
   NULL: the key was not found   

   NOTE: the parameter nposs is not an array of integers: it is
   actually an integer variable that is passed by reference. In it you
   must store the number of elements in the array that you return,
   that is, the number of positions associated to the key. The call
   will be something like this:

   int n
   long **poss = index_get(index, key, &n);

   for (int i=0; i<n; i++) {
       Do something with poss[i]
   }

   ANOTHER NOTE: remember that the search for the key MUST BE DONE
   using binary search.

   FURTHER NOTE: the pointer returned belongs to this module. The
   caller guarantees that the values returned will not be changed.

*/
long *index_get(index_t *idx, int key, int* nposs) {
  int index, flag = 0;
  if(!idx || !nposs || key < 0) return NULL;

  flag = record_bin_search(idx->records, idx->n_records, key, &index);
  if (!flag) return NULL;

  *nposs = idx->records[index]->n_pos;

  return idx->records[index]->pos;
}

long *index_get_string(index_t *idx, char* key, int* nposs) {
  int index, flag = 0;
  if(!idx || !nposs || key < 0) return NULL;

  flag = record_bin_search_string(idx->records, idx->n_records, key, &index);
  if (!flag) return NULL;

  *nposs = idx->records[index]->n_pos;

  return idx->records[index]->pos;
}


/* 
   Closes the index by freeing the allocated resources. No operation
   on the index will be possible after calling this function. 

   Parameters:
   index:  the index the function operates upon

   Returns:
   Nothing

   NOTE: This function does NOT save the index on the file: you will
   have to call the function index_save for this.
*/
void index_close(index_t *idx) {
  int i;
  if(!idx) return;
  for(i=0; i< idx->n_records; i++){
    free(idx->records[i]->pos);
    if(idx->records[i]->keystring) free(idx->records[i]->keystring);
    free(idx->records[i]);
  }
  if(idx->records) free(idx->records);
  
  free(idx);
  return;
}


/*
  Function: long **index_get_order(index_t *index, int n, int* nposs);

  Function useful for debugging but that should not be used otherwise:
  returns the nth record in the index. DO NOT USE EXCEPT FOR
  DEBUGGING. The test program uses it.

   Parameters:
   index:  the index the function operates upon
   n: number of the record to be returned
   key: output parameter: the key of the record
   nposs: output parameter: the number of positions associated to this key
   
   Returns:

   pos: an array of *nposs long integers with the positions associated
        to this key
   NULL: the key was not found   


   See index_get for explanation on nposs and pos: they are the same stuff
*/
long *index_get_order(index_t *index, int n, int *key, int* nposs) {
  if(!index || !nposs || !key || n<0) return NULL;
  if(n > (index->n_records - 1)) return NULL;
  *nposs = index->records[n]->n_pos;
  *key = index->records[n]->key;
  return index->records[n]->pos;
}

long *index_get_order_string(index_t *index, int n, char **key, int* nposs) {
  if(!index || !nposs || n<0) return NULL;
  if(n > (index->n_records - 1)) return NULL;
  *nposs = index->records[n]->n_pos;
  *key = index->records[n]->keystring;
  return index->records[n]->pos;
}



/*AUXILIARY FUNCTIONS*/
  record_t* create_record(int key, long firstpos){
    record_t* newrecord = NULL;

    if(key <0 || firstpos < 0) return NULL;
    newrecord = (record_t*)malloc(sizeof(record_t));
    if(!newrecord) return NULL;
    newrecord->key = key;
    newrecord->keystring=NULL;
    newrecord ->n_pos = 1;
    newrecord->pos = (long*)malloc(sizeof(long));
    if(!(newrecord->pos)) {
      free(newrecord);
      return NULL;
    }
    *(newrecord->pos) = firstpos;
    return newrecord;
  }
  record_t* create_record_string(char* key , long firstpos){
    record_t* newrecord = NULL;

    if(key <0 || firstpos < 0) return NULL;
    newrecord = (record_t*)malloc(sizeof(record_t));
    if(!newrecord) return NULL;
    newrecord->key = -1;
    newrecord->keystring=key;
    newrecord ->n_pos = 1;
    newrecord->pos = (long*)malloc(sizeof(long));
    if(!(newrecord->pos)) {
      free(newrecord);
      return NULL;
    }
    *(newrecord->pos) = firstpos;
    return newrecord;
  }

  type_t index_get_type(index_t* idx){
    if(!idx) return -1;
    return idx->type;
  }

  /*RETURN:
    FOUND = 1
    NOT_FOUND = 0*/
  int record_bin_search(record_t** records, int n_records, int key, int *ppos){ 
    int m=0, BOs=0, F=0, n; 
    if(!records||n_records < 0||!ppos || key < 0){
      *ppos = -1;
      return 0;
    }
    n = n_records;
    n_records--;
    while (F<=n_records){
      m=(F+n_records)/2;
      if(records[m]->key == key) {*ppos=m; return 1;}
      else if (key < records[m]->key) n_records=m-1;
      else F=m+1;

    }
    *ppos = m;
    if(n != 0) if(records[m]->key < key) *ppos = m+1;
    return 0;
  }

  int record_bin_search_string(record_t** records, int n_records, char* key, int *ppos){ 
    int m=0, BOs=0, F=0, n; 
    if(!records||n_records < 0||!ppos || !key){
      *ppos = -1;
      return 0;
    }
    n = n_records;
    n_records--;
    while (F<=n_records){
      m=(F+n_records)/2;
      if(strcmp(records[m]->keystring, key) == 0) {*ppos=m; return 1;}
      else if (strcmp(key, records[m]->keystring) < 0) n_records=m-1;
      else F=m+1;

    }
    *ppos = m;
    if(n != 0) if((m==0 && (strcmp(records[m]->keystring, key) < 0)) || (strcmp(records[m]->keystring, key)<0)) *ppos = m+1;
    return 0;
  }