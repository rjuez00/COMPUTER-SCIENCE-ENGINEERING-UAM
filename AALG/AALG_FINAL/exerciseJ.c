#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "sorting.h"

int main(int argc, char** argv){

    int larga[10], corta[8], i ,bl, bc;
    larga[0] = 6;
    larga[1] = 3;
    larga[2] = 9;
    larga[3] = 8;
    larga[4] = 7;
    larga[5] = 1;
    larga[6] = 10;
    larga[7] = 2;
    larga[8] = 4;
    larga[9] = 5;


    for(i=0; i<8; i++){
        corta[i]=8-i;
    }

    printf("\n");

    for(i=0; i<10; i++){
        printf("%d ", larga[i]);
    }
    printf("\n");

    for(i=0; i<8; i++){
        printf("%d ", corta[i]);
    }
    printf("\n");

    bl = quicksort(larga, 0, 9);
    bc = quicksort(corta, 0, 7);

    printf("Larga BOs: %d\n", bl);
    printf("Corta BOs: %d\n", bc);
     for(i=0; i<10; i++){
        printf("%d ", larga[i]);
    }
    printf("\n");

    for(i=0; i<8; i++){
        printf("%d ", corta[i]);
    }
    printf("\n");
    return 0;


} 