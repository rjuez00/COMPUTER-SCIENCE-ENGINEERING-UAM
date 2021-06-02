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
#include <math.h>

int merge(int *table, int ip, int iu, int imiddle);

int median(int *table, int ip, int iu,int *pos);
int median_stat(int *table, int ip, int iu,int *pos);
int median_avg(int *table, int ip, int iu,int *pos);
int split(int* table, int ip, int iu,int *pos);
int split_avg(int* table, int ip, int iu,int *pos);
int split_stat(int* table, int ip, int iu,int *pos);

void swap(int *a, int *b);
void min_max (int ip, int iu, int med, int* max, int* min);
int max(int* table, int N, int i1, int i2, int i3);
int min(int* table, int ip, int iu, int* min);


/*AUX*/
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

  int min(int* table, int ip, int iu, int* min){
    int m = ip, i = ++ip, BOs=0;
    if(ip>iu||!table) return 0;
    if(ip==iu) return 0;
    
    while(i<=iu){
      if(table[i] < table[m]) m = i;
      i++;
    }
    *min=m;
    return BOs;
  }

  int max(int* table, int N, int i1, int i2, int i3){

    if(i1>=N) {
      if(table[i3]>table[i2]) return i3;
      else return i2;
    }

    if(i2>=N) {
      if(table[i1]>table[i3]) return i1;
      else return i3;
    }
    
    if(i3>=N) {
      if(table[i1]>table[i2]) return i1;
      else return i2;
    }
    
    if(table[i1]>table[i2] && table[i1]>table[i3]) return i1;
    if(table[i2]>table[i1] && table[i2]>table[i3]) return i2;
    if(table[i3]>table[i2] && table[i3]>table[i1]) return i3;
    return -1;
  }
/***************************************************/
/* Function: InsertSort    Date:                   */
/* Your comment                                    */
/***************************************************/
/*############ LOCAL ALGORITHMS ############*/
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

  int bubblesort(int* table, int ip, int iu){
    int i, j, BOs=0; 
    
    for(i=iu; i>ip; i--){ 
      for(j=ip; j<i; j++){ 
        if(table[j]>table[j+1]) swap(&table[j], &table[j+1]);
      }
    }
    return BOs;
  }/*BOs not done*/

  int bubblesort_v2(int* table, int ip, int iu){
    int flag = 1, i = iu, j, BOs=0;
    if(!table || ip>iu){return ERR;}

    while(flag == 1 && i > ip){
      flag = 0;
      
      for(j = ip; j<i; j++){
        if(table[j]>table[j+1]) {
          swap(&table[j], &table[j+1]);
          flag = 1;
        }
      }

      i--;
    }
    return BOs;
  }/*BOs not done*/

  int selectsort(int* table, int ip, int iu){
    int BOs = 0, i = ip, minim;
    if(ip>iu || !table || ip==iu) return -1;

    while(i<iu){
      BOs += min(table, i, iu, &minim); /*BOs not done*/
      if(BOs == ERR) return ERR;

      swap(&table[i], &table[minim]);
      i++;
    }
    return BOs;
  }/*BOs not done*/


