#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "node.h"
#define NAME_L 350
extern int errno;
/*The label indicates if it has been scanned*/
struct _Node {
    char name[NAME_L];
    int id;
};

Node *node_ini(){
    Node *a=NULL;
    a=(Node*)calloc(1,sizeof(Node));
    if(!a){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_ini: %s\n", strerror(errno));  
        return NULL;}
    a->id=0;
    strcpy(a->name, "");
    return a;
}

void node_destroy(void *n){
    if(!n){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_destroy: %s\n", strerror(errno));  
    return;}
    free(n);
}

int node_getId(const Node *n){
    int id;
    if(!n){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_getId: %s\n", strerror(errno));  
        return -1;
    }
    id=n->id;
    return id;
}

char *node_getName(const Node *n){
    if(!n){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_getName: %s\n", strerror(errno));  
        return NULL;}
        
    return (char*)n->name;
}


Node *node_setId(Node *n, const int id){
    if(!n){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_setId: %s\n", strerror(errno));  
        return NULL;}
    n->id=id;
    return n;

}

Node *node_setName(Node *n, const char *name){
    if(!n || !name){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_setName: %s\n", strerror(errno));  
        return NULL;}
    strcpy(n->name,name);
    return n;
}


int node_cmp (const void *n1, const void *n2){
    int n1id=0, n2id=0, compare=0;
    char *n1str, *n2str; 
    if(!n1||!n2){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_cmp: %s\n", strerror(errno));  
        return -9999;
    }
    n1id=node_getId((Node*)n1);
    n2id=node_getId((Node*)n2);
    n1str=node_getName((Node*)n1);
    n2str=node_getName((Node*)n2);
    
    compare=n1id-n2id;
    
    if(strcmp(n1str,n2str) && compare==0){
        compare++;
        /*the declaration doesn't specify what to do 
         * in case of same id but different 
         * name so I just set it to 1*/
    }
    
    return compare;
}

void *node_copy(const void *src){
    const Node *use;
    int id=-1;
    Node *a=NULL;
    if(!src){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_copy: %s\n", strerror(errno));  
        return NULL;
    }

    a=node_ini();
    use=src;
    id=node_getId(use);
    if(a==NULL){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in memory allocation for node_ini: %s\n", strerror(errno));  
        return NULL;}
   
    
    
    a=node_setId(a,id);
    a=node_setName(a,node_getName(use));
    
    return a;

}

int node_print(FILE *pf, const void *n){
    const Node *use;
    int success;
    use=n;
    if(!pf||!n){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function node_print: %s\n", strerror(errno));  
        return -1;
    }
    success=fprintf(pf,"[%i,%s]",node_getId(use), node_getName(use));
   
    return success;

}
