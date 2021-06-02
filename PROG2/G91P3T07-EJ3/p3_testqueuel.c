/*
* File: p3_testqueue.c
* Author: PROG2 Teachers
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "queuel.h"
#include "node.h"

#define MAX 255

extern int errno;
void mainCleanUp (Queue *q1, Queue *q2, Queue *q3, Node *pn, FILE *pf) {
 if (pn) node_destroy(pn);
 if (q1) queue_destroy (q1);
 if (q2) queue_destroy (q2);
 if (q3) queue_destroy (q3);
 if (pf) fclose (pf);
}
int main(int argc, char** argv) {
 FILE *pf=NULL;
 Queue *q1=NULL, *q2=NULL, *q3=NULL;
 Node *pn=NULL;
 int id, i, npoints, middle;
 char name[MAX];
 char s[MAX];
 if (argc < 2) {
 fprintf(stderr, " Error: Enter as argument the name of the file with the nodes.\n");
 return EXIT_FAILURE;
 }
 pf = fopen(argv[1], "r");
 if (pf==NULL){
 fprintf (stderr, " File opening error: %s\n", strerror(errno));
 return EXIT_FAILURE;
 }
 if (fgets(s, MAX, pf)==NULL) {
 fprintf(stderr, " File reading error: %s\n", strerror(errno));
mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
 if (sscanf(s, "%d\n", &npoints) !=1 ){
 fprintf(stderr, " Error of data format in file: %s\n", strerror(errno));
mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
 pn = node_ini();
 if (pn==NULL) {
 fprintf(stderr, " Error: node initialization.\n");
mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
 q1 = queue_ini(node_destroy, node_copy, node_print);
 q2 = queue_ini(node_destroy, node_copy, node_print);
 q3 = queue_ini(node_destroy, node_copy, node_print);

 if (!q1 || !q2 || !q3) {
 fprintf(stderr, "Error: queue initialization.\n");
mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
 printf("Inicialmente:\n");
 printf("Queue 1: ");queue_print(stdout, q1);
 printf("Queue 2: ");queue_print(stdout, q2);
 printf("Queue 3: ");queue_print(stdout, q3);
 printf("Adding %d elements a q1:\n", npoints);
 for (i=0; i<npoints; i++){
if (fgets(s, MAX, pf) == NULL){
 fprintf(stderr, " File reading error: %s\n", strerror(errno));
 mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
if(sscanf(s, "%d %s \n", &id, name) !=2 ){
 fprintf(stderr, " Error of data format in file: %s\n", strerror(errno));
 mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
node_setId(pn, id);
node_setName(pn, name);
if (queue_insert(q1, pn) == NULL) {
 fprintf(stderr,"Error: queue insert.\n");
 mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
 printf("Queue 1: ");queue_print(stdout, q1);
printf("Queue 2: ");queue_print(stdout, q2);
printf("Queue 3: ");queue_print(stdout, q3);
 printf("\n");
 }
 node_destroy(pn); pn = NULL;
 printf("\n<<< Passing the first half of Queue 1 to Queue 2\n");
 npoints = queue_size(q1);
 middle = npoints/2;
 for(i=0; i< middle; i++){
pn = queue_extract(q1);
if (queue_insert(q2, pn)== NULL) {
 fprintf(stderr, "Error: insert in Queue 2.\n");
 mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
node_destroy(pn); pn = NULL;
printf("Cola 1: ");queue_print(stdout, q1);
printf("Cola 2: ");queue_print(stdout, q2);
printf("Cola 3: ");queue_print(stdout, q3);
 printf("\n");
 }
 printf("\n<<< Passing the second half of Queue 1 to Queue 3\n");
 for(i=npoints/2; i< npoints; i++){
pn = queue_extract(q1);
if (queue_insert(q3, pn) == NULL) {
 fprintf(stderr,"Error: insert in Queue 3.\n");
 mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_FAILURE;
 }
node_destroy(pn); pn = NULL;
printf("Queue 1: ");queue_print(stdout, q1);
printf("Queue 2: ");queue_print(stdout, q2);
printf("Queue 3: ");queue_print(stdout, q3);
 printf("\n");
 }
 /* Free everything*/
 mainCleanUp (q1, q2, q3, pn, pf);
 return EXIT_SUCCESS;
}