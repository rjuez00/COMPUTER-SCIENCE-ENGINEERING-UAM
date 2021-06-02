#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "arqo4.h"
#include <omp.h>


/*The function that prints the matrices. for debug purposes only.*/
void matrix_print(float** matrixA, int size){
    char temp[10];
    int i, j;

    /*Line at the top of the matrix. It is to make it look better.*/
    for(i=0; i<size; i++){
        printf("-------------");
    }
    printf("-");
    
    /*It displays the content of the matrix, separating it with |*/
    printf("\n");
    for(i=0; i<size; i++){
        printf("|");
        for(j=0; j<size; j++){
            sprintf(temp, "%f", matrixA[i][j]);
            printf(" %-10s |", temp);
        }
        printf("\n");
    }
    
    /*Line at the bottom of the matrix. It is to make it look better.*/
    for(i=0; i<size; i++){
        printf("-------------");
    }
    printf("-");
    
    printf("\n\n\n");
}

/*This function multiplies the matrices, wether they are using the normal or the transposed method.*/
double matrix_mult(float** matrixA, float** matrixB, int size, int transposed){
    int h, i, j;
    float** matrixC;
    float** matrixT;
    struct timeval start, end;
    double cpu_time_used;
    float sum;
    /*Error control in case one of the matrices does not exist.*/
    if(!matrixA || !matrixB){
        return -1.0;
    }

    /*We generate the result matrix.*/
    matrixC = generateEmptyMatrix(size);
    if(!matrixC) return -1.0;
    
    /*In case we will use the normal multiplication.*/
    if(transposed == 0){
        /*Measure time from here.*/
        gettimeofday(&start, NULL);

        /*We multiply row by column*/
        for(h = 0; h < size; h++){
            for(i = 0; i < size; i++){
                sum = 0.0;
                #pragma omp parallel for reduction(+ : sum)
                for(j = 0; j < size; j++){
                    sum += matrixA[j][h] * matrixB[i][j];
                }
                matrixC[i][h] = sum;
            } 
        }

        /*Measure time until here.*/
        gettimeofday(&end, NULL);
    } else {
        /*We create an intermediate matrix here.*/
        matrixT = generateEmptyMatrix(size);

        /*Measure time from here.*/
        gettimeofday(&start, NULL);

        /*We transpose the matrix and save it in matrixT.*/
        for(i=0; i<size; i++)
            for(j=0; j<size; j++)
                matrixT[i][j] = matrixB[j][i];
            
        /*We multiply row by row*/
        for(h = 0; h < size; h++)
            for(i = 0; i < size; i++){
                sum = 0.0;
                #pragma omp parallel for reduction(+ : sum)
                for(j = 0; j < size; j++){
                    sum += matrixA[h][j] * matrixT[i][j];
                }
                matrixC[i][h] = sum;
            } 

        /*Measure time until here.*/
        gettimeofday(&end, NULL);

        /*We free the transposed matrix, as it will not be used from here.*/
        freeMatrix(matrixT);
    }

    /*We convert the time to seconds.*/
    cpu_time_used = ((end.tv_sec  - start.tv_sec) * 1000000u + end.tv_usec - start.tv_usec) / 1.e6;

    /*We free the result matrix, because we do not need the result.*/
    freeMatrix(matrixC);

    return cpu_time_used;
}


int main( int argc, char *argv[]){
    float** matrixA;
    float** matrixB;
    double time;
    int matrixSize, nprocs=0;
    char flagTransposed = 0;
    
    if(argc < 3){
        printf("usage:\n%s <matrix_size> <threads> or\n%s <matrix_size> <threads> t (for transposed)\n", argv[0], argv[0]);
        return EXIT_FAILURE;
    }
    
    /*We convert the matrix size to an integer.*/
    matrixSize = atoi(argv[1]);
    nprocs = atoi(argv[2]);
    omp_set_num_threads(nprocs);   
    printf("Se han lanzado %d hilos.\n",nprocs);

    /*set flagTransposed to 1 in case we specified t in the arguments.*/
    if(argc == 4) flagTransposed = argv[3][0] == 't' ? 1 : 0;

    /*We create the two matrices*/
    matrixA = generateMatrix(matrixSize);
    matrixB = generateMatrix(matrixSize);
    
    /*We multiply the matrices.*/
    time = matrix_mult(matrixA, matrixB, matrixSize, flagTransposed);
    
    /*We free the matrices.*/
    freeMatrix(matrixA);
    freeMatrix(matrixB);
    
    /*We print the time*/
    printf("Tiempo %f\n", time);
    
    return EXIT_SUCCESS;
}