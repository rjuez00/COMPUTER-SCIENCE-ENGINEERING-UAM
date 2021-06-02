#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "node.h"
#define NAME_L 64

/*The label indicates if it has been scanned*/
struct _Node {
    char name[NAME_L];
    int id;
    int nConnect;
    Label etq;
    int previous_id;
};

Node *node_ini(){
    Node *a=NULL;
    a=(Node*)calloc(1,sizeof(Node));
    if(!a){return NULL;}
    a->id=0;
    a->nConnect=0;
    strcpy(a->name, "");
    a->etq=WHITE;
    a->previous_id=-1;
    return a;
}

void node_destroy(void *n){
    if(!n){return;}
    free(n);
}

int node_getId(const Node *n){
    
    int id;
    id=n->id;
    return id;
}

char *node_getName(const Node *n){
    if(!n){return NULL;}
        
    return (char*)n->name;
}

int node_getConnect(const Node *n){
    int nconnect=n->nConnect;
    return nconnect;
}

Node *node_setId(Node *n, const int id){
    if(!n){return NULL;}
    n->id=id;
    return n;

}

Node *node_setName(Node *n, const char *name){
    if(!n){return NULL;}
    strcpy(n->name,name);
    return n;
}

Node *node_setConnect(Node *n, const int cn){
    if(!n){return NULL;}
    n->nConnect=cn;
    return n;
}

int node_cmp (const Node *n1, const Node *n2){
    int n1id=node_getId(n1);
    int n2id=node_getId(n2);
    char *n1str=node_getName(n1);
    char *n2str=node_getName(n2);
    
    int compare=n1id-n2id;
    
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
    int nconnect=-1;
    Node *a=node_ini();
    use=src;
    id=node_getId(use);
    nconnect=node_getConnect(use);
    if(a==NULL){return NULL;}
   
    
    
    a=node_setId(a,id);
    a=node_setConnect(a,nconnect);
    a=node_setName(a,node_getName(use));
    node_setPrevious(a,use->previous_id);
    node_setLabel(a, use->etq);
    return a;

}

int node_print(FILE *pf, const void *n){
    const Node *use;
    int success;
    use=n;
    if(pf==NULL){
        fprintf(stderr, "Error opening file");
    }
    success=fprintf(pf,"[%i,%s,%i]",node_getId(use), node_getName(use), node_getConnect(use));
   
    return success;

}

Label node_getLabel(const Node *n){
    if(!n){return BLACK;}
    return n->etq;
}

Status node_setLabel(Node *n, Label etq){
    if(!n){return ERROR;}
    n->etq=etq;
    return OK;
}

int node_getPrevious(const Node *n){
    if(!n){return -1;}
    return n->previous_id;
}

Status node_setPrevious(Node *n, int id){
    if(!n){return ERROR;}
    n->previous_id=id;
    return OK;
}