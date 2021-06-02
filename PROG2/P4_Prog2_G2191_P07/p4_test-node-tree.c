/** 
 * @brief Main program for testing trees with nodes
 * 
 * @file p4_test-node-tree.c
 * @author Rodrigo Juez and Enmanuel Abreu Gil
 * @copyright GNU Public License
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "node.h"
#include "tree.h"
#include "types.h"
#define MAX_LINE 20


extern int errno;


int main(int argc, char const *argv[]){
    FILE *f;
    char line[MAX_LINE];
    int id=-1;
    Node *nodeinsert=NULL;
    Tree *ab=NULL;

    if(argc<2 || argc >2){
        fprintf(stdout, "Expecting %s <filename.txt>\n", argv[0]); 
        return (EXIT_FAILURE);
    }

    f=fopen(argv[1],"r");
    if(f==NULL){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error opening file: %s\n", strerror(errno));  
	    return (EXIT_FAILURE);
    }

    ab=tree_ini(node_destroy, node_copy, node_print, node_cmp);
    if(!ab) {
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in memory allocation in tree_ini: %s\n", strerror(errno));  
		
        return (EXIT_FAILURE);
    }
    while(fscanf(f, "%i %s", &id, line)==2){
        nodeinsert=node_ini();
        if(!nodeinsert) return (EXIT_FAILURE);
        node_setId(nodeinsert, id);
        node_setName(nodeinsert, line);
        tree_insert(ab, nodeinsert);               
        
        node_destroy(nodeinsert);
    }
    printf("Depth: %i\nNumber of Nodes: %i", tree_depth(ab), tree_numNodes(ab));
    printf("\nTree inOrder: ");
    tree_inOrder(stdout, ab);
    printf("\nTree preOrder: ");
    tree_preOrder(stdout, ab);
    printf("\nTree postOrder: ");
    tree_postOrder(stdout, ab);
    printf("\n");

    printf("Insert an id to search: "); 
    scanf("%i", &id);
    printf("Insert the name of that id: ");
    scanf("%s", line);

    nodeinsert=node_ini();
    if(!nodeinsert) return (EXIT_FAILURE);
    node_setId(nodeinsert, id);
    node_setName(nodeinsert, line);
    
    if(tree_find(ab, nodeinsert)){
        printf("\nThe noded IS in the tree\n");
    }

    else{
        printf("\nThe noded is NOT in the tree\n");

    }

    node_destroy(nodeinsert);

    tree_free(ab);
    fclose(f);
return (EXIT_SUCCESS);
}