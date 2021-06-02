/**
 *
 * Descripcion: Header file for sorting functions 
 *
 * Fichero: sorting.h
 * Autor: Carlos Aguirre
 * Version: 1.0
 * Fecha: 16-09-2019
 *
 */

#ifndef ORDENACION_H
#define ORDENACION_H

/* constants */

#ifndef ERR
  #define ERR -1
  #define OK (!(ERR))
#endif

/* type definitions */
typedef int (* pfunc_sort)(int*, int, int);

/* Functions */

int InsertSort(int* table, int ip, int iu);
int InsertSortInv(int* table, int ip, int iu);
int selectsort(int* table, int ip, int iu);
int bubblesort(int* table, int ip, int iu);
int bubblesort_v2(int* table, int ip, int iu);


int MergeSort(int* T, int F, int L);
int quicksort(int* table, int ip, int iu);
int HeapSort(int* table, int ip, int iu);



int quicksort_inv(int* table, int ip, int iu);
int MergeSort_inv(int* table, int ip, int iu);
int introsort1(int* tabla, int ip,int iu);
int quicksort_src1(int* table, int ip, int iu);
int quicksort_src2(int* table, int ip, int iu);
int quicksort_src3(int* table, int ip, int iu);
#endif
