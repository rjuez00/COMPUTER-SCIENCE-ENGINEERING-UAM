/**
 *
 * Descripcion: Header file for time measurement functions 
 *
 * Fichero: times.h
 * Autor: Carlos Aguirre.
 * Version: 1.0
 * Fecha: 15-09-2019
 *
 */

#ifndef TIEMPOS_H
#define TIEMPOS_H

/* constants */

#ifndef ERR
  #define ERR -1
  #define OK (!(ERR))
#endif


#include "sorting.h"
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

/* type definitions */
typedef struct time_aa {
  int N;           /* size of each element */
  int n_elems;     /* number of elements to average */
  double time;   /* average clock time */
  double average_ob; /* average number of times that the OB is executed */
  int min_ob;      /* minimum of executions of the OB */
  int max_ob;      /* maximum of executions of the OB */
} TIME_AA, *PTIME_AA;


/* Functions */
short average_sorting_time(pfunc_sort method, int n_perms,int N, PTIME_AA ptime);
short generate_sorting_times(pfunc_sort method, char* file, int num_min, int num_max, int incr, int n_perms);
short save_time_table(char* file, PTIME_AA time, int n_times);

#endif