/*############ MERGESORT ############*/
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
/*############ QUICKSORT ############*/
  int quicksort(int* table, int ip, int iu){
    int pos, BOs=0, buff=ERR;

    if(!table || ip>iu){return ERR;}


    BOs += split(table, ip, iu, &pos);
    if(ip<pos-1) {
      buff = quicksort(table, ip, pos-1);
      if(buff == ERR) return ERR;
      BOs+=buff;
    }
    
    if(pos+1<iu) {
      buff = quicksort(table, pos+1, iu);
      if(buff == ERR) return ERR;
      BOs+=buff;
    }
    

    return BOs;
  }

  int split(int* table, int ip, int iu, int *pos){

    int i, k=0, BOs=0;
    
    if(!table || ip<0 || pos==NULL){return ERR;}
    BOs+=median(table, ip, iu, pos);
    k=table[*pos];
    swap(&table[ip], &table[(*pos)]);
    (*pos)=ip;
    for(i=ip+1; i<=iu ; i++){
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
    for(i=ip+1; i<=iu ; i++){
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
    for(i=ip+1; i<=iu ; i++){
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
      *pos = iu;
    } /*two BO*/
    
    else {BOs++; (*pos) = med;}
    
    return 3;
  }


/*############ HEAPSORT ############*/
  int heapify(int* table, int N, int i){
    int ind = 0;
    while((2*i+2) <= N){
      ind = max(table, N, i, 2*i+1, 2*i+2);
      if(ind != i){
        swap(&table[i], &table[ind]);
        i=ind;
      }
      else return 0;
    }
    return 0;
  }

  int CreateHeap(int* table, int N){
    int i, j;
    if(!table) return ERR;
    if(N == 1) return 0;
    for(i=(N/2)-1; i>=0; i--){
      heapify(table, N, i);
      printf("\n");
      for(j=0; j<N; j++) printf("%i ", table[j]);
    }
    return 0;
  }

  int SortHeap (int* table, int N){
    int i, j;
    if(!table || N<0) return ERR;
    for(i=N-1; i>=1; i--){
      swap(&table[0], &table[i]);
      heapify(table, i, 0);
      printf("\n");
      for(j=0; j<N; j++) printf("%i ", table[j]);

    }
    return 0;
  }

  int HeapSort(int* table, int ip, int iu){
    int N;
    if(iu <ip||!table) {return -1;}

    N = iu-ip +1;
    CreateHeap(&(table[ip]), N);
    printf("\n");
    SortHeap(&(table[ip]), N);

    return 0;
  }/*BOs not done*/


/*############ QUICKSORT_INV ############*/
  int split_inv(int* table, int ip, int iu, int *pos){

    int i, k=0, BOs=0;
    
    if(!table || ip<0 || pos==NULL){return ERR;}
    BOs+=median(table, ip, iu, pos);
    k=table[*pos];
    swap(&table[ip], &table[(*pos)]);
    (*pos)=ip;
    for(i=ip+1; i<=iu ; i++){
      if(BOs++, table[i]>k){
        (*pos)++;
        swap(&table[(*pos)], &table[i]);
      }
    }
    swap(&table[ip], &table[*pos]);

    return BOs;
  }

  int split_avg_inv(int* table, int ip, int iu, int *pos){

    int i, k=0, BOs=0;
    
    if(!table || ip<0 || pos==NULL){return ERR;}
    BOs+=median_avg(table, ip, iu, pos);
    k=table[*pos];
    swap(&table[ip], &table[(*pos)]);
    (*pos)=ip;
    for(i=ip+1; i<=iu ; i++){
      if(BOs++, table[i]>k){
        (*pos)++;
        swap(&table[(*pos)], &table[i]);
      }
    }
    swap(&table[ip], &table[*pos]);

    return BOs;
  }

  int split_stat_inv(int* table, int ip, int iu, int *pos){

    int i, k=0, BOs=0;
    
    if(!table || ip<0 || pos==NULL){return ERR;}
    BOs+=median_stat(table, ip, iu, pos);
    k=table[*pos];
    swap(&table[ip], &table[(*pos)]);
    (*pos)=ip;
    for(i=ip+1; i<=iu ; i++){
      if(BOs++, table[i]>k){
        (*pos)++;
        swap(&table[(*pos)], &table[i]);
      }
    }
    swap(&table[ip], &table[*pos]);

    return BOs;
  }

  int quicksort_inv(int* table, int ip, int iu){
    int pos, BOs=0, buff=ERR;

    if(!table || ip>iu){return ERR;}


    BOs += split_inv(table, ip, iu, &pos);
    if(ip<pos-1) {
      buff = quicksort_inv(table, ip, pos-1);
      if(buff == ERR) return ERR;
      BOs+=buff;
    }
    
    if(pos+1<iu) {
      buff = quicksort_inv(table, pos+1, iu);
      if(buff == ERR) return ERR;
      BOs+=buff;
    }
    

    return BOs;
  }

/*############ INTROSORT ############*/
  int introsort(int* table, int ip, int iu, int prof){
    int pos, BOs=0, buff=ERR;
    if(!table || ip>iu){return ERR;}

    if(!prof) return MergeSort(table, ip, iu);
  

    BOs += split(table, ip, iu, &pos);
    if(ip<pos-1) {
      buff = introsort(table, ip, pos-1, --prof);
      if(buff == ERR) return ERR;
      BOs+=buff;
    }
  
    if(pos+1<iu) {
      buff = introsort(table, pos+1, iu, --prof);
      if(buff == ERR) return ERR;
      BOs+=buff;
    }
    return BOs;
  }

  int introsort1(int* tabla, int ip,int iu){
    return introsort(tabla, ip, iu, floor(log(iu-ip+1)/log(2)));
  }
/*############ MERGESORT_inv ############*/
  int merge_inv(int *table, int ip, int iu, int imiddle){
    int* tableAux = NULL; 
    int i = ip, j = (imiddle+1), k = 0, BOs=0;
    if(!table || ip>imiddle || imiddle>iu) return ERR;
    tableAux=(int*)malloc(sizeof(int)*(iu-ip+1));
    if(!tableAux) return ERR;

    while(i <= imiddle && j <= iu){
      BOs++;
      if(table[i] > table[j]){
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

  int MergeSort_inv(int* table, int ip, int iu){
    int imiddle, OBs=0;
    if(ip>iu||!table) return ERR;
    if(ip==iu) return OK;
    else{
      imiddle=(ip+iu)/2; /*we don't use the floor function because as we're dividing ints it automatically rounds down the int*/
      OBs+=MergeSort_inv(table, ip, imiddle);

      OBs+=MergeSort_inv(table,imiddle+1,iu);
      
      return merge_inv(table,ip ,iu ,imiddle) + OBs;
    }

  }
/*############ QS_tail ############*/
  int quicksort_src1(int* table, int ip, int iu){
    int im;
    if(!table || ip>iu){return ERR;}

    while(ip<iu) {
      split(table, ip, iu, &im);
      quicksort_src1(table, ip, im-1);
      ip = ++im;      
    }
    return OK;
  }

  int quicksort_src2(int* table, int ip, int iu){
    int im;
    if(!table || ip>iu){return ERR;}

    while(ip<iu) {
      split(table, ip, iu, &im);
      quicksort_src2(table, im+1, iu);
      iu = --im;      
    }
    return OK;
  }

  int quicksort_src3(int* table, int ip, int iu){
    int im;
    if(!table || ip>iu){return ERR;}
    
    while(ip<iu) {
      split(table, ip, iu, &im);
      
      if((iu-im) > (im-ip) ){
        printf("1");
        quicksort_src1(table, ip, im-1);
        ip = ++im;
      }
      
      else{
        printf("2");
        quicksort_src2(table, im+1, iu);
        iu = --im;      
      }
    }
    return OK;
  }