#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "arqo3.h"

/*The function that prints the matrices. for debug purposes only.*/
void matrix_print(tipo** matrixA, int size){
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
double matrix_mult(tipo** matrixA, tipo** matrixB, int size, int transposed){
    int h, i, j;
    tipo** matrixC;
    tipo** matrixT;
    clock_t start, end;
    double cpu_time_used;

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
        start = clock();

        /*We multiply row by column*/
        for(h = 0; h < size; h++)
            for(i = 0; i < size; i++){
                matrixC[i][h] = 0.0;
                for(j = 0; j < size; j++)
                    matrixC[i][h] += matrixA[j][h] * matrixB[i][j];
            } 
            
        /*Measure time until here.*/
        end = clock();
    } else {
        /*We create an intermediate matrix here.*/
        matrixT = generateEmptyMatrix(size);

        /*Measure time from here.*/
        start = clock();

        /*We transpose the matrix and save it in matrixT.*/
        for(i=0; i<size; i++)
            for(j=0; j<size; j++)
                matrixT[i][j] = matrixB[j][i];
            
        /*We multiply row by row*/
        for(h = 0; h < size; h++)
            for(i = 0; i < size; i++){
                matrixC[i][h] = 0.0;
                for(j = 0; j < size; j++)
                    matrixC[i][h] += matrixA[h][j] * matrixT[i][j];
            }
            
        

        /*Measure time until here.*/
        end = clock();

        /*We free the transposed matrix, as it will not be used from here.*/
        freeMatrix(matrixT);
    }

    /*We convert the time to seconds.*/
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    /*We free the result matrix, because we do not need the result.*/
    freeMatrix(matrixC);

    return cpu_time_used;
}


int main( int argc, char *argv[]){
    tipo** matrixA;
    tipo** matrixB;
    int matrixSize;
    double time;
    char flagTransposed = 0;
    
    /*We check if the number of arguments is correct and explain how to use it otherwise.*/
	if(argc < 2){
        printf("usage:\n%s <matrix_size> or\n%s <matrix_size> t (for transposed)\n", argv[0], argv[0]);
        return EXIT_FAILURE;
    }
    
    /*We convert the matrix size to an integer.*/
    matrixSize = atoi(argv[1]);
    
    /*set flagTransposed to 1 in case we specified t in the arguments.*/
    if(argc == 3) flagTransposed = argv[2][0] == 't' ? 1 : 0;

    /*We create the two matrices*/
    matrixA = generateMatrix(matrixSize);
    matrixB = generateMatrix(matrixSize);
    
    /*We multiply the matrices.*/
    time = matrix_mult(matrixA, matrixB, matrixSize, flagTransposed);
    
    /*We free the matrices.*/
    freeMatrix(matrixA);
    freeMatrix(matrixB);
    
    /*We print the time*/
    printf("%f\n", time);
    
    return EXIT_SUCCESS;
}