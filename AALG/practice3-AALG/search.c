/**
 *
 * Description: Implementation of functions for search
 *
 * File: search.c
 * Author: Carlos Aguirre and Javier Sanz-Cruzado
 * Version: 1.0
 * Date: 14-11-2016
 *
 */

#include "search.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "sorting.h"


/**
 *  Key generation functions
 *
 *  Description: Receives the number of keys to generate in the n_keys
 *               parameter. The generated keys go from 1 to max. The
 * 				 keys are returned in the keys parameter which must be 
 *				 allocated externally to the function.
 */
  
/**
 *  Function: uniform_key_generator
 *               This function generates all keys from 1 to max in a sequential
 *               manner. If n_keys == max, each key will just be generated once.
 */
void uniform_key_generator(int *keys, int n_keys, int max)
{
  int i;
  for(i = 0; i < n_keys; i++) {keys[i] = (i % max);}

  return;
}

/**
 *  Function: potential_key_generator
 *               This function generates keys following an approximately
 *               potential distribution. The smaller values are much more 
 *               likely than the bigger ones. Value 1 has a 50%
 *               probability, value 2 a 17%, value 3 the 9%, etc.
 */
void potential_key_generator(int *keys, int n_keys, int max)
{
  int i;

  for(i = 0; i < n_keys; i++) 
  {
    keys[i] = .5+max/(1 + max*((double)rand()/(RAND_MAX))) -1;
  }

  return;
}

PDICT init_dictionary (int size, char order)
{
  PDICT dict=NULL;
  if(size<=0 ||(order!=NOT_SORTED && order!=SORTED)){
    return NULL;
  }
  
  dict = (PDICT) malloc (sizeof(DICT));
  if(!dict) return NULL;
  dict->table = NULL;
  dict->table = (int*) malloc (size * sizeof(int));
  if(!dict->table) {
      free(dict);
      return NULL;
    }
  dict->order = order;;
  dict->size = size;
  dict->n_data = 0;
  
  return dict;
}

/*typedef struct dictionary {
  int size; 
  int n_data;
  char order;  
  int *table; 
} DICT, *PDICT;*/

void free_dictionary(PDICT pdict)
{
  if(!pdict) return;

  if(pdict->table) free((pdict->table));
  free(pdict);

}

int insert_dictionary(PDICT pdict, int key)
{ int i=0, OBs=1; /*this is for being able to have it in the while statement we correct it at the end with a -1*/
  if(!pdict) return ERR;
  pdict->table[pdict->n_data] = key;
  pdict->n_data++;

  if(pdict->order == NOT_SORTED) return 0;
  if(pdict->order == SORTED) {
    i=pdict->n_data -2;
    while(i>=0    &&   pdict->table[i] > key && OBs++){
      pdict->table[i+1]=pdict->table[i];
      i--;
    }  
    pdict->table[i+1]=key; 
    return --OBs;
  }
  
  return ERR;
}

int massive_insertion_dictionary (PDICT pdict,int *keys, int n_keys)
{
  int i, OBs=0, buffer=0;
  if(!pdict||!keys||n_keys<1){
    return ERR;
  }
  for(i=0; i<n_keys; i++) {
    buffer = insert_dictionary(pdict, keys[i]);
    if(buffer == ERR) return ERR;
    OBs += buffer;
  }

  return OBs;
  
}

int search_dictionary(PDICT pdict, int key, int *ppos, pfunc_search method)
{
	if(!pdict||!method||!ppos) return ERR;

  if(method==bin_search && pdict->order == NOT_SORTED){
    *ppos=ERR;
    return ERR;  
  }

  return method(pdict->table, 0, pdict->n_data-1 ,key, ppos);

  
}


/* Search functions of the Dictionary ADT only works with the table sorted*/
int bin_search(int *table,int F,int L,int key, int *ppos)
{ int m=0, BOs=0; 
	if(!table||F>L||!ppos){
    return ERR;
  }
  while (F<=L){
    BOs++;
    m=(F+L)/2;
    if(table[m]==key) {*ppos=++m; return BOs;}
    else if (key < table[m]) L=m-1;
    else F=m+1;

  }
  *ppos = NOT_FOUND;
  return NOT_FOUND;
}

int lin_search(int *table,int F,int L,int key, int *ppos)
{
  int i, BOs=0, flag;

  if(!table||F>L||!ppos){
    return ERR;
  }

  for(i=F, flag=0; i<=L && flag==0; i++){

    BOs++;
    if(table[i]==key){
      flag=1;
    }
  }
  
  if(flag==0) {*ppos = NOT_FOUND; 
               return NOT_FOUND;}
  else *ppos = i;

  return BOs;
}

int lin_auto_search(int *table,int F,int L,int key, int *ppos)
{
	int i, BOs=0, flag, aux;

  if(!table||F>L||!ppos){
    return ERR;
  }
  for(i=F, flag=0; i<=L && flag==0; i++){

    BOs++;
    if(table[i]==key){
      if(i==0){*ppos=++i; return BOs;}
      flag=1;
    }
  }
  i--; /*real index*/
  
  if(flag==0) {*ppos = NOT_FOUND; 
               return NOT_FOUND;}
  else {
    aux=table[i-1];
    table[i-1]=table[i];
    table[i]=aux;
    *ppos = i;} /*I return i and not i-1 becuase whe need to return it user friendly which would be the new index +1: i-1+1=i*/

  return BOs;
}

