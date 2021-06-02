/**
 *
 * Descripcion: Implementation of time measurement functions
 *
 * Fichero: times.c
 * Autor: Carlos Aguirre Maeso
 * Version: 1.0
 * Fecha: 16-09-2019
 *
 */


#define _POSIX_C_SOURCE 199309L

#include "times.h"
#include "permutations.h"
#define CLOCK_REALTIME 0
#define BILLION  1000000000
#define MAX_INT 2147483647
#define MAX_CHAR 100

/*SIZES OF TABLES: */
#define SPACE_N 6
#define SPACE_OBS 



/***************************************************/
/* Function: average_sorting_time Date:            */
/*                                                 */
/* Your documentation                              */
/***************************************************/

void free_matrix(int** matrix, int sizea){
  int i=0;
  for(i=0; i<sizea; i++){
          free(matrix[i]);
        } 
  free(matrix);
}

void print_time_aa(PTIME_AA timestruct){
  if(!timestruct) return;
  printf("N: %d  \nn_elems: %d\ntime: %f\naverage OB: %f\nMin OB: %d\nMax OB: %d", timestruct->N, timestruct->n_elems, timestruct->time, timestruct->average_ob, timestruct->min_ob, timestruct->max_ob);
}

short average_sorting_time(pfunc_sort method,
                              int n_perms,
                              int N, 
                              PTIME_AA ptime)
{
  int i, OBs=0;
  int **permutations=NULL;
  struct timespec start, end;
  long seconds, nanoseconds;
  double time=0, totalOBs=0;

  if(!method || !ptime || n_perms < 1 || N < 1) return ERR;

  permutations = generate_permutations(n_perms, N);
  if(!permutations) return ERR;
  ptime->N=N;
  ptime->n_elems=n_perms;
  
  ptime->min_ob=MAX_INT;

  for(i=0; i<n_perms; i++){

    if(clock_gettime(CLOCK_REALTIME, &start)==ERR){
      free_matrix(permutations, n_perms);
      permutations=NULL;  
      return ERR;
    }

    OBs=method(permutations[i], 0, N-1);
    if(OBs==ERR) {
      free_matrix(permutations, n_perms);
      permutations=NULL;
      return ERR;
    } 


    if(OBs>(ptime->max_ob)) ptime->max_ob=OBs;
    if(OBs<(ptime->min_ob)) ptime->min_ob=OBs;
    totalOBs+=OBs;
    OBs=0;

    if(clock_gettime(CLOCK_REALTIME, &end)==ERR){
      free_matrix(permutations, n_perms);
      permutations=NULL;  
      return ERR;
    }

    seconds = end.tv_sec - start.tv_sec; 
    nanoseconds = end.tv_nsec - start.tv_nsec; 
    
    if (start.tv_nsec > end.tv_nsec) { 
	    --seconds; 
	    nanoseconds += 1000000000; 
    } 
    time+=seconds;
    time+=(float)nanoseconds/BILLION;

    
  }
    time=time/(double)n_perms;
    totalOBs=totalOBs/(double)n_perms;
    ptime->time=time;
    ptime->average_ob=totalOBs;



  free_matrix(permutations, n_perms);
  permutations=NULL;  
  return OK;
}

/***************************************************/
/* Function: generate_sorting_times Date:          */
/*                                                 */
/* Your documentation                              */
/***************************************************/
short generate_sorting_times(pfunc_sort method, char* file, 
                                int num_min, int num_max, 
                                int incr, int n_perms)

{
  int i=0, arraylenth=0, size_permutation=0;
  PTIME_AA times_array = NULL;

  if(!method || !file || num_min < 1 || num_max < num_min || incr < 0 || n_perms < 1) return ERR;
  
  if(incr != 0) for(i=num_min; i<=num_max; i+=incr) arraylenth++;
  else arraylenth = num_max - num_min + 1;

  size_permutation = num_min;

  times_array = (PTIME_AA)malloc(sizeof(TIME_AA)*arraylenth);
  if(!times_array) return ERR;
  /*INITIALIZE ARRAY*/
  for(i=0; i<arraylenth; i++){
    times_array[i].N = 0;
    times_array[i].n_elems = 0;
    times_array[i].time = 0;
    times_array[i].average_ob = 0;
    times_array[i].max_ob = 0;
    times_array[i].min_ob = MAX_INT;
  }
  
  for(i=0; i<arraylenth; i++){
    if(size_permutation > num_max){
      free(times_array);
      times_array = NULL;
      return ERR;
    }

    if(average_sorting_time(method, n_perms, size_permutation, &(times_array[i])) == ERR) {
      free(times_array);
      return ERR;
    };
    size_permutation += incr;
  
  }
 

  save_time_table(file, times_array, arraylenth);

  
  free(times_array);
  return OK;
}

