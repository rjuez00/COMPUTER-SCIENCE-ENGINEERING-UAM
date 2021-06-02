#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "types.h"
#include "node.h"
#include "graph.h"

#define MAX_NAME 100


int main(int argc, char **argv) {
    int startid, endid;
    FILE *f=NULL;
    Graph *graph=NULL;
    Node *end=NULL;
    Node *using1=NULL;
    Node *using2=NULL;
    char filename[MAX_NAME];

    if(argc>4 || argc<4){
        printf("Expecting only ./p3_e1 <filename> <origin_id> <destination_id>\n");
        return (EXIT_FAILURE);
    }

    if(!strcmp(argv[2], argv[3])){
        printf("Do not enter the same id for the origin and the destination");
        return (EXIT_FAILURE);

    }
    strcpy(filename, argv[1]);
    startid=atoi(argv[2]);
    endid=atoi(argv[3]);

    graph=graph_ini();
    if(!graph){return (EXIT_FAILURE);}
    f=fopen(filename, "r");
    if(!f){return (EXIT_FAILURE);}
    
    if(!graph_readFromFile(f,graph)){return (EXIT_FAILURE);}
    if(!graph_print(stdout,graph)){return (EXIT_FAILURE);}

    end=graph_findDeepSearch(graph,startid,endid);

    if(!end){
        printf("\nPath not found");
    }
    else{
        using1=graph_getNode(graph,startid);
        using2=graph_getNode(graph,endid);
        printf("\n\nA path was found between %s and %s: \n", node_getName(using1), node_getName(using2));
            graph_printPath(stdout,graph,endid);

    }


    printf("\n\n");
    fclose(f);
    node_destroy(using1);
    node_destroy(using2);
    graph_destroy(graph);
    node_destroy(end);
    return (EXIT_SUCCESS);
}

