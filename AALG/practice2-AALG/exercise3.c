/**************************************************/
/* Program: exercise3       Date:                 */
/* Authors:                                       */
/*                                                */
/* Program that generates N random permutations   */
/* with M elemnts each                          */
/*                                                */
/* Input: Command line                            */
/* -size: number of elements in each permutation  */
/* -numP: number of permutations                  */
/* Output: 0: OK, -1: ERR                         */
/**************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "permutations.h"

int main(int argc, char** argv)
{
  int i;
  unsigned int n_perms, size, j, k;
  int** perms = NULL;

  srand(time(NULL));
  
  if (argc != 5) {
    fprintf(stderr, "Error in input parameters:\n\n");
    fprintf(stderr, "%s -size <int> -numP <int>\n", argv[0]);
    fprintf(stderr, "Where:\n");
    fprintf(stderr, " -size : number of elements in each permutation.\n");
    fprintf(stderr, " -numP : number of permutations.\n");
    exit(-1);
  }

  printf("Practice number 1, section 3\n");
  printf("Done by: your names\n");
  printf("Group: Your group\n");


  /* check command line */
  for(i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-size") == 0) {
      size = atoi(argv[++i]);
    } else if (strcmp(argv[i], "-numP") == 0) {
      n_perms = atoi(argv[++i]);
    } else {
      fprintf(stderr, "Wrong paramenter %s\n", argv[i]);
    }
  }

  perms = generate_permutations(n_perms, size);

  if (perms == NULL) { /* error */
    printf("Error: Out of memory\n");
    exit(-1);
  } else {
    for(j = 0; j < n_perms; j++) { /* for each permutation */
      for(k = 0; k < size; k++) {
        printf("%d ", perms[j][k]); /* print each element */
      }
      printf("\n");
      free(perms[j]); /* free permutation */
    }

    free(perms); /* free permutations array */
  }

  return 0;
}