/***************************************************/
/* Function: save_time_table Date:                 */
/*                                                 */
/* Your documentation                              */
/***************************************************/

/*N average_clock_time, average_ob, max_ob, min_ob*/
short save_time_table(char* file, PTIME_AA ptime, int n_times)
{
  FILE *save = NULL;
  int i=0, space_n, space_obs, n_calculator=0, ob_calculator=0, total=0;
  char buffer[MAX_CHAR];
  
  if(!file || !ptime || n_times < 1) return ERR;
  save = fopen(file,"w");
  if(!save) return ERR;
  
  for(i=0; i<n_times; i++){
    if(n_calculator < ptime[i].N) n_calculator = ptime[i].N;
    if(ob_calculator < ptime[i].max_ob) ob_calculator = ptime[i].max_ob;
  }
  /*calculate space for N*/
  for(space_n=0; n_calculator != 0; space_n++) n_calculator = n_calculator/10;
  space_n++;
  /*calculate space for OBs*/
  for(space_obs=0; ob_calculator != 0; space_obs++) ob_calculator = ob_calculator/10;
  space_obs++;

  if(space_obs<6) space_obs=6;
  fprintf(save, "\n");
  /*HEATHER*/
    sprintf(buffer, "|N");
    total+=2;
    total = strlen(buffer);
    while(strlen(buffer)<space_n){
      strcat(buffer, " ");
      total++;
    }
    strcat(buffer, "|");
    total++;
    fputs(buffer, save);

    sprintf(buffer, "clock_time");
    strcat(buffer, "|");
    total+=11;
    fputs(buffer, save);  

    sprintf(buffer, "AVERAGE_OB");
    total += 10;
    while(strlen(buffer)<(space_obs+6)){
      strcat(buffer, " ");
      total++;
    }
    strcat(buffer, "|");
    total++;
    fputs(buffer, save);

    sprintf(buffer, "MAX_OB");
    total += 6;
    while(strlen(buffer)<(space_obs)){
      strcat(buffer, " ");
      total++;
    }
    strcat(buffer, "|");
    total++;
    fputs(buffer, save);

    sprintf(buffer, "MIN_OB");
    total += 6;
    while(strlen(buffer)<(space_obs)){
      strcat(buffer, " ");
      total++;
    }
    strcat(buffer, "|\n");
    total++;
    fputs(buffer, save);





  /*DIVISOR*/
    for(i=0; i<total; i++){
      fprintf(save, "_");
    }
    fprintf(save, "\n");

  
  for(i=0; i<n_times; i++){
    /*N:*/
    sprintf(buffer, "|%d", ptime[i].N);
    while(strlen(buffer)<space_n){
      strcat(buffer, " ");
    }
    strcat(buffer, "|");
    fputs(buffer, save);

    /*AVERAGE_CLOCK_TIME*/
    sprintf(buffer, "%f  ", ptime[i].time);
    strcat(buffer, "|");
    fputs(buffer, save);

    /*AVERAGE_OB*/
    sprintf(buffer, "%f", ptime[i].average_ob);
    while(strlen(buffer)<(space_obs+6)){
      strcat(buffer, " ");
    }
    strcat(buffer, "|");
    fputs(buffer, save);

    /*MAX_OB*/
    sprintf(buffer, "%d", ptime[i].max_ob);
    while(strlen(buffer)<space_obs){
      strcat(buffer, " ");
    }
    strcat(buffer, "|");
    fputs(buffer, save);

    /*MIN_OB*/
    sprintf(buffer, "%d", ptime[i].min_ob);
    while(strlen(buffer)<space_obs){
      strcat(buffer, " ");
    }
    strcat(buffer, "|\n");
    fputs(buffer, save);



  }
  /*DIVISOR*/
    for(i=0; i<total; i++){
      fprintf(save, "¯");
    }
    fprintf(save, "\n");


  fclose(save);
  return OK;
}


