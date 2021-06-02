#include <stdlib.h>
#include "types.h"
#include "minimiza.h"
#include "newstate.h"

#define NAMESIZE 5  // Tamaño maximo que se muestra del nombre de los estados en la funcion de
                    // imprimir matriz


/**
 * Funcion auxiliar que imprime la semimatriz para debugging.
 * - Imprime 0 si dos estados son indistinguibles.
 * - Imprime 1 si dos estados son distinguibles.
 * - Imprime 2 si se ha determinado que dos estados son distinguibles en el ultimo paso.
 *   Una vez acabado el paso los doses se convierten a unos.
 */
void printMatriz(char **matriz, int size, int* lookuptable, AFND* afd){
    
    char tempname[NAMESIZE+1];
    if (matriz == NULL) return;
    for(int u=0; u<NAMESIZE; ++u)
        printf(" ");
    printf("   ");
    for (int i=size-1; i>0; --i){
        sprintf(tempname, "%.*s", NAMESIZE-1, AFNDNombreEstadoEn(afd, lookuptable[i]));
        printf("|  %-*s", NAMESIZE-1, tempname);
    }
    printf("\n");
    for(int u=0; u<NAMESIZE; ++u)
        printf(" ");

    printf("   ");
    
    for (int i=size-1; i>0; --i)
        for(int u=0; u<NAMESIZE+2; ++u)
            printf("-");
    
    printf("\n");
    for (int i=0; i<size-1; ++i){ 
        sprintf(tempname, "%.*s", NAMESIZE, AFNDNombreEstadoEn(afd, lookuptable[i]));
        printf("%-*s:  ", NAMESIZE, tempname);
        for (int j=0; j<size-i-1; ++j) {
            if(matriz[i][j] == 2){
                printf("|  \033[0;31m");
                printf("%d", matriz[i][j]);
                for(int u=0; u<NAMESIZE-2; ++u)
                    printf(" ");
                printf("\033[0m");
            }
            else if(matriz[i][j] == 1){
                printf("|  \033[1;36m");
                printf("%d", matriz[i][j]);
                for(int u=0; u<NAMESIZE-2; ++u)
                    printf(" ");
                printf("\033[0m");
            }
            else{
                printf("|  %d", matriz[i][j]);
                for(int u=0; u<NAMESIZE-2; ++u)
                    printf(" ");
            }
        }
        printf("\n");
    }

    printf("\n\n");
}

/**
 * Recibe un array de in dinámico de tamaño size, le aumenta el tamaño en uno y mete un elemento nuevo al final.
 * No introduce elementos repetidos.
 */
int* append_int(int* array, int* size, int element){
    short flag_initialized = 1;

    if(!array){
        flag_initialized=0;
        *size=0;
    }
    /* Mira si está repetido el elemento */
    if(flag_initialized == 1) 
        for (int i=0; i<*size; i++)
            if(array[i] == element)
                return array;
    
    ++(*size);
    
    if(!flag_initialized)
        array = (int*)malloc((*size) * sizeof(int));
    else
        array = (int*)realloc(array, (*size) * sizeof(int));
    
    if (!array) {
        fprintf(stderr, "Error in realloc or malloc in int append");
        return NULL;
    }
    
    array[(*size)-1] = element;
    return array;
}


/**
 * Elimina los estados inaccesibles, devuelve un array de ids de los estados
 * este array se usará más tarde como "lookup" table, se usará el indice del array
 * como posicion de la matriz y el contenido como id del afd original
 */
int* EliminaInaccesible(AFND* afd, int *tam){
    if(!afd){
        fprintf(stderr, "Error en argumento EliminaInaccesible\n");
        return NULL;
    }
    
    int num_estados_afd = AFNDNumEstados(afd);
    int num_entradas_afd = AFNDNumSimbolos(afd);
    int* accesibles = NULL;
    int size, current = 0;
    /*metemos los iniciales para empezar a analizar a donde nos llevan*/
    accesibles = append_int(accesibles, &size, AFNDIndiceEstadoInicial(afd));

    /*vamos iterando por la lista de accessibles comprobando las entradas y si conectan con otros estados, añadiendolos a los accessibles
    si es asi y analizandolos posteriormente*/
    while(current < size){
        for(int j=0; j<num_entradas_afd; j++)
            for(int k=0; k<num_estados_afd; k++)
                if (AFNDTransicionIndicesEstadoiSimboloEstadof(afd, accesibles[current], j, k))
                    accesibles = append_int(accesibles, &size, k);
        current++;
    }
    *tam = size;
    return accesibles;
}

