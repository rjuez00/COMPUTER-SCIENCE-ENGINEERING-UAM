% EJERCICIO 1



write_log(S) :- open('error_logs.txt', append, Out), write(Out, S), write(Out, '\n'), close(Out).

/***************
* EJERCICIO 1. sum_pot_prod/4
*
*	ENTRADA:
*		X: Vector de entrada de numeros de valor real.
*		Y: Vector de entrada de numeros de valor real.
*		Potencia: Numero de valor entero, potencia.
*	SALIDA:
*		Resultado: Numero de valor real resultado de la operacion sum_pot_prod. 
*
****************/
% Both lists are correct
sum_pot_prod([], [], _, 0).

% One list is not empty, so they are not the same size
sum_pot_prod([], [_|_], _, _) :- print('ERROR 1.2 Longitud.'), !, fail.
sum_pot_prod([_|_], [], _, _) :- print('ERROR 1.2 Longitud.'), !, fail.

% Power is 0
sum_pot_prod(_, _, P, _) :- P<1, print('ERROR 1.1 Potencia'), !, fail.


% Recursive call that multiplies two elements (one of each list) between the, adds and powers them to POW, to then add 
% the result to the final solution
sum_pot_prod([E1|X], [E2|Y], POW, SOL) :- sum_pot_prod(X, Y, POW, OLDSOL), SOL is (OLDSOL)+(E1*E2)**POW, !.

/***************
* EJERCICIO 2. segundo_penultimo/3
*
*       ENTRADA:
*               L: Lista de entrada de numeros de valor real.
*       SALIDA:
*               X : Numero de valor real. Segundo elemento.
*		Y : Numero de valor real. Penultimo elemento.
*
****************/

% Calculates the penultimate element on the list
penult([X,_], X).
penult([_|L], X) :- penult(L, X).

% Calculates the second element on the list
seg([_|[X|_]], X).

% Calls the two functions that calculate the second and penultimate elements
segundo_penultimo(L, X, Y) :- seg(L, X), penult(L, Y), !.

% Only one element on the list
segundo_penultimo([_], _, _):- print('ERROR 2.1 Longitud.'), !, fail.

% No element on the list
segundo_penultimo([], _, _):- print('ERROR 2.1 Longitud.'), !, fail.


/***************
* EJERCICIO 3. sublista/5
*
*       ENTRADA:
*		L: Lista de entrada de cadenas de texto.
*		Menor: Numero de valor entero, indice inferior.
*		Mayor: Numero de valor entero, indice superior.
*		E: Elemento, cadena de texto.
*       SALIDA:
*		Sublista: Sublista de salida de cadenas de texto.
*
****************/

% Based on P18
% Slicing goes down on the recursion dropping the first element of the input list until it 
% reaches the first index, when it starts adding elements to the new list 
% (starting with the one on the first index) until it reaches the other index, when 
% it returns the list it has constructed between the two indexes.

slicing([], _, _, _) :- print("ERROR 3.2 Indices"), !, fail.

slicing([X], 1, 1, [X]).
slicing([X|_], 1, 1, [X]).
slicing([X|Xs], 1, K, [X|Ys]) :- K > 1, K1 is K -1, slicing(Xs, 1, K1, Ys).

% Menor is reduced to count until when we have to drop from the first part 
% Mayor is reduced because as the length is smaller now (after dropping the front part), the indexes change too
slicing([_|L], Menor, Mayor, Sublista) :- Menor > 1, Menor1 is Menor -1, Mayor1 is Mayor-1, slicing(L, Menor1, Mayor1, Sublista).


sublista(_, Menor, Mayor, _, _) :-  Menor > Mayor, print("ERROR 3.2 Indices"), !, fail.
sublista(_, Menor, _, _, _) :- Menor < 1, print("ERROR 3.2 Indices"), !, fail.
sublista(L, Menor, Mayor, E, Sublista) :- slicing(L, Menor, Mayor, Sublista), contiene(Sublista, E), !.


