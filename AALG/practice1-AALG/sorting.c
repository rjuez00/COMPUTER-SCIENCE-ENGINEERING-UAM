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

/***************************************************/
/* Function: SelectSort    Date:                   */
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