/**
 * insertamos aqui en la semimatriz, el control de errores esta diseñado para que podamos insertar incluso fuera de 
 * el rango reservado, puesto que cuando inicializamos la matriz no tomamos en cuenta los rangos
 * 
 * argumento final: pone un 2, esto seria como la X negra en el pdf en caso de ser true y roja en el caso de ser false
 * argumento noerror: si es TRUE no printeara los errores por pasarnos de indice, esto lo hicimos para debugear
 * 
 */
void insertarX(char **matriz, int size, int indexRow, int indexColumn, BOOL final, BOOL noerror){
    if (indexColumn >= size || indexRow > indexColumn - 1 || indexRow < 0) {
        if(!noerror)
            fprintf(stderr, "Fallo al insertar en la posicion: %d %d\n", indexRow, indexColumn);
        
        return;
    }
    if(!final) final = 2;
    matriz[indexRow][size - indexColumn -1] = final;
}

/**
 * Funcion auxiliar que usamos para ver que hay en una posicion de la semimatriz
 * Esta hecho de tal forma que tambien funcione si se intenta acceder un elemento 
 * de la otra semimatriz (ya que son simetricas).
 * 
 * Devuelve TRUE si el elemento es 1 (Distinguible) o FALSE si es cualquier otro numero
 * (Usamos 0 para indistinguible y 2 si va a ser distinguible en el siguiente paso)
*/
BOOL getX(char** matriz, int size, int indexRow, int indexColumn){

    // Primero miramos que no se acceda ningun elemento de fuera de la matriz
    if (indexRow >= 0 && indexRow < size && indexColumn >= 0 && indexColumn < size) {

        // Si se cumple esta condicion, la busqueda esta fuera de la semimatriz
        if (indexColumn >= size || indexRow > indexColumn - 1 || indexRow < 0) {
            // Si los indices son diferentes, devolvemos el elemento simetrico con otra
            // llamada a la funcion invirtiendo los argumentos
            if (indexRow != indexColumn) return getX(matriz, size, indexColumn, indexRow);
            else return FALSE; // False porque un elemento es indistinguible de si mismo
        } else { // Si esta dentro de nuestra semimatriz
            if (matriz[indexRow][size - indexColumn -1] == 1) return TRUE;
            else return FALSE;
        }

    } else {

        fprintf(stderr, "Fallo al leer en la posicion: %d %d (%d %d)\n", indexRow, indexColumn, indexRow, size - indexColumn -1);
        return FALSE;

    }
}

/**
 * libera la semimatriz
 */
void liberaMatriz(char** matriz, int size){
    if (matriz == NULL) return;
    for (int i=0; i<size-1; ++i)
        if (matriz[i] != NULL)
            free(matriz[i]);

    free(matriz);
}