% Checks that th list has an element
contiene([E|_], E).
contiene([L|Ls], E) :- L \= E, contiene(Ls, E).


% Error Control

% The list does not contain the element E
contiene([], _) :- print('ERROR 3.1 Elemento'), !, fail.

% Check if the ranges are correct
% rangosCorrectos([L|Ls], Menor, Mayor) :- Mayor1 is Mayor-1, rangosCorrectos(Ls, Menor, Mayor1).
% rangosCorrectos([], Menor, Mayor) :- Mayor >= 1, 
% rangosCorrectos([], Menor, Mayor) :- Menor < 1, print("ERROR 3.2 Indices"), !, fail.

/***************
* EJERCICIO 4. espacio_lineal/4
*
*       ENTRADA:
*               Menor: Numero de valor entero, valor inferior del intervalo.
*               Mayor: Numero de valor entero, valor superior del intervalo.
*               Numero_elementos: Numero de valor entero, numero de valores de la rejilla.
*       SALIDA:
*               Rejilla: Vector de numeros de valor real resultante con la rejilla.
*
****************/

% Error Control
espacio_lineal(I, I, 1, I).
espacio_lineal(I, K, _, _) :-  I > K, print("ERROR 4.1 Indices"), !, fail.
espacio_lineal(I, K, N, _) :-  N < 2, I =\= K, print("ERROR 4.2 Longitud"), !, fail.




% To calculate the jumps: (Mayor-Menor)/(Numero_elementos -1)

% Each time we go down on the recursion level the jump is calculated
% WE go down on the recursion until we reach I=K, when we start going up inserting on the list the elements calculated on each recursion level
espacio_lineal(I, K, 1, [SOL]) :- I =:= K, SOL is I/1.
espacio_lineal(I, K, N, [I|Rejilla]) :- N > 1, I1 is (I+(K-I)/(N-1)), N1 is N-1, espacio_lineal(I1, K, N1, Rejilla), !.



/***************
* EJERCICIO 5. normalizar/2
*
*       ENTRADA:
*		Distribucion_sin_normalizar: Vector de numeros reales de entrada. Distribucion sin normalizar.
*       SALIDA:
*		Distribucion: Vector de numeros reales de salida. Distribucion normalizada.
*
****************/

% Calculates z, which is the number by which all numbers on the distribution must be divided to obtain the normalized version
calcula_z([], 0).
calcula_z([X|L], SOL) :- calcula_z(L, Z), SOL is Z+X.


% Divides all numbers on the distribution by z
dividir_todos([], _, []).
dividir_todos([X|L], Z, [Dividido|NewList]) :- X >= 0, dividir_todos(L, Z, NewList), Dividido is X/Z.

% Error in case any of the numbers on the distribution is negative
dividir_todos([X|_], _, _) :- X < 0, print("ERROR 5.1 Negativos"), !, fail.

% First calculates z (calcula_z()) and then normalizes the distribution (dividir_todos())
normalizar(Distribucion_sin_normalizar, Distribucion) :- calcula_z(Distribucion_sin_normalizar, Z), dividir_todos(Distribucion_sin_normalizar, Z, Distribucion), !.

/***************
* EJERCICIO 6. divergencia_kl/3
*
*       ENTRADA:
*		D1: Vector de numeros de valor real. Distribucion.
*		D2: Vector de numeros de valor real. Distribucion.
*       SALIDA:
*		KL: Numero de valor real. Divergencia KL.
*
****************/

% Error in case one of the lists is longer than the other
divergencia_kl_calcular([_|_], [], _) :- print("ERROR 6.3. Longitud"), !, fail.
divergencia_kl_calcular([], [_|_], _) :- print("ERROR 6.3. Longitud"), !, fail.


% Goes down on recursion levels separating X and Y, and when it goes up it calculates the sum
divergencia_kl_calcular([], [], 0).
divergencia_kl_calcular([X|L], [Y|K], SOL) :- X > 0, Y > 0, divergencia_kl_calcular(L, K, Z), SOL is Z+X*log(X/Y).

