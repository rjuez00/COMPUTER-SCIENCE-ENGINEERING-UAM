#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <stdbool.h>

#include "SymbolTable.h"

#define BUFFER_SIZE 2000
#define CIERRE -999
#define ZERO 0

void cleanse(char * str) {
    /*Removes the \n at the end of the string str*/
    for(;*str != '\0'; str++)
        if(*str == '\n')
            *str = '\0';
}


int main(int argc, char* argv[]){
    SymbolTable* table = NULL;
    DataItem* item = NULL;
    FILE* input = NULL, * output = NULL;
    if(argc != 3){
        printf("Correct usage: %s <inputfile> <outputfile>\n", argv[0]);
        return EXIT_FAILURE;
    }
    
    input = fopen(argv[1], "r");
    if(!input){
        fprintf(stderr, "error when opening input file\n");
        return EXIT_FAILURE;
    }
    output = fopen(argv[2], "w");
    if(!output){
        fprintf(stderr, "error when opening output file\n");
        fclose(input);
        return EXIT_FAILURE;
    }

    table = SymbolTable_new();
    if(!table){
        fprintf(stderr, "error alloc'ing SymbolTable\n");
        fclose(input);
        fclose(output);
        SymbolTable_free(table);
        return EXIT_FAILURE;
    }
    char buffer[BUFFER_SIZE];

    while (true) {
        if (fgets(buffer, BUFFER_SIZE, input) == NULL) break;
        DataItem* item = NULL;
        char * id = strtok(buffer, " ");
        cleanse(id);
        char * val = strtok(NULL, "\n");
        /* If it's NULL, we're searching for the key
             */
        if (val != NULL) {
            int value = atoi(val);
            if (value < ZERO){
                if (value == CIERRE) {
                    if (strcmp(id, "cierre") == 0 || strcmp(id, "close") == 0) {
                        if(SymbolTable_to_global(table) == ERROR) {
                            fprintf(output, "-1\t%s\n", id);
                        } else {
                            fprintf(output, "cierre\n");
                        }
                    } else {
                        fprintf(output, "-1\t%s\n", id);
                    }
                } else {
                    if (SymbolTable_to_local(table, id, value, INT, SCALAR) == ERROR){
                        fprintf(output, "-1\t%s\n", id);
                    }
                    else{
                        fprintf(output, "%s\n", id);
                    }
                }
            } else {
                if(SymbolTable_add(table, id, value, VARIABLE, INT, SCALAR) == ERROR) {
                    fprintf(output, "-1\t%s\n", id);
                } else {
                    fprintf(output,"%s\n", id);
                }
            }
        } else {
            item = SymbolTable_get(table, id);
            fprintf(output, "%s\t%d\n", id, item != NULL ? DataItem_get_value(item) : -1);
        }
    }
    
   
    SymbolTable_free(table);
    fclose(input);
    fclose(output);

    return EXIT_SUCCESS;
}