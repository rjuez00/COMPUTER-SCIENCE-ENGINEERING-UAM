#pragma GCC optimize ("-O3")
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include "graph.h"
#include "queue.h"


struct _Graph{
    Node *nodes[MAX_NODES];
    Bool connections[MAX_NODES][MAX_NODES];
    
    int num_nodes;
    int num_edges;
};

Status reverse_queue(Queue *q)
{
    void* temp=NULL;
    if (queue_isEmpty(q))
       return ERROR;
    else {
        temp=queue_extract(q);
        reverse_queue(q);
        queue_insert(q,temp);
        node_destroy(temp);
        return OK;
    }
}

void graph_printPath (FILE *pf, Graph *g, int idNode){
    Node *act=NULL;
    int counter=0;
    Node *print=NULL;
    int backId;
    Queue *st=NULL;
    st=queue_ini(node_destroy, node_copy, node_print);
    if(!pf || !g || idNode <0){ return; }

    backId=idNode;
    while(backId!=-1){
        act=graph_getNode(g,backId);
        queue_insert(st,act);
        backId=node_getPrevious(act);
        node_destroy(act);
    }
    reverse_queue(st);
    

    while(!queue_isEmpty(st)){
        print=queue_extract(st);
        fprintf(pf,"-->");
        node_print(pf,print);

        if(counter>3){
             fprintf(pf,"-->");

            printf("\n");

            counter=0;
        }

        node_destroy(print);
        counter++;
    }
    queue_destroy(st);
}


Node *graph_findDeepSearch (Graph *g, int from_id, int to_id){
   Bool finished=FALSE;
    Queue *st=NULL;
    Node *start=NULL;
    Node *aux=NULL;
    Node *neighbour=NULL;
    int auxid=-1;
    int cuanttconnect=0;
    int *connectindex=NULL;
    int i=0;
    if(!g || from_id==-1 || to_id==-1){return NULL;}
    st=queue_ini(node_destroy, node_copy, node_print);
    start=graph_getNode(g,from_id);
    if(!start){return NULL;}
    queue_insert(st,start);
   
    while(!queue_isEmpty(st)){
        aux=queue_extract(st); 
        auxid=node_getId(aux);
        if(!aux){printf("ERROR"); return NULL;}

        if(!node_getLabel(aux)){
            cuanttconnect=node_getConnect(aux);
            connectindex=graph_getConnectionsFrom(g, auxid);
            node_setLabel(aux,BLACK);
            graph_setNode(g,aux); 
            for(i=0; i<cuanttconnect; i++){

                neighbour=graph_getNode(g,connectindex[i]);

                if(to_id == connectindex[i]){
                    node_setPrevious(neighbour,auxid);
                    graph_setNode(g,neighbour);
                    finished=TRUE;
                    break;
                }

                else if(node_getLabel(neighbour)==WHITE){
                    node_setPrevious(neighbour,auxid);
                    queue_insert(st, neighbour);
                    graph_setNode(g, neighbour);

                }
                node_destroy(neighbour);
                neighbour=NULL;
            }
            node_destroy(aux);

        }
        else {
            node_destroy(aux);
        }
        free(connectindex);
        connectindex=NULL;
        if(finished){break;}
    }
    node_destroy(start);
    queue_destroy(st);
    return neighbour; 
}


int find_node_index(const Graph *g, int nId1) {
 int i;
 if (!g) return -1;

 for(i=0; i < g->num_nodes; i++) {
 if (node_getId (g->nodes[i]) == nId1) return i;
 }

 
 return -1;
}

int *graph_getConectionsIndex(const Graph *g, int index) {
    int *array = NULL, i, j=0, size;

    if (!g) return NULL;
    if (index < 0 || index >g->num_nodes) return NULL;
    /* get memory for the array with the connected nodes index*/
    size = node_getConnect (g->nodes[index]);
    array = (int *) malloc(sizeof(int) * size);

    if (!array) {
    /* print errorr message*/
    fprintf (stderr, "%s\n", strerror(errno));
    return NULL;
 }

 /* asigno valores al array con los indices de los nodos conectados*/
 for(i = 0; i< g->num_nodes; i++) {
     if (g->connections[index][i] == TRUE) { 
         array[j] = i;
         j++;}
 }

 return array;
}

Status graph_readFromFile (FILE *fin, Graph *g) {
 Node *n;
 char buff[MAX_LINE], name[MAX_LINE];
 int i, nnodes = 0, id1, id2;
 Status flag = ERROR;

 /* read number of nodes*/
 if ( fgets (buff, MAX_LINE, fin) != NULL)
 if ( sscanf(buff, "%d", &nnodes) != 1) return ERROR;

 /* init buffer_node*/
 n = node_ini();
 if (!n) return ERROR;

 /* read nodes line by line*/
 for(i=0; i < nnodes; i++) {
     if ( fgets(buff, MAX_LINE, fin) != NULL)
         if (sscanf(buff, "%d %s", &id1, name) != NO_FILE_POS_VALUES) break;

 /* set node name and node id*/
     node_setName (n, name);
     node_setId (n, id1);

 /*insert node in the graph*/
     if ( graph_insertNode (g, n) == ERROR) break;
 }

 /* Check if all node have been inserted*/
 if (i < nnodes) { 
     node_destroy(n);
     return ERROR;
 }

 /* read connections line by line and insert it*/
 while ( fgets(buff, MAX_LINE, fin) ) {
     if ( sscanf(buff, "%d %d", &id1, &id2) == NO_FILE_POS_VALUES )
         if (graph_insertEdge(g, id1, id2) == ERROR) break;
 }

 /* check end of file*/
 if (feof(fin)) flag = OK;

 /*clean up, free resources*/
 node_destroy (n);
 return flag;
}

