/** 
 * @brief main program
 * 
 * @file p4_e2.c
 * @author Rodrigo Juez and Enmanuel Abreu Gil
 * @copyright GNU Public License
 */

/*INCLUDES*/
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <errno.h>
    #include "int.h"
    #include "tree.h"

    extern int errno;

int main(int argc, char **argv) {
    /*DECLARATION*/
        FILE* f=NULL;
        Tree* pa=NULL; 
        int temp=-1;
        int search=-1;
        if (argc !=2){
            printf("Expecting %s <filename>\n", argv[0]); 
            return (EXIT_FAILURE);
        }
    /*MEMORY*/
        f=fopen(argv[1], "r");
        if(!f){
            fprintf(stderr, "Value of errno: %d\n", errno);
            fprintf(stderr, "Error opening file: %s\n", strerror(errno));  
            return (EXIT_FAILURE);
        }
        pa=tree_ini(int_destroy, int_copy, int_print, int_cmp);
        if(!pa){
            fprintf(stderr, "Value of errno: %d\n", errno);
            fprintf(stderr, "Error in p4_e2 allocating memory: %s\n", strerror(errno));              return (EXIT_FAILURE);
        }

    while(fscanf(f,"%i", &temp)==1){
        tree_insert(pa, &temp);
    }
    fclose(f);


    printf("Number of Nodes: %i\nDepth: %i\n", tree_numNodes(pa), tree_depth(pa));

    printf("Previous Order:");
    tree_preOrder(stdout, pa);
    
    printf("\nAverage order:");
    tree_inOrder(stdout, pa);
    
    printf("\nLater Order:");
    tree_postOrder(stdout,pa);
    printf("\n");


    printf("Enter a number: ");
    scanf("%i", &search);
    printf("Number entered: %d\n", search);
    if(tree_find(pa, &search)){
        printf("The data %i is inside the Tree\n", search);

    }
    else{
        printf("The data %i is NOT found inside the Tree\n", search);
    }

    /*FREE*/
    tree_free(pa);
    return (EXIT_SUCCESS);
}   