/*  Guardamos la semimatriz girada 90º para mayor comodidad
    (Mirar como se imprimen con la funcion de imprimir matriz para entenderlo mejor)
    
EJEMPLO:

        |  H   |  E   |  C   |  G   |  F   |  B   
        ------------------------------------------
A    :  |  0   |  0   |  1   |  0   |  0   |  0   
B    :  |  0   |  0   |  1   |  0   |  0   
F    :  |  0   |  0   |  1   |  0   
G    :  |  0   |  0   |  1   
C    :  |  1   |  1   
E    :  |  0  

¡IMPORTANTE!
        primer indice = lookuptable
        segundo indice = size - lookuptable - 1
        
    este metodo de acceso se usará para acceder a la matriz, puesto que las funciones recibiran el 
    indice de la lookuptable que quieren acceder y en el caso de las columnas como estan
    invertidas hay que obtener el indice de la matriz en si
*/
char** inicializaMatriz(AFND* afd, int* lookuptable, int size){
    if(!afd || !lookuptable || size <= 1){
        fprintf(stderr, "Error en argumentos inicializaMatriz\n");
        return NULL;
    }
    char **matriz = NULL;

    matriz = (char **)calloc(size-1, sizeof(char *));
    if (matriz == NULL) {
        fprintf(stderr, "Error creando la matriz\n");
        return NULL;
    }
    for(int i=0; i<size-1; ++i){
        matriz[i] = (char *)calloc(size-i-1, sizeof(char));
        if (matriz[i] == NULL) {
            fprintf(stderr, "Error creando la matriz\n");
            liberaMatriz(matriz, size);
            return NULL;
        }
    }
    
    int* finales = NULL;
    int finalesSize=0;
    int i; 
    char flag=0;
    
    /* obtenemos los estados finales   */
    for(int i=0; i<size; i++)
        if ( (AFNDTipoEstadoEn(afd, lookuptable[i]) == FINAL) || (AFNDTipoEstadoEn(afd, lookuptable[i]) == INICIAL_Y_FINAL) )
            finales = append_int(finales, &finalesSize, i);
        
    
    /*iteramos por los estados finales*/
    for(int n=0; n<finalesSize; n++){
        i = finales[n];
        for (int j=0; j<size; ++j){
            flag = 0;
            for(int k=0; k<finalesSize; ++k){
                if(finales[k] == j) { /* comprobamos si ambos estados son finales y entonces estaran 
                                         en dos conjuntos distintos asi que los marcamos como DISTINGUIBLES
                                         es decir NO le ponemos un 1*/
                    flag = 1;
                    break;
                }
            }
            if (flag) continue;
            insertarX(matriz, size, i, j, TRUE, TRUE);
            insertarX(matriz, size, j, i, TRUE, TRUE);
        }
    }

    /*para debugear y que se entienda el algoritmo*/
    printMatriz(matriz, size, lookuptable, afd);
    free(finales);
    return matriz;
}

/**
 * Devuelve el indice del estado (del afnd) al que se llega desde el estado
 * suministrado a la funcion mediante la transicion con el indice de la entrada
 * que se pasa a la funcion.
 * En caso de que no exista dicha transicion, devuelve -1
 */
int obtenTransicionConEntrada(AFND *afd, int estado, int entrada){
    for(int i=0; i<AFNDNumEstados(afd); ++i)
        if(AFNDTransicionIndicesEstadoiSimboloEstadof(afd, estado, entrada, i))
            return i;

    return -1;
}


/**
 * Devolvemos el indice en el que esta contenido el id del estado del AFD
 */
int indexInLookupTable(int* lookup, int size, int content){
    if(!lookup) return -1;
    for(int i=0; i<size; ++i){
        if(lookup[i] == content)
            return i;
    }
    
    return -1;
}


/**
 * Determina si dos elementos son indistinguibles. Pasamos indices de nuestra 
 * semimatriz (que convertimos a indices del afdn con la lookup table), miramos
 * a que estados transicionan por cada entrada y usando la lookup table de nuevo
 * miramos si los estados a los que transicionamos son indistinguibles en la matriz.
 * Si por cada entrada llegan a estados indistinguibles, son indistinguibles
 * 
 * Devuelve TRUE si son indistinguibles y FALSE en caso contrario
 */
BOOL comprobarIndistinguible(AFND* afd, char** matriz, int* lookup, int size, int indexA, int indexB){


    // Convertimos los indices a indices de estados del afnd
    int estado1 = lookup[indexA];
    int estado2 = lookup[indexB];
    int estadoDest1, estadoDest2;

    for(int i=0; i<AFNDNumSimbolos(afd); ++i){

        // Indices de los estados del afnd a los que transicionan con la entrada i
        estadoDest1 = obtenTransicionConEntrada(afd, estado1, i);
        estadoDest2 = obtenTransicionConEntrada(afd, estado2, i);;

        // Si son iguales (o no transiciona niguno porque ambos devuelven -1)
        if (estadoDest1 == estadoDest2) {
            continue;
        // Si uno transiciona y otro no
        } else if (estadoDest1 == -1 || estadoDest2 == -1) {
            return FALSE;
        // Miramos si los estados a los que llegan son indistinguibles.
        // indexInLookupTable convierte un indice de estado del afnd a uno de la matriz
        } else {
            if ( getX(matriz, size, indexInLookupTable(lookup, size, estadoDest1), indexInLookupTable(lookup, size, estadoDest2)) == TRUE ){
                return FALSE;
            }
        }
        
    }
    
    return TRUE;  // Indistinguibles!
} 