% Error in case any of the distributions has a 0
divergencia_kl_calcular([X|_], [_|_], _) :- X =:= 0, print("ERROR 6.1. Divergencia KL no definida"), !, fail.
divergencia_kl_calcular([_|_], [Y|_], _) :- Y =:= 0, print("ERROR 6.1. Divergencia KL no definida"), !, fail.

% Error in case there is any negative number
divergencia_kl_calcular([X|_], [_|_], _) :- X < 0, print("ERROR 6.2. Divergencia KL definida solo para distribuciones"), !, fail.
divergencia_kl_calcular([_|_], [Y|_], _) :- Y < 0, print("ERROR 6.2. Divergencia KL definida solo para distribuciones"), !, fail.


% Checks if a distribution sums 1 by adding all elements on it
comprueba_suma([], N) :- N =:= 1.
% Error in case it does not sum 1
comprueba_suma([], N) :- N =\= 1, print("ERROR 6.2. Divergencia KL definida solo para distribuciones"), !, fail.
comprueba_suma([X|L], N) :- N1 is N+X, comprueba_suma(L, N1).


% Function that first checks if both distributions sum 1 (comprueba_suma()), and then calculates the divergence (divergencia_kl_calcular())
divergencia_kl(X, Y, SOL) :- comprueba_suma(X, 0), comprueba_suma(Y, 0), divergencia_kl_calcular(X, Y, SOL), !.

/*-------------------------Checkear longitud-----------------------------------------------------------------------*/

/***************
* EJERCICIO 7. producto_kronecker/3
*
*       ENTRADA:
*		Matriz_A: Matriz de numeros de valor real.
*		Matriz_B: Matriz de numeros de valor real.
*       SALIDA:
*		Matriz_bloques: Matriz de bloques (matriz de matrices) de numeros reales.
*
****************/
% We designed a formula to decompose, and is multiplying an inmutable element by something that we keep looping
% the functions are called: inmutableElement_loopableElement(inmutableElement, loopableElement, result)


% Multiplies a row by a number (N)
int_fila(_, [], []).
int_fila(N, [X|L], [Y|K]) :- N >= 0, X >= 0, int_fila(N, L, K), Y is X*N.

% Error control (as its the smallest operation we only have to check it here)
int_fila(N, _, _) :- N < 0, print("ERROR 7.1. Elemento menor que 0"), !, fail.
int_fila(_, [X|_], _) :- X < 0, print("ERROR 7.1. Elemento menor que 0"), !, fail.


% Multiplies a matrix (list of lists), by a number (N) using the function implemented before to multiply
% each row by N
int_matriz(_, [], []).
int_matriz(N, [X|L], [Y|K]) :- int_matriz(N, L, K), int_fila(N, X, Y).


% Multiplies the matrix M by each of the numbers of a row using the previous function, generating
% as many matrixes as numbers are in the row
matriz_fila(_, [], []).
matriz_fila(M, [X|L], [Y|K]) :- matriz_fila(M, L, K), int_matriz(X, M, Y).


% Obtains the Kronecker product using the previous function to multiply each of the rows of the first matrix by the second one
% In this case we do not use the same format as in the others, now the inmutable element (the second matrix) is in the second argument
producto_kronecker([], _, []).
producto_kronecker([FilasMatriz|CyclingMatriz], StaticM, [Y|K]) :- producto_kronecker(CyclingMatriz, StaticM, K), matriz_fila(StaticM, FilasMatriz, Y), !.




/***************
* EJERCICIO 8a. distancia_euclidea/3
*
*       ENTRADA:
*               X1: Vector de numeros de valor real. 
*               X2: Vector de numeros de valor real.
*       SALIDA:
*               D: Numero de valor real. Distancia euclidea.
*
****************/
% Error in case the length is different
suma([_|_], [], _) :- print("ERROR 8a.1. Longitud"), !, fail.
suma([], [_|_], _) :- print("ERROR 8a.1. Longitud"), !, fail.

suma([], [], 0).
suma([X1 | L1], [X2 | L2], SOL) :- suma(L1, L2, D), SOL is (X1-X2)**2 + D.