short generate_search_times(pfunc_search method, pfunc_key_generator generator, 
                                int order, char* file, 
                                int num_min, int num_max, 
                                int incr, int n_times)
{
  int i=0, arraylenth=0, size_permutation=0;
  PTIME_AA times_array = NULL;

  if(!method || !file || num_min < 1 || num_max < num_min || incr < 0 || n_times < 1 || !generator) return ERR;
  
  if(incr != 0) for(i=num_min; i<=num_max; i+=incr) arraylenth++;
  else arraylenth = num_max - num_min + 1;

  size_permutation = num_min;

  times_array = (PTIME_AA)malloc(sizeof(TIME_AA)*arraylenth);
  if(!times_array) return ERR;
  /*INITIALIZE ARRAY*/
  for(i=0; i<arraylenth; i++){
    times_array[i].N = 0;
    times_array[i].n_elems = 0;
    times_array[i].time = 0;
    times_array[i].average_ob = 0;
    times_array[i].max_ob = 0;
    times_array[i].min_ob = MAX_INT;
  }
  
  for(i=0; i<arraylenth; i++){
    if(size_permutation > num_max){
      free(times_array);
      times_array = NULL;
      return ERR;
    }

    if(average_search_time(method, generator, order, size_permutation, n_times, &(times_array[i])) == ERR) {
      free(times_array);
      return ERR;
    };
    size_permutation += incr;
  
  }
 

  save_time_table(file, times_array, arraylenth);

  
  free(times_array);
  return OK;
}









short average_search_time(pfunc_search method, pfunc_key_generator generator,
                              int order,
                              int N, 
                              int n_times,
                              PTIME_AA ptime)
{
  PDICT pdict = NULL;
  int* perm = NULL;
  int* keys = NULL;
  struct timespec start, end;
  long seconds, nanoseconds;
  double time=0;
  int  bufferOBs = 0, i, ppos = 0;
  if(!method || !generator || (order != SORTED && order != NOT_SORTED) || N < 0 || n_times < 0 || !ptime) return ERR;
  /*PTIME INIT*/
    ptime->max_ob = 0; 
    ptime->min_ob = MAX_INT;
    ptime->average_ob = 0; 
    ptime->N = N;
    ptime->n_elems = N*n_times;
  
  pdict = init_dictionary(N, order);

  if(!pdict) return ERR;
  
  perm = generate_perm(N);
  if(!perm) {free_dictionary(pdict); return ERR;}
  
 
  
  if(massive_insertion_dictionary(pdict, perm, N) == ERR) {
    free_dictionary(pdict); 
    free(perm);
    return ERR;
  }
   
  keys = (int*)malloc(sizeof(int)*n_times*N);
  if(!keys){
    free_dictionary(pdict);
    free(perm);
    return ERR;
  }

  generator(keys, N*n_times, N);

  for (i = 0; i < N*n_times; i++){

    if(clock_gettime(CLOCK_REALTIME, &start)==ERR){
      printf("\nerror in clock function at start\n");
      free_dictionary(pdict); free(perm); free(keys);
      return ERR;
    }
    if(keys[i] > N){printf("el potential keys generator devuelve numeros mas grandes que el N que le damos");}
    bufferOBs = search_dictionary(pdict, keys[i], &ppos, method);
    if(ppos < 0 || bufferOBs < 0){
      printf("\nkey %i wasn't found\n", keys[i]);
      free_dictionary(pdict); free(perm); free(keys);
      return ERR;
    }
    if(clock_gettime(CLOCK_REALTIME, &end)==ERR){
      printf("\nerror in clock function at end\n");
      free_dictionary(pdict); free(perm); free(keys);
      return ERR;
    }
    ptime->average_ob += bufferOBs;
    if(ptime->max_ob < bufferOBs) ptime->max_ob = bufferOBs;
    if(ptime->min_ob > bufferOBs) ptime->min_ob = bufferOBs;
    seconds = end.tv_sec - start.tv_sec; 
    nanoseconds = end.tv_nsec - start.tv_nsec; 
    
    if (start.tv_nsec > end.tv_nsec) { 
	    --seconds; 
	    nanoseconds += 1000000000; 
    } 
    time+=seconds;
    time+=(float)nanoseconds/BILLION;
  
  
  }
  time = time/(double)(N*n_times);
  ptime->time = time;
  ptime->average_ob = ptime->average_ob/(N*n_times);
  free(perm); free(keys);
  free_dictionary(pdict);
  return OK;
}