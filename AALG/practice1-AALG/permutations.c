/**
 *
 * Descripcion: Implementation of function that generate permutations
 *
 * File: permutations.c
 * Autor: Carlos Aguirre
 * Version: 1.0
 * Fecha: 21-09-2019
 *
 */


#include "permutations.h"
#include <stdlib.h>
#include <stdio.h>


/***************************************************/
/* Function: random_num Date:                      */
/* Authors:                                        */
/*                                                 */
/* Rutine that generates a random number           */
/* between two given numbers                       */
/*                                                 */
/* Input:                                          */
/* int inf: lower limit                            */
/* int sup: upper limit                            */
/* Output:                                         */
/* int: random number                              */
/***************************************************/
int random_num(int inf, int sup)
{
  int x;
  double d;
  d=((double)rand())/((double)RAND_MAX + 1);
  x=(int)(sup-inf+1)*d;
  return (inf+x);
}


/***************************************************/
/* Function: generate_perm Date:                   */
/* Authors:                                        */
/*                                                 */
/* Rutine that generates a random permutation      */
/*                                                 */
/* Input:                                          */
/* int n: number of elements in the permutation    */
/* Output:                                         */
/* int *: pointer to integer array                 */
/* that contains the permitation                   */
/* or NULL in case of error                        */
/***************************************************/
int* generate_perm(int N)
{
  int i=0, swapindex=0, temp=0;
  int *permutations=NULL;
  permutations=(int*)malloc(sizeof(int)*N);
  if(!permutations) return NULL;
  
  for (i=0; i<N; i++){
    permutations[i]=i+1;
  }

  for (i=0; i<N; i++){
      /*SWAP*/
    swapindex=random_num(i,N-1);
    temp = permutations[swapindex];
    permutations[swapindex] = permutations[i];
    permutations[i] = temp;

  }

  return permutations;  

}



/***************************************************/
/* Function: generate_permutations Date:           */
/* Authors:                                        */
/*                                                 */
/* Function that generates n_perms random          */
/* permutations with N elements                    */
/*                                                 */
/* Input:                                          */
/* int n_perms: Number of permutations             */
/* int N: Number of elements in each permutation   */
/* Output:                                         */
/* int**: Array of pointers to integer that point  */
/* to each of the permutations                     */
/* NULL en case of error                           */
/***************************************************/
int** generate_permutations(int n_perms, int N)
{
  int i;
  int** matrixPerm=NULL;


  matrixPerm=(int**)malloc(sizeof(int*)*n_perms);
  if(!matrixPerm) return NULL;
  
  for(i=0;i<n_perms;i++){
    matrixPerm[i]=NULL;
    matrixPerm[i]=generate_perm(N);
    if(!matrixPerm[i]) return NULL;
  }
  
  return matrixPerm;
}
