/** 
 * @brief Module for handeling trees
 * 
 * @file tree.c
 * @author Rodrigo Juez
 * @copyright GNU Public License
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "tree.h"

extern int errno;
/*FOR NODES*/
    #define INFO(x) ((x)->info)
    #define LEFT(x) ((x)->left)
    #define RIGHT(x) ((x)->right)
/*FOR TREES*/
    #define ROOT(pa) ((pa)->root)


typedef struct _NodeBT {
    void* info;
    struct _NodeBT* left;
    struct _NodeBT* right;
} NodeBT;

struct _Tree {
    NodeBT *root;

    destroy_elementtree_function_type destroy_element_function;
    copy_elementtree_function_type copy_element_function;
    print_elementtree_function_type print_element_function;
    cmp_elementtree_function_type cmp_element_function;
};

/*PRIVATE FUNCTIONS DECLARATION*/
    Bool tree_findRec(NodeBT *pa, const void *po, cmp_elementtree_function_type cmp);
    int tree_numNodesRec(NodeBT *pa);
    int tree_depthRec(NodeBT *pa);
    Status tree_postOrderRec(FILE *f, NodeBT *pa, print_elementtree_function_type print);
    Status tree_inOrderRec(FILE *f, NodeBT *pa, print_elementtree_function_type print);
    Status tree_preOrderRec(FILE *f, NodeBT *pa, print_elementtree_function_type print);
    Status tree_insertRec(NodeBT **pa, const void *po,copy_elementtree_function_type copy_funct, cmp_elementtree_function_type cmp_funct);
    void tree_freeRec(NodeBT *n, destroy_elementtree_function_type destroy_element_function);
    NodeBT* NodeBT_ini(const void *po, copy_elementtree_function_type copy);

Tree* tree_ini(destroy_elementtree_function_type f1,copy_elementtree_function_type f2,print_elementtree_function_type f3,cmp_elementtree_function_type f4){
    Tree *pa=NULL;
    if(!f1 || !f2 || !f3 || !f4){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_ini: %s\n", strerror(errno));  
        
        return NULL;}
    pa=(Tree*)malloc(sizeof(Tree));
    if(!pa){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in memory allocation in tree_ini: %s\n", strerror(errno));  
        
        return NULL;}
    pa->root=NULL;
    pa->cmp_element_function=f4;
    pa->copy_element_function=f2;
    pa->destroy_element_function=f1;
    pa->print_element_function=f3;
    return pa;
}

Bool tree_isEmpty( const Tree *pa){
    if (!pa) {
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_isEmpty: %s\n", strerror(errno));  
        
        return TRUE;
    }
    if (!ROOT(pa))
        return TRUE;
    
    return FALSE;
}

void tree_free(Tree *pa){
   if(!pa){
       fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_free: %s\n", strerror(errno));  
        
       return;}
   tree_freeRec(ROOT(pa), pa->destroy_element_function);
   free(pa);


}

Status tree_insert(Tree *pa, const void *po){
    if (!pa || !po){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_insert: %s\n", strerror(errno));  
        
        return ERROR;}
    return tree_insertRec(&ROOT(pa), po, pa->copy_element_function, pa->cmp_element_function);

}

Status tree_preOrder(FILE *f, const Tree *pa){
    if(!f || !pa){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_preOrder: %s\n", strerror(errno));  
        
        return ERROR;}
    return tree_preOrderRec(f, ROOT(pa), pa->print_element_function);

}

Status tree_inOrder(FILE *f, const Tree *pa){
    if(!f|| !pa){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_inOrder: %s\n", strerror(errno));  
        
        return ERROR;}

    return tree_inOrderRec(f, ROOT(pa), pa->print_element_function);
}

Status tree_postOrder(FILE *f, const Tree *pa){
    if(!f || !pa){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_postOrder: %s\n", strerror(errno));  
        
        return ERROR;}

    return tree_postOrderRec(f, ROOT(pa), pa->print_element_function);
}

int tree_depth(const Tree *pa){
    if(!pa || tree_isEmpty(pa)){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_depth: %s\n", strerror(errno));  
        
        return 0;} /*tree_isEmpty also checks for an invalid pointer*/
    return tree_depthRec(ROOT(pa));
}

int tree_numNodes(const Tree *pa){
    if(!pa || tree_isEmpty(pa)){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_numNodes: %s\n", strerror(errno));  
        
        return 0;} /*tree_isEmpty already checks for invalid pointer and empty tree*/
    return tree_numNodesRec(ROOT(pa));
}