% Calculates the euclidean distance between X and Y
distancia_euclidea(X, Y, D) :- suma(X, Y, S), D is sqrt(S).

/***************
* EJERCICIO 8b. calcular_distancias/3
*
*       ENTRADA:
*               X_entrenamiento: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector.
*               X_test: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector. Instancias sin etiquetar.
*       SALIDA:
*               Matriz_resultados: Matriz de numeros de valor real donde cada fila es un vector con la distancia de un punto de test al conjunto de entrenamiento X_entrenamiento.
*
****************/

fila_matriz(_, [], []).
fila_matriz(F, [X|L], [Y|M]) :- fila_matriz(F, L, M), distancia_euclidea(F, X, Y).

% Calculates euclidean distances between the test matrix and the trained matrix
calcular_distancias(_, [], []).
calcular_distancias(M, [F|L], [Y|K]) :- calcular_distancias(M, L, K), fila_matriz(F, M, Y).


/***************
* EJERCICIO 8c. predecir_etiquetas/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Matriz_resultados: Matriz de numeros de valor real donde cada fila es un vector con la distancia de un punto de test al conjunto de entrenamiento X_entrenamiento.
*       SALIDA:
*               Y_test: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_test.
*
****************/
% Goes distance vector to distance vector calculating the predicted tag
predecir_etiquetas(_, _, [], []).
predecir_etiquetas(E, K, [D|Ds], [PREDICTED|SOL]) :- predecir_etiquetas(E, K, Ds, SOL), predecir_etiqueta(E, K, D, PREDICTED).

/***************
* EJERCICIO 8d. predecir_etiqueta/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Vec_distancias: Vector de valores reales correspondiente a una fila de Matriz_resultados.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
****************/
% Call first the list that calculates the nearest lables and select the one with most elements 
predecir_etiqueta(Y_entrenamiento, K, Vec_distancias, Etiqueta) :- calcular_K_etiquetas_mas_relevantes(Y_entrenamiento, K, Vec_distancias, Etiquetas_relevantes), 
                                                                   calcular_etiqueta_mas_relevante(Etiquetas_relevantes, Etiqueta).

/***************
* EJERCICIO 8e. calcular_K_etiquetas_mas_relevantes/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Vec_distancias: Vector de valores reales correspondiente a una fila de Matriz_resultados.
*       SALIDA:
*		K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*
****************/
% NOTE: The output that is produced has the same elements but not the same order as in the assignment.
% This implementation appeare to be the most legible and as its not necessary to know the order to implement the algorithm we decided to leave it like that.
% Also our order is more correct as its ordered from less to most relevant. 

% It keeps looping through the list going down recursion levels as it eliminates the most important elements and pass them to the next level
% When we go up on the recursion we recompose the final solution with the solutions we extracted on each level
calcular_K_etiquetas_mas_relevantes(_, 0, _, []).
calcular_K_etiquetas_mas_relevantes(Xs, K, Ds, [ELEM|SOLs]) :- encontrar_menor_distancia(Xs, Ds, ELEM, ELEMD), eliminar_elemento(Xs, Ds, ELEM, ELEMD, NEWXs, NEWDs), K1 is K-1, calcular_K_etiquetas_mas_relevantes(NEWXs, K1, NEWDs, SOLs).


% Simple function to eliminate elements of a list, as they can be repeated we also pass the distance to be eliminated from both
% There is no problem if there are two elements of the same lable and distance, does not matter which of them we eliminate
% it goes down inthe recursion while it looks for that element and when it reaches it its excluded from the recomposition
eliminar_elemento([X|Xs], [D|Ds], X, D, Xs, Ds).
eliminar_elemento([X|Xs], [D|Ds], ELEM, ELEMD, [X|NEWXs], [D|NEWDs]) :- eliminar_elemento(Xs, Ds, ELEM, ELEMD, NEWXs, NEWDs).

