/** 
 * @brief Main program for testing trees with strings
 * 
 * @file p4_e4.c
 * @author Rodrigo Juez and Enmanuel Abreu Gil
 * @copyright GNU Public License
 */


#include <stdio.h>
#include <stdlib.h>
#include <time.h> 
#include <string.h>
#include <errno.h>


#include "tree.h"
#include "string.h"
#include "types.h"

extern int errno;

/*I create another function to read the file
because that way the fixed string is deleted
when the function is exited*/
char* read_string_from_file(FILE *pf){
	char *dinamic=NULL;
	char read[200];
	if(!pf){
		fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument in function read_string_from_file: %s\n", strerror(errno));  
		return NULL;
	}

	if(fscanf(pf, "%s", read)<1){return NULL;}
	dinamic=(char*)malloc(sizeof(char)*(1+strlen(read)));
	if(!dinamic){
		fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in memory allocation in read_string_from_file: %s\n", strerror(errno));  
		return NULL;
	}
	strcpy(dinamic, read);
	return dinamic;
}

int main(int argc, char **argv){
	FILE *pf=NULL;
	char *a=NULL;
	char search[20];
	Tree *ab=NULL;
	if(argc<2 || argc>2) {
		fprintf(stdout, "Use %s <filename>\n", argv[0]);
		return (EXIT_FAILURE);
	}
	
	pf=fopen(argv[1], "r");
	if(!pf) {
		fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error opening file: %s\n", strerror(errno));  
		
		return (EXIT_FAILURE);

	}
	
	ab=tree_ini(string_destroy, string_copy, string_print, string_cmp);
	if(!ab){
		fclose(pf);
		fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in memory allocation in tree_ini: %s\n", strerror(errno));  
		
		return (EXIT_FAILURE);
	}


	while((a=read_string_from_file(pf))!=NULL){
		tree_insert(ab, a);
		string_destroy(a);
	}
	fclose(pf);

	printf("Number of nodes: %i\nDepth: %i\n", tree_numNodes(ab), tree_depth(ab));
	tree_inOrder(stdout, ab);

	printf("\nEnter a string to search the tree (following the same format as in the input file): ");
	scanf("%s", search);
	printf("%s\n", search);
	
	if(tree_find(ab, search)==TRUE){
		printf("Element found!\n");
	}
	else{
		printf("Element NOT found!\n");
	}
	tree_free(ab);
	return 0;
}