/**
 * setea a 1 todos los 2 de la matriz, esto se hace cuando se han comprobado ya si todos los elementos
 * son indisguibles o no, es decir se generan los nuevos conjuntos
 */
void cierraConjuntos(char** matriz, int size){
    for (int i=0; i<size-1; ++i){
        for (int j=0; j<size-i-1; ++j) {
            if (matriz[i][j] == 2)
                matriz[i][j] = 1;
        }
    }
}


/**
 * Va comprobando elemento a elemento si son indistinguibles y si es asi inserta un 2 en la matriz
 * Al final de la funcion, los 2s se convierten en 1s
 * 
 * Devuelve un booleano que indica si se ha cambiado la matriz en este paso del algoritmo
 */
BOOL calculaConjuntos(AFND* afd, char** matriz, int* lookup, int size){
    BOOL sonindistinguibles;
    BOOL cambiado = FALSE;
    for(int i=0; i<size-1; i++)
        for(int j=i+1; j<size; j++){
            if(!getX(matriz, size, i, j)){
                sonindistinguibles = comprobarIndistinguible(afd, matriz, lookup, size, i, j);
                if(!sonindistinguibles){
                    insertarX(matriz, size, i, j, FALSE, FALSE);
                    cambiado = TRUE;
                }
            }
        }
        
    printMatriz(matriz, size, lookup, afd);
    /* Ha creado ya los indistinguibles (2s) y los setea a 1*/
    if (cambiado == TRUE)
        cierraConjuntos(matriz, size);
    
    
    return cambiado;
}


/**
 * Crea un afnd a partir de la semimatriz. Se llama depues de ejecutar el algoritmo sobre ella.
 * Usamos un ADT (NewState) para representar los nuevos estados (*Lo reusamos de la P1)
 */
AFND *obtenDeMatriz(AFND* original, char** matriz, int size, int* lookup_table){
    if(!original || !matriz){
        fprintf(stderr, "Error en argumentos de obtenDeMatriz");
        return NULL;
    }

    int numEstados = 0;
    NewState **nuevosEstados = NULL; // Array dinamico con los nuevos estados (formados por los conjuntos cocientes)
    
    int sizedonotcheck=0;
    int* donotcheck = NULL; //Aqui metemos los estados que ya se han incluido en algun conjunto cociente
                            // Para no tenerlos en cuenta mas veces
    int* temp = NULL;   // Array dinamico donde vamos metiendo los estados de un mismo conjunto cociente
                        // Una vez se termina un conjunto cociente, se usa para crear el NewState
    int temptam = 0;
    int dest;
    int skipstate = 0; // flag
    
    // Por cada elemento de la lookup table (los estados sin los inaccesibles)
    for(int i=0; i<size; i++){

        // Miramos si ya esta en un conjunto cociente
        skipstate = 0;
        for(int k=0; k<sizedonotcheck; k++){
            if(donotcheck[k] == i) {
               skipstate = 1;
               break;
            }
        }
        if (skipstate) continue;

        // Si no, se crea un conjunto cociente donde solo esta ese estado
        temp = append_int(temp, &temptam, lookup_table[i]);
        // Miramos que mas estados pertenecen a ese conjunto y los metemos ahi y en donotcheck
        // como ya explique antes
        for(int j=i+1; j<size; j++){
            if(!getX(matriz, size, i, j)){
                donotcheck = append_int(donotcheck, &sizedonotcheck, j);
                temp = append_int(temp, &temptam, lookup_table[j]);
            }
        }

        // Se añade un NewState a la lista de nuevos estados
        numEstados++;
        nuevosEstados = (NewState**)realloc(nuevosEstados, numEstados*sizeof(NewState*));
        BOOL inicial = FALSE;
        for(int u=0; u<temptam; u++){
            if(AFNDTipoEstadoEn(original, temp[u]) == INICIAL_Y_FINAL || AFNDTipoEstadoEn(original, temp[u]) == INICIAL)
                inicial = TRUE;
        }
        nuevosEstados[numEstados-1] = NewState_create(inicial, temp, temptam, original);
        temp = NULL;
        temptam = 0;
    }

    // Se genera un afnd a partir del array de nuevos estados
    AFND* nuevo = AFNDNuevo("minimizado", numEstados, AFNDNumSimbolos(original));

    for (int i=0; i<numEstados; ++i){
        printf("Nuevo Estado %s %d\n", NewState_getname(nuevosEstados[i]), NewState_gettype(nuevosEstados[i]));
        AFNDInsertaEstado(nuevo, NewState_getname(nuevosEstados[i]), NewState_gettype(nuevosEstados[i]));

    }

    for(int i=0; i<AFNDNumSimbolos(original); i++){
        AFNDInsertaSimbolo(nuevo, AFNDSimboloEn(original, i));
    }

    for (int i=0; i<numEstados; ++i){
        int firstate = NewState_getfirst(nuevosEstados[i]);
        for (int e=0; e<AFNDNumSimbolos(original); ++e) {
            dest = obtenTransicionConEntrada(original, firstate, e);
            if (dest != -1){
                for (int k=0; k<numEstados; ++k){
                    if (NewState_isIncluded(nuevosEstados[k], dest) == TRUE){

                        AFNDInsertaTransicion(nuevo, NewState_getname(nuevosEstados[i]), AFNDSimboloEn(original, e), NewState_getname(nuevosEstados[k]));
                    }
                }
            }
        }

    }

    // Liberamos recursos
    for (int i=0; i<numEstados; ++i){
        NewState_destroy(nuevosEstados[i]);
    }
    free(donotcheck);
    free(nuevosEstados);

    return nuevo;
}



