// ----------- Arqo P4-----------------------
// pescalar_par1
// ¿Funciona correctamente?
//
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include "arqo4.h"

int main(int argc, char *argv[])
{
	int nproc;
	float *A=NULL, *B=NULL;
	long long k=0;
	struct timeval fin,ini;
	double sum=0;
    int sizearg=M;
       
	if(argc == 3){
		sizearg=atoll(argv[1]);
		nproc=atoi(argv[2]);
	}
	
	A = generateVectorOne(sizearg);
	B = generateVectorOne(sizearg);
	if ( !A || !B )
	{
		printf("Error when allocationg matrix\n");
		freeVector(A);
		freeVector(B);
		return -1;
	}
	
        omp_set_num_threads(nproc);   
     
        printf("Se han lanzado %d hilos.\n",nproc);

	gettimeofday(&ini,NULL);
	/* Bloque de computo */
	sum = 0;

	#pragma omp parallel if (M>8000000)
    #pragma omp parallel for reduction(+ : sum)
	for(k=0;k<sizearg;k++)
	{
		sum = sum + A[k]*B[k];
	}
	/* Fin del computo */
	gettimeofday(&fin,NULL);

	printf("Resultado: %f\n",sum);
	printf("Tiempo: %f\n", ((fin.tv_sec*1000000+fin.tv_usec)-(ini.tv_sec*1000000+ini.tv_usec))*1.0/1000000.0);
	freeVector(A);
	freeVector(B);

	return 0;
}