Bool tree_find(Tree* pa, const void* pe){
    if(!pa || tree_isEmpty(pa)){
        fprintf(stderr, "Value of errno: %d\n", errno);
        fprintf(stderr, "Error in argument for function tree_find: %s\n", strerror(errno));  
        
        return FALSE;} /*tree_isEmpty already checks for a NULL pointer apart from its main function*/
    return tree_findRec(ROOT(pa), pe, pa->cmp_element_function);
}



/*-------------------------RECURSIVE PRIVATE FUNCTIONS-------------------------*/
Bool tree_findRec(NodeBT *pa, const void *po, cmp_elementtree_function_type cmp){
    int cmpr=0;
    if(!po || !cmp || !pa) {return FALSE;}

    cmpr=cmp(po, pa->info);
    if(cmpr==0){
        return TRUE;
    }
    if(cmpr > 0)
        return tree_findRec(RIGHT(pa), po, cmp);
    else
        return tree_findRec(LEFT (pa), po, cmp);
    
    return ERROR;
}

int tree_numNodesRec(NodeBT *pa){
    if(!pa){return 0;}
    return 1 + tree_numNodesRec(RIGHT(pa)) + tree_numNodesRec(LEFT(pa));
}

int tree_depthRec(NodeBT *pa){
    int cuanttR=0;
    int cuanttL=0;
    if(!pa){return -1;}
    if(!RIGHT(pa) && !LEFT(pa)){return 0;}
    cuanttR=tree_depthRec(RIGHT(pa));
    cuanttL=tree_depthRec(LEFT (pa));
    if(cuanttR>cuanttL){
        return cuanttR+1;
    }
        return cuanttL+1;
}

Status tree_postOrderRec(FILE *f, NodeBT *pa, print_elementtree_function_type print){
    if(!f || !print){return ERROR;}
    if (!pa){return OK;}
    tree_postOrderRec(f, LEFT(pa), print);
    tree_postOrderRec(f, RIGHT(pa), print);
    print(f, pa->info);
    return OK;
}

Status tree_inOrderRec(FILE *f, NodeBT *pa, print_elementtree_function_type print){
    if(!f || !print){return ERROR;}
    if(!pa){return OK;}
    tree_inOrderRec(f, LEFT(pa), print);
    print(f, pa->info);
    tree_inOrderRec(f, RIGHT(pa), print);
    return OK;
}

Status tree_preOrderRec(FILE *f, NodeBT *pa, print_elementtree_function_type print){
    if(!f) return ERROR;
    if(!pa) return OK;
    print(f, pa->info);
    tree_preOrderRec(f, LEFT(pa), print);
    tree_preOrderRec(f, RIGHT(pa), print);
    return OK;
}

Status tree_insertRec(NodeBT **pa, const void *po,copy_elementtree_function_type copy_funct, cmp_elementtree_function_type cmp_funct){
    int comparison=0;
    if(!copy_funct || !cmp_funct || !po){return ERROR;}

    if(*pa==NULL){ /*We've hitted the end of the tree!*/
        *pa=NodeBT_ini(po, copy_funct);
        if(!pa){return ERROR;}
        return OK;
    }
    /*If we are not at the end of the tree */
    comparison=cmp_funct(po, (*pa)->info);
    if(comparison < 0){
        return tree_insertRec( &(LEFT(*pa)), po, copy_funct, cmp_funct);
    }

    else if (comparison > 0){
        return tree_insertRec( &(RIGHT(*pa)), po, copy_funct, cmp_funct);
    }

    else {return ERROR;}
    return ERROR;
}

void tree_freeRec(NodeBT *n, destroy_elementtree_function_type destroy_element_function){
    if(!n || !destroy_element_function){return;}
    tree_freeRec(RIGHT(n), destroy_element_function);
    RIGHT(n)=NULL;
    tree_freeRec(LEFT(n) , destroy_element_function);
    LEFT(n)=NULL;
    destroy_element_function(n->info);
    free(n);
}

NodeBT* NodeBT_ini(const void *po, copy_elementtree_function_type copy){
    NodeBT *new=NULL;
    new=(NodeBT*)malloc(sizeof(NodeBT));
    if(!new){return NULL;}
    new->info=copy(po);
    new->left=NULL;
    new->right=NULL;
    return new;
}