Graph *graph_ini(){
    Graph *a=NULL;
    int j;
    int i;
    a=(Graph*)calloc(1,sizeof(Graph));
    a->num_edges=0;
    a->num_nodes=0;

    for(i=0; i<MAX_NODES; i++){
        a->nodes[i]=NULL;

        for(j=0; j<MAX_NODES; j++){
            a->connections[i][j]=0;
        }

    }
    
    return a;
}

void graph_destroy(Graph *g){
    int i;
    if(!g) return;

    for(i=0; i<MAX_NODES; i++){
        free(g->nodes[i]);
        g->nodes[i]=NULL;
    }
    free(g);
}

Node *graph_getNode (const Graph *g, int nId){
    Node *newboi;
    int a;
    if(!g || nId<0) return NULL;
    a=find_node_index(g, nId);
    if(a==-1){printf("ERROR"); return NULL;}
    newboi=node_copy(g->nodes[a]);
    if(!newboi){printf("NULL");return NULL;}
    return newboi;
}

Status graph_setNode (Graph *g, const Node *n){
    Node *newboi;
    int index;
    if(!g || !n) return ERROR;
    
    newboi=node_copy(n);
    
    index=find_node_index(g, node_getId(n));
    if(index==-1) return ERROR;
    
    
    /*I SET THE NUMBER OF CONNECTIONS TO NEWBOI AS IS REPLACING ANOTHER PREVIOUS NODE WITH THE SAME CONNECTIONS*/
    node_setConnect(newboi, node_getConnect(g->nodes[index]));
    
    node_destroy(g->nodes[index]);
    g->nodes[index]=newboi;

    return OK;

}

int *graph_getNodesId (const Graph* g){
    int *arr;  
    int i;
    arr=(int*)calloc(graph_getNumberOfNodes(g),sizeof(int));

    if(!arr) return ERROR;

    for(i=0; i<graph_getNumberOfNodes(g); i++){
        arr[i]=node_getId(g->nodes[i]);
    }
    return arr;
        
}

int graph_getNumberOfNodes(const Graph *g){
    if (!g){
        return -1;
    }
    return g->num_nodes;
}


int graph_getNumberOfEdges(const Graph * g){
    int edges=0;
    if(!g) return -1;
    
    edges= g->num_edges;

    return edges;
}

Bool graph_areConnected(const Graph * g, const int og, const int dest){
    int index1, index2;
    if(!g) return FALSE;
    
    index1=find_node_index(g,og);
    index2=find_node_index(g,dest);

    if(g->connections[index1][index2] == 1) return TRUE;

    return FALSE;
}

int graph_getNumberOfConnectionsFrom(const Graph *g, const int fromId){
    int cuantt=0;
    if(!g) return -1;
    
    cuantt=node_getConnect(graph_getNode (g, fromId));

    return cuantt;   
}

int *graph_getConnectionsFrom(const Graph *g, const int og){
    int *connections=NULL;
    int position=-1, cuanttconnections, i;
    if(!g || og < 0){return NULL;}
    position=find_node_index(g,og);
    if(position ==-1){return NULL;}
    connections=graph_getConectionsIndex(g,position);
    if(!connections){return NULL;}
    cuanttconnections=node_getConnect(g->nodes[position]);
 
    for(i=0; i<cuanttconnections; i++){
        connections[i]=node_getId(g->nodes[connections[i]]);
    }
    
    return connections;
}

int graph_print(FILE *pf, const Graph *g){
    int cuantt=0, *connections=NULL, sum=0, i=0, x=0, nconnect=0, printed=0;
    int success=0;
    if(!g || !pf) return -1;
    cuantt=graph_getNumberOfNodes(g);
    
    for(i=0; i<cuantt; i++){
        /*DEVUELVE ARRAY CON CONEXIONES*/
        sum=node_print(pf, g->nodes[i]);
        connections=graph_getConectionsIndex(g, i);
        nconnect=node_getConnect(g->nodes[i]);

        for(x=0; x<nconnect; x++){
            printed=fprintf(pf,"%i ",node_getId(g->nodes[connections[x]]));
            sum=sum+printed;
                
        }
        
        fprintf(pf,"\n");
        nconnect=0;
        success+=sum;
        free(connections);
        connections=NULL;
        sum=0;
        }

        
        
        return success;        
}

Status graph_insertNode(Graph *g, const Node *n) {
    int i=0;
    int id;
    Node *newboi;
    if(!g || !n) return ERROR;

    for(i=0; i<graph_getNumberOfNodes(g); i++){
        if(!node_cmp(n,g->nodes[i]))
            return ERROR;

    }

    
    id=node_getId(n);
    if(find_node_index(g,id) != -1) return ERROR;
    
    

    newboi=node_copy(n);
    if(!newboi) return ERROR;
    g->nodes[graph_getNumberOfNodes(g)]=newboi;
    g->num_nodes++;
    return OK;

}

/* Se añade una arista entre los nodos de id "nId1" y "nId2".
 * Actualiza los atributos del grafo y de los nodos que sean necesarios.
 * Devuelve OK o ERROR. */

Status graph_insertEdge(Graph *g, const int og, const int dest){
    int indexog, indexdest, nConnect1;
    if(!g || og<0 || dest<0) return ERROR;
    

    indexog=find_node_index(g, og);
    indexdest=find_node_index(g, dest);

    nConnect1=node_getConnect(g->nodes[indexog]);
   
    
    g->connections[indexog][indexdest]=1;
    
    node_setConnect(g->nodes[indexog], nConnect1+1);
    return OK;

}