AFND* AFNDMinimiza(AFND * afnd){
    
    if(!afnd){
        fprintf(stderr, "Error en arugmentos de AFNDMinimiza\n");
        return NULL;
    }
    
    if(AFNDNumEstados(afnd) < 1){
        fprintf(stderr, "Error en arugmentos de AFNDMinimiza: El automata no tiene estados\n");
        return NULL;
    }

    // Elimina inaccesibles
    int size;
    int *accesibles = EliminaInaccesible(afnd, &size);
    
    if (accesibles == NULL) {
        return NULL;
    }
    
    // Tal y como hemos implementado la matriz, si solo hay un estado se crearia 
    // una matriz de tamaño 0x0. Esto daria problema por lo que en este caso
    // devolvemos un afnd igual al que se pasa a la funcion
    // (Como tiene 1 estado ya esta minimizado)
    if(size == 1){
        AFND* nuevo = AFNDNuevo("minimizado", 1, AFNDNumSimbolos(afnd));
        AFNDInsertaEstado(nuevo, AFNDNombreEstadoEn(afnd, accesibles[0]), AFNDTipoEstadoEn(afnd, accesibles[0]));
        for(int i=0; i<AFNDNumSimbolos(afnd); i++){
            AFNDInsertaSimbolo(nuevo, AFNDSimboloEn(afnd, i));
            if(AFNDTransicionIndicesEstadoiSimboloEstadof(afnd, accesibles[0], i, accesibles[0])){
                AFNDInsertaTransicion(nuevo, AFNDNombreEstadoEn(afnd, accesibles[0]), AFNDSimboloEn(afnd, i) ,AFNDNombreEstadoEn(afnd, accesibles[0]));
            }
        }
        free(accesibles);
        return nuevo;
    }

    // Crea una semimatriz vacia (casi, ya que ya indicamos en ella que los estados
    // finales e iniciales y finales estan en otra clase de equivalencia (son distinguibles del resto))
    char **matriz = inicializaMatriz(afnd, accesibles, size);
    
    // Ejecutamos pasos del algortimo hasta que no se modifica la semimatriz
    BOOL modified = TRUE;
    while (modified == TRUE)
        modified = calculaConjuntos(afnd, matriz, accesibles, size);

    // Creamos un afnd nuevo a partir de la semimatriz
    AFND* nuevo = obtenDeMatriz(afnd, matriz, size, accesibles);

    // Liberamos recursos
    liberaMatriz(matriz, size);
    free(accesibles);

    return nuevo;
}