% Error check in case we receive more distances than lables or viceversa
encontrar_menor_distancia([], [_|_], _, _, _, _) :- print('ERROR 9.1 Longitud'), !, fail.
encontrar_menor_distancia([_|_], [], _, _, _, _) :- print('ERROR 9.1 Longitud'), !, fail.

% Finds the solution going down on the recursion and storing the lowest (we cakk it MAXTAG for habit, but it should be MINTAG)
% when it reaches the root it goes up and returns the element it found and the distance (so that we can find it after)
encontrar_menor_distancia([], [], MAXTAG, MAXCOUNT, MAXTAG, MAXCOUNT).
encontrar_menor_distancia([X|Xs], [D|Ds], _, MAXD, SOL, SOLD) :- D < MAXD, encontrar_menor_distancia(Xs, Ds, X, D, SOL, SOLD).
encontrar_menor_distancia([_|Xs], [D|Ds], MAXTAG, MAXD, SOL, SOLD) :- D >= MAXD, encontrar_menor_distancia(Xs, Ds, MAXTAG, MAXD, SOL, SOLD).
encontrar_menor_distancia([X|Xs], [D|Ds], SOL, SOLD) :- encontrar_menor_distancia(Xs, Ds, X, D, SOL, SOLD).


/***************
* EJERCICIO 8f. calcular_etiqueta_mas_relevante/2
*
*       ENTRADA:
*               K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
****************/

% Uses the functions implemented below to obtain the most relevant lable
calcular_etiqueta_mas_relevante(K_etiquetas, Etiqueta) :- calcular_contadores(K_etiquetas, TUPLAS), my_max(TUPLAS, [Etiqueta, _]).

% Calculates the lable with the highgest counter 
my_max([], R, R). 
my_max([[ELEM, CONT]|Xs], [_, CONTMAX], R):- CONT > CONTMAX, my_max(Xs, [ELEM, CONT], R).
my_max([[_, CONT]|Xs], [ELEMMAX, CONTMAX], R):- CONT =< CONTMAX, my_max(Xs, [ELEMMAX, CONTMAX], R).
my_max([X|Xs], R):- my_max(Xs, X, R).


% Combines the creation of a tuple and the adding of the counter
calcular_contadores([], []).
calcular_contadores([X|L], TUPLAS) :- calcular_contadores(L, NEWTUPLAS), comprobar_existencia(X, NEWTUPLAS, NEWNEWTUPLAS), calcular_contador(X, NEWNEWTUPLAS, TUPLAS).


% Increase an existing tuple
calcular_contador(_, [], []).
calcular_contador(ELEM, [[ELEM, CONT] | LISTATUPLAS], [[ELEM, CONT1]|K]) :- CONT1 is CONT+1, calcular_contador(ELEM, LISTATUPLAS, K).
calcular_contador(ELEM, [X | LISTATUPLAS], [X|K]) :- calcular_contador(ELEM, LISTATUPLAS, K).

% Create new tuple in case a label was not included on the counting list
comprobar_existencia(ELEM, [], [[ELEM, 0]]).
comprobar_existencia(ELEM, [[ELEM, COUNT] | LISTATUPLAS], [[ELEM, COUNT] | LISTATUPLAS]).
comprobar_existencia(ELEM, [[X, COUNT] | LISTATUPLAS], [[X, COUNT]|K]) :- comprobar_existencia(ELEM, LISTATUPLAS, K).

/***************
* EJERCICIO 8g. k_vecinos_proximos/5
*
*       ENTRADA:
*		X_entrenamiento: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector.
*		Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*		K: Numero de valor entero.
*		X_test: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector. Instancias sin etiquetar.
*       SALIDA:
*		Y_test: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_test.
*
****************/

% Calls calcular_distancias to obtain the results matrix and then predict tags to obtain the predictions
k_vecinos_proximos(X_entrenamiento, Y_entrenamiento, K, X_test, Y_test) :- calcular_distancias(X_entrenamiento, X_test, Matriz_resultados), predecir_etiquetas(Y_entrenamiento, K, Matriz_resultados, Y_test), !.






