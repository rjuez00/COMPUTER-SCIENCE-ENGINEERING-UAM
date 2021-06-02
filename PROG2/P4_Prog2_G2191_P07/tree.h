/** 
 * @brief Interface for handeling trees
 * 
 * @file tree.c
 * @author Prog2 Teachers 
 * @copyright GNU Public License
 */
#ifndef TREE_H
#define TREE_H
#include "types.h"



typedef struct _Tree Tree;

typedef void (*destroy_elementtree_function_type)(void*);
typedef void (*(*copy_elementtree_function_type)(const void*));
typedef int (*print_elementtree_function_type)(FILE *, const void*);
typedef int (*cmp_elementtree_function_type)(const void*, const void*);
/* Initialize an empty tree. */
Tree* tree_ini(destroy_elementtree_function_type f1,copy_elementtree_function_type f2,print_elementtree_function_type f3,cmp_elementtree_function_type f4);
/* Indicates if the tree is empty or not. */
Bool tree_isEmpty( const Tree *pa);
/* Frees the memory used by a Tree.*/
void tree_free(Tree *pa);
/* Inserts an element into a binary search tree by copying it into new memory. */
Status tree_insert(Tree *pa, const void *po);
/*Writes in the file f the path of a tree in previous order without modifying it. */
Status tree_preOrder(FILE *f, const Tree *pa);
/* Writes in the file f the path of a tree in medium order without modifying it */
Status tree_inOrder(FILE *f, const Tree *pa);
/* Writes in file f the path of a tree in post order without modifying it. */
Status tree_postOrder(FILE *f, const Tree *pa);
/* Computes the depth of a tree. An empty tree has depth -1. */
int tree_depth(const Tree *pa);
/* Computes the number of nodes in a tree. An empty tree has 0 nodes.*/
int tree_numNodes(const Tree *pa);
/* Returns TRUE if the element pe can be found in the tree pa */
Bool tree_find(Tree* pa, const void* pe);


#endif 