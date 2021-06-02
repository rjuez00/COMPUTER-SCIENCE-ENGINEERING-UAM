/**
 *
 * Descripcion: Implementation of sorting functions
 *
 * Fichero: sorting.c
 * Autor: Carlos Aguirre
 * Version: 1.0
 * Fecha: 16-09-2019
 *
 */

#include "sorting.h"
#include <stdio.h>
#include <stdlib.h>

int merge(int *table, int ip, int iu, int imiddle);
void swap(int *a, int *b);
int median(int *table, int ip, int iu,int *pos);
int median_stat(int *table, int ip, int iu,int *pos);
int median_avg(int *table, int ip, int iu,int *pos);
int split(int* table, int ip, int iu,int *pos);
int split_avg(int* table, int ip, int iu,int *pos);
int split_stat(int* table, int ip, int iu,int *pos);
void min_max (int ip, int iu, int med, int* max, int* min);

/***************************************************/
/* Function: InsertSort    Date:                   */
/* Your comment                                    */
/***************************************************/
int InsertSort(int* table, int ip, int iu){
    
    int i, j, aux;
    int BOs=0;
    if(!table || ip < 0 || iu < 0 || ip > iu){
        printf("ERROR in InsertSort input");
        return ERR;
    }

    for(i = ip+1; i <= iu; i++){
      aux = table[i];
      for(j = i-1; j >= ip; j--){
        BOs++;
        if(table[j]>aux){
          table[j+1]=table[j]; 
        } else {break;}
      }

      table[j+1]=aux;

    }

    return BOs;
}

int InsertSortInv(int* table, int ip, int iu){
    int i, j, aux;
    int BOs=0;
    if(!table || ip < 0 || iu < 0 || ip > iu){
        printf("ERROR in InsertSort input");
        return ERR;
    }
    for(i = ip+1; i <= iu; i++){
      aux = table[i];
      for(j = i-1; j >= ip; j--){
        BOs++;
        if(table[j]<aux){
          table[j+1]=table[j]; 
        } else {break;}
      }
      table[j+1]=aux;
    }
    return BOs;
}

int MergeSort(int* table, int ip, int iu){
  int imiddle, OBs=0;
  if(ip>iu||!table) return ERR;
  if(ip==iu) return OK;
  else{
    imiddle=(ip+iu)/2; /*we don't use the floor function because as we're dividing ints it automatically rounds down the int*/
    OBs+=MergeSort(table, ip, imiddle);

    OBs+=MergeSort(table,imiddle+1,iu);
    
    return merge(table,ip ,iu ,imiddle) + OBs;
  }

}

int merge(int *table, int ip, int iu, int imiddle){
  int* tableAux = NULL; 
  int i = ip, j = (imiddle+1), k = 0, BOs=0;
  if(!table || ip>imiddle || imiddle>iu) return ERR;
  tableAux=(int*)malloc(sizeof(int)*(iu-ip+1));
  if(!tableAux) return ERR;

  while(i <= imiddle && j <= iu){
    BOs++;
    if(table[i] < table[j]){
      tableAux[k] = table[i];
      k++; i++;  
    }

    else{
      tableAux[k] = table[j];
      k++; j++;
    }
  }

  while(i <= imiddle){
    tableAux[k] = table[i];
    k++; i++;
  }

  while(j <= iu){
    tableAux[k] = table[j];
    k++; j++;
  }

  for(i=ip, k=0; i <= iu; i++, k++) table[i] = tableAux[k];

  free(tableAux);
  return BOs;
}




int quicksort(int* table, int ip, int iu){
  int pos, BOs=0;

  if(!table || ip>iu){return ERR;}


  BOs += split_stat(table, ip, iu, &pos);
  BOs += quicksort(table, ip, pos-1);
  BOs += quicksort(table, pos+1, iu);
  

  return BOs;
}


int split(int* table, int ip, int iu, int *pos){

  int i, k=0, BOs=0;
  
  if(!table || ip<0 || pos==NULL){return ERR;}
  BOs+=median(table, ip, iu, pos);
  k=table[*pos];
  swap(&table[ip], &table[(*pos)]);
  (*pos)=ip;
  for(i=ip; i<=iu ; i++){
    if(BOs++, table[i]<k){
      (*pos)++;
      swap(&table[(*pos)], &table[i]);
    }
  }
  swap(&table[ip], &table[*pos]);

  return BOs;
}

int split_avg(int* table, int ip, int iu, int *pos){

  int i, k=0, BOs=0;
  
  if(!table || ip<0 || pos==NULL){return ERR;}
  BOs+=median_avg(table, ip, iu, pos);
  k=table[*pos];
  swap(&table[ip], &table[(*pos)]);
  (*pos)=ip;
  for(i=ip; i<=iu ; i++){
    if(BOs++, table[i]<k){
      (*pos)++;
      swap(&table[(*pos)], &table[i]);
    }
  }
  swap(&table[ip], &table[*pos]);

  return BOs;
}

int split_stat(int* table, int ip, int iu, int *pos){

  int i, k=0, BOs=0;
  
  if(!table || ip<0 || pos==NULL){return ERR;}
  BOs+=median_stat(table, ip, iu, pos);
  k=table[*pos];
  swap(&table[ip], &table[(*pos)]);
  (*pos)=ip;
  for(i=ip; i<=iu ; i++){
    if(BOs++, table[i]<k){
      (*pos)++;
      swap(&table[(*pos)], &table[i]);
    }
  }
  swap(&table[ip], &table[*pos]);

  return BOs;
}


int median(int *table, int ip, int iu,int *pos){
  
  if(ip>iu || !table || !pos) return ERR;
  *pos = ip;
  
  return 0;
}

int median_avg(int *table, int ip, int iu,int *pos){
  if(ip>iu || !table || !pos) return ERR;
  *pos = (ip+iu)/2;

  return 0;
}

int median_stat(int *table, int ip, int iu,int *pos){
  int med, BOs=0; /*CAMBIAR EL median_stat y tiene que devolver 3 BOs*/
  int max=0, min=0;
  if(ip>iu || !table || !pos) return ERR;
  med = (ip+iu)/2;

  min_max(table[ip], table[iu], table[med], &max, &min);

  if(BOs++, table[ip] != max && table[ip] != min){
    *pos = ip;
  } /*one BO*/
  else if(BOs++, table[iu] != max && table[iu] != min){
    *pos = ip;
  } /*two BO*/
  
  else {BOs++; (*pos) = med;} /*although we don't do a comparison here 
                              the equivalent for min_max should be 3 
                              so i add a BO*/

                       
  return 3;
}


void swap(int *a, int *b){
  int aux;
  aux=*b;
  *b=*a;
  *a=aux;  
}


void min_max (int ip, int iu, int med, int* max, int* min){
  if (!max || !min) return;
  
  if(ip > iu && ip > med){ *max = ip;}
  else if (iu > ip && iu > med) {*max = iu;}
  else {*max = med;}

  if(ip < iu && ip < med){ *min = ip;}
  else if (iu < ip && iu < med) {*min = iu;}
  else {*min = med;}
}