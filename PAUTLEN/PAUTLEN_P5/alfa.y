%{
#include <stdio.h>
#include <string.h>
#include "alfa.h"
#include "generacion.h"
#include "SymbolTable.h"


extern int yylex();
extern FILE* yyout;
int yyerror();
extern int column, row;
SymbolTable* table;
int tipo_actual;
int clase_actual;
int tamanio_vector_actual;

int pos_parametro_actual;
int pos_variable_local_actual = -1;
int num_variables_locales_actual;
int num_parametros_actual;
int num_parametros_llamada_actual;
int tipo_retorno;
int has_return;

int islocal;
int counttag;
int en_explist;
%}

%union
{
	tipo_atributo atributos;
}

/* Identificadores*/
%token <atributos> TOK_IDENTIFICADOR
%token <atributos> TOK_CONSTANTE_ENTERA


%token TOK_MAIN
%token TOK_INT
%token TOK_BOOLEAN
%token TOK_ARRAY
%token TOK_FUNCTION
%token TOK_IF
%token TOK_ELSE
%token TOK_WHILE
%token TOK_SCANF
%token TOK_PRINTF
%token TOK_RETURN

/* Simbolos */
%token TOK_PUNTOYCOMA
%token TOK_COMA
%token TOK_PARENTESISIZQUIERDO
%token TOK_PARENTESISDERECHO
%token TOK_CORCHETEIZQUIERDO
%token TOK_CORCHETEDERECHO
%token TOK_LLAVEIZQUIERDA
%token TOK_LLAVEDERECHA
%token TOK_ASIGNACION
%token TOK_MAS
%token TOK_MENOS
%token TOK_DIVISION
%token TOK_ASTERISCO
%token TOK_AND
%token TOK_OR
%token TOK_NOT
%token TOK_IGUAL
%token TOK_DISTINTO
%token TOK_MENORIGUAL
%token TOK_MAYORIGUAL
%token TOK_MENOR
%token TOK_MAYOR

/* Constantes */ 
%token TOK_TRUE
%token TOK_FALSE

/* Error */
%token TOK_ERROR

/* Precedence */
%left TOK_MAS TOK_MENOS TOK_OR
%left TOK_ASTERISCO TOK_DIVISION TOK_AND
%right TOK_NOT MENOSU


/* resto de los tokens sin valor */
/* semántico */

%type <atributos> condicional
%type <atributos> comparacion
%type <atributos> elemento_vector
%type <atributos> exp
%type <atributos> constante
%type <atributos> constante_entera
%type <atributos> constante_logica
%type <atributos> identificador
%type <atributos> if_exp
%type <atributos> if_exp_sentencias
%type <atributos> tipo
%type <atributos> funcion
%type <atributos> bucle
%type <atributos> while_exp
%type <atributos> while
%type <atributos> fn_name
%type <atributos> fn_declaration
%type <atributos> idf_llamada_funcion

/* resto de los no terminales */
/* con atributos semánticos */


%%
programa: iniciotable TOK_MAIN TOK_LLAVEIZQUIERDA escritura1 declaraciones escritura_funciones funciones escritura_main sentencias TOK_LLAVEDERECHA {
	fprintf(yyout,";R1:\t<programa> ::= main { <declaraciones> <funciones> <sentencias> }\n" );
	escribir_fin(yyout);
	SymbolTable_free(table);
};

escritura1: {
	escribir_subseccion_data(yyout);
	escribir_cabecera_bss(yyout);
};

escritura_funciones: {
		escribir_segmento_codigo(yyout);
}

escritura_main: { /*R1*/
	escribir_inicio_main(yyout);
};

iniciotable: {
	table = SymbolTable_new();
	islocal = 0;
	counttag = 1;
	if(!table){
		fprintf(stderr, "Not enough memory.\n");
		SymbolTable_free(table);
		 return -1;
	}
};

declaraciones: declaracion {fprintf(yyout,";R2:\t<declaraciones> ::= <declaracion>\n");}
| declaracion declaraciones {fprintf(yyout,";R3:\t<declaraciones> ::= <declaracion> <declaraciones>\n");};

declaracion: clase identificadores TOK_PUNTOYCOMA {	/*R4*/ };

clase: clase_escalar {
	fprintf(yyout,";R5:\t<clase> ::= <clase_escalar>\n");
	clase_actual=SCALAR;
}
| clase_vector {
	fprintf(yyout,";R7:\t<clase> ::= <clase_vector>\n");
	clase_actual=VECTOR;
};

clase_escalar: tipo { fprintf(yyout,";R9:\t<clase_escalar> ::= <tipo>\n"); };

tipo: TOK_INT { fprintf(yyout,";R10:\t<tipo> ::= int\n"); tipo_actual = INT; $$.tipo = INT; }
| TOK_BOOLEAN { fprintf(yyout,";R11:\t<tipo> ::= boolean\n"); tipo_actual = BOOLEAN; $$.tipo = BOOLEAN; };

clase_vector: TOK_ARRAY tipo TOK_CORCHETEIZQUIERDO TOK_CONSTANTE_ENTERA TOK_CORCHETEDERECHO {
	fprintf(yyout,";R15:\t<tipo> ::= array <tipo>[ TOK_CONSTANTE_ENTERA ]\n");
	if ($4.valor_entero < 1 || $4.valor_entero > MAX_TAMANIO_VECTOR) {
		fprintf(stderr, "****Error semantico en lin %d: El tamanyo del vector <nombre_vector> excede los limites permitidos (1,%d).\n", row, MAX_TAMANIO_VECTOR);
		SymbolTable_free(table);
		 return -1;
	}

	tamanio_vector_actual = $4.valor_entero;
};

identificadores: identificador {fprintf(yyout,";R18:\t<identificadores> ::= <identificador>\n");}
| identificador TOK_COMA identificadores {fprintf(yyout,";R19:\t<identificadores> ::= <identificador> , <identificadores>\n");};

funciones: funcion funciones { fprintf(yyout,";R20:\t<left> ::= <funcion> <funciones>\n");}
| /* empty */ { fprintf(yyout,";R21:\t<funciones> ::=\n"); };

fn_name: TOK_FUNCTION tipo TOK_IDENTIFICADOR{
	/* check if it exists in the current context */
	fprintf(yyout, ";R22.2 \t fn_name");
	if(SymbolTable_get(table, $3.lexema) != NULL) {
		fprintf(stderr, "****Error semantico en lin %d: Declaracion duplicada.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	has_return = 0;
	islocal = 1;
	SymbolTable_to_local(table, $3.lexema, -1, tipo_actual, SCALAR, -1, -1, -1, -1);
	num_variables_locales_actual = 0;
	pos_variable_local_actual = 1;
	num_parametros_actual = 0;
	pos_parametro_actual = 0;
	tipo_retorno = $2.tipo;
	strcpy($$.lexema, $3.lexema);
};

funcion: fn_declaration sentencias TOK_LLAVEDERECHA {
	fprintf(yyout,";R22:\t<funcion> ::= function <tipo> <identificador> ( <parametros_funcion> ) { <declaraciones_funcion> <sentencias> }\n");
	if (!has_return) {
		fprintf(stderr, "****Error semantico en lin %d: Funcion %s sin sentencia de retorno.\n", row, $1.lexema);
		SymbolTable_free(table);
		 return -1;
	}
	SymbolTable_to_global(table);
	DataItem * item = SymbolTable_get(table, $1.lexema);
	DataItem_set_num_params(item, num_parametros_actual);
	// we get out of function
	islocal = 0;
	pos_variable_local_actual = -1;
	num_variables_locales_actual = -1;
};


fn_declaration: fn_name TOK_PARENTESISIZQUIERDO parametros_funcion TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA declaraciones_funcion {
	declararFuncion(yyout, $1.lexema, num_variables_locales_actual);
	DataItem * item = SymbolTable_get(table, $1.lexema);
	DataItem_set_num_params(item, num_parametros_actual);
	strcpy($$.lexema, $1.lexema);
};


parametros_funcion: parametro_funcion resto_parametros_funcion { fprintf(yyout,";R23:\t<resto_parametros_funcion> ::= ; <parametro_funcion> <resto_parametros_funcion>\n"); }
| /* empty */ { fprintf(yyout,";R24:\t<parametros_funcion> ::=\n"); };

resto_parametros_funcion: TOK_PUNTOYCOMA parametro_funcion resto_parametros_funcion {/* R25 */}
| /* empty */ {fprintf(yyout,";R26:\t<resto_parametros_funcion> ::=\n");};

parametro_funcion: tipo idpf {
	fprintf(yyout,";R27:\t<parametro_funcion> ::= <tipo> <identificador>\n");
	pos_parametro_actual++;
	num_parametros_actual++;
 };

/* RULE FOR PARAMETER OF FUNCTION */
idpf: TOK_IDENTIFICADOR {
	fprintf(yyout,";R27.2:\t<parametro_funcion> ::= <tipo> <identificador>\n");

	/* check if it's duped by just adding it to the symbol table */
	if (SymbolTable_add(table, $1.lexema, 0, PARAMETER, tipo_actual, SCALAR, -1, num_parametros_actual, -1, -1) == ERROR) {
		fprintf(stderr, "****Error semantico en lin %d: Declaracion duplicada.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
 };

declaraciones_funcion: declaraciones {fprintf(yyout,";R28:\t<declaraciones_funcion> ::= <declaraciones>\n");} 
 | /* empty */ {fprintf(yyout,";R29:\t<declaraciones_funcion> ::=\n");};

sentencias: sentencia {fprintf(yyout,";R30:\t<sentencias> ::= <sentencia>\n");}
 | sentencia sentencias {fprintf(yyout,";R31:\t<sentencias> ::= <sentencia> <sentencias>\n");};

sentencia: sentencia_simple TOK_PUNTOYCOMA {fprintf(yyout,";R32:\t<sentencia> ::= <sentencia_simple> ;\n");}
 | bloque {fprintf(yyout,";R33:\t<sentencia> ::= <bloque>\n");};


sentencia_simple: asignacion {fprintf(yyout,";R34:\t<sentencia_simple> ::= <asignacion>\n");}
 | lectura {fprintf(yyout,";R35:\t<sentencia_simple> ::= <lectura>\n");}
 | escritura {fprintf(yyout,";R36:\t<sentencia_simple> ::= <escritura>\n");}
 | retorno_funcion {
	fprintf(yyout,";R38:\t<sentencia_simple> ::= <retorno_funcion>\n");
  };

bloque: condicional {fprintf(yyout,";R40:\t<bloque> ::= <condicional>\n");}
| bucle {fprintf(yyout,";R41:\t<bloque> ::= <bucle>\n");};

asignacion: TOK_IDENTIFICADOR TOK_ASIGNACION exp {
	fprintf(yyout,";R43:\t<asignacion> ::= <identificador> = <exp>\n");
	DataItem * item = SymbolTable_get(table, $1.lexema);
	if (item == NULL) {
		fprintf(stderr, "****Error semantico en lin %d: Acceso a variable no declarada (%s).\n", row, $1.lexema);
		SymbolTable_free(table);
		 return -1;
	}
	int cat = DataItem_get_category(item);
	int type = DataItem_get_type(item);
	int elem = DataItem_get_element_category(item);

	if (elem == FUNCTION || cat == VECTOR 
	|| type != $3.tipo) {
		fprintf(stderr, "****Error semantico en lin %d: Asignacion incompatible.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	short local_pos = DataItem_get_pos_local_variable(item);
	if (local_pos > 0) { /* if more than 0, it's a local variable */
		escribirVariableLocal(yyout, local_pos);
		asignarDestinoEnPila(yyout, $3.es_direccion);
	} else if (elem == PARAMETER) {
		/* it's a parameter being assigned to */
		short param_pos = DataItem_get_pos_param(item);
		escribirParametro(yyout, param_pos, num_parametros_actual);
		asignarDestinoEnPila(yyout, $3.es_direccion);
	} else { /* it's a global variable being assigned to */
		asignar(yyout, $1.lexema, $3.es_direccion);
	}}



 | elemento_vector TOK_ASIGNACION exp { fprintf(yyout,";R44:\t<asignacion> ::= <elemento_vector> = <exp>\n");
	if($3.tipo != $1.tipo){
		fprintf(stderr, "****Error semantico en lin %d: Asignacion incompatible.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	
	asignarDestinoEnPila_paraVector(yyout, $3.es_direccion);
 };

elemento_vector: TOK_IDENTIFICADOR TOK_CORCHETEIZQUIERDO exp TOK_CORCHETEDERECHO {
	fprintf(yyout,";R48:\t<elemento_vector> ::= <identificador> [ <exp> ]\n");
	if ($3.tipo != INT) {
		fprintf(stderr, "****Error semantico en lin %d: El indice en una operacion de indexacion tiene que ser de tipo entero.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	DataItem * item = SymbolTable_get(table, $1.lexema);
	if(!item){
		fprintf(stderr, "****Error semantico en lin %d: Acceso a variable no declarada (%s).\n", row, $1.lexema);
		SymbolTable_free(table);
		 return -1;
	}
	if(DataItem_get_category(item) != VECTOR){
		fprintf(stderr, "****Error semantico en lin %d: Intento de indexacion de una variable que no es de tipo vector.\n", row);
		SymbolTable_free(table); 
		 return -1;
	}

	
	$$.tipo =  DataItem_get_type(item);
	$$.es_direccion = 1;
	escribir_elemento_vector(yyout, $1.lexema, DataItem_get_value(item), $3.es_direccion);
 };

condicional: if_exp_sentencias {
	ifthenelse_fin(yyout, $1.etiqueta);
	fprintf(yyout,";R50:\t<condicional> ::= if ( <exp> ) { <sentencias> }\n");
	}
 | if_exp_sentencias TOK_ELSE TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA {
	ifthenelse_fin(yyout, $1.etiqueta);
	fprintf(yyout,";R51:\t<condicional> ::= if ( <exp> ) { <sentencias> } else { <sentencias> }\n");
	};


if_exp: TOK_IF TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA {
	fprintf(yyout,";R51.2:\t<condicional> ::= if ( <exp> ) { <sentencias> } else { <sentencias> }\n");
	if($3.tipo == INT){
		fprintf(stderr, "****Error semantico en lin %d: Condicional con condicion de tipo int.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	$$.etiqueta = counttag;
	counttag++;
	// we can't predict it will or not have an else
	// so we just do ifthenelse
	ifthenelse_inicio(yyout, $3.es_direccion, $$.etiqueta);
};



if_exp_sentencias: if_exp sentencias TOK_LLAVEDERECHA {
	fprintf(yyout,";R51.1:\t<condicional> ::= if ( <exp> ) { <sentencias> } else { <sentencias> }\n");
	$$.etiqueta = $1.etiqueta;
	ifthenelse_fin_then(yyout, $$.etiqueta);
};



bucle: while_exp sentencias TOK_LLAVEDERECHA {
	fprintf(yyout,";R52:\t<bucle> ::= while ( <exp> ) { <sentencias> }\n");
	while_fin(yyout, $1.etiqueta);
};

while: TOK_WHILE TOK_PARENTESISIZQUIERDO{
	fprintf(yyout,";R52.2:\t<bucle> ::= while ( <exp> ) { <sentencias> }\n");
	$$.etiqueta = counttag;
	counttag++;
	while_inicio(yyout, $$.etiqueta);
};

while_exp: while exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA {
	fprintf(yyout,";R52.3:\t<bucle> ::= while ( <exp> ) { <sentencias> }\n");
	if($2.tipo == INT){
		fprintf(stderr, "****Error semantico en lin %d: Bucle con condicion de tipo int.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	
	$$.etiqueta = $1.etiqueta;
	while_exp_pila(yyout, $2.es_direccion, $1.etiqueta);
	
};

lectura: TOK_SCANF TOK_IDENTIFICADOR {
	fprintf(yyout,";R54:\t<lectura> ::= scanf <identificador>\n");
	DataItem * item = SymbolTable_get(table, $2.lexema);

	if(!item){
		fprintf(stderr, "****Error semantico en lin %d: Acceso a variable no declarada (%s).\n", row, $2.lexema);
		SymbolTable_free(table);
		 return -1;
	}
	int cat = DataItem_get_category(item);
	int elem = DataItem_get_element_category(item);
	if(cat == FUNCTION || cat == VECTOR){
		fprintf(stderr, "****Error semantico en lin %d: Asignacion incompatible.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	int pos = elem == PARAMETER ? DataItem_get_pos_param(item) : DataItem_get_pos_local_variable(item);
	if (pos >= 0) {
		if (elem == PARAMETER) {
			escribirParametro(yyout, pos, num_parametros_actual);
		} else {
			escribirVariableLocal(yyout, pos);
		}
		leer_local(yyout, pos, DataItem_get_type(item));
	} else {
		leer(yyout, $2.lexema, DataItem_get_type(item));
	}
};

escritura: TOK_PRINTF exp {
	fprintf(yyout,";R56:\t<escritura> ::= printf <exp>\n");
	escribir(yyout, $2.es_direccion, $2.tipo);
};

retorno_funcion: TOK_RETURN exp {
	fprintf(yyout,";R61:\t<retorno_funcion> ::= return <exp>\n");
	if(!islocal){
		fprintf(stderr, "****Error semantico en lin %d: Sentencia de retorno fuera del cuerpo de una función.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	if($2.tipo != tipo_retorno){
		fprintf(stderr, "****Error semantico en lin %d: Asignacion incompatible.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	has_return = 1;
	retornarFuncion(yyout, $2.es_direccion);
};

exp: exp TOK_MAS exp {
	fprintf(yyout,";R72:\t<exp> ::= <exp> + <exp>\n");
	if($1.tipo == BOOLEAN || $3.tipo == BOOLEAN){
		fprintf(stderr, "****Error semantico en lin %d: Operacion aritmetica con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
		}
	$$.tipo = INT;
	$$.es_direccion = FALSE;
	sumar(yyout, $1.es_direccion, $3.es_direccion);
 	}
| exp TOK_MENOS exp {
	fprintf(yyout,";R73:\t<exp> ::= <exp> - <exp>\n");
	if($1.tipo == BOOLEAN || $3.tipo == BOOLEAN){
		fprintf(stderr, "****Error semantico en lin %d: Operacion aritmetica con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
		}
	$$.tipo = INT;
	$$.es_direccion = FALSE;
	restar(yyout, $1.es_direccion, $3.es_direccion);
	}
| exp TOK_DIVISION exp {
	fprintf(yyout,";R74:\t<exp> ::= <exp> / <exp>\n");
	if($1.tipo == BOOLEAN || $3.tipo == BOOLEAN){
		fprintf(stderr, "****Error semantico en lin %d: Operacion aritmetica con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
		}
	$$.tipo = INT;
	$$.es_direccion = FALSE;

	dividir(yyout, $1.es_direccion, $3.es_direccion);
 }
| exp TOK_ASTERISCO exp {
	fprintf(yyout,";R75:\t<exp> ::= <exp> * <exp>\n");
	if($1.tipo == BOOLEAN || $3.tipo == BOOLEAN){
		fprintf(stderr, "****Error semantico en lin %d: Operacion aritmetica con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
		}
	$$.tipo = INT;
	$$.es_direccion = FALSE;

	multiplicar(yyout, $1.es_direccion, $3.es_direccion);
 }
| TOK_MENOS exp %prec MENOSU {
	fprintf(yyout,";R76:\t<exp> ::= <exp> - <exp>\n");
	if($2.tipo == BOOLEAN){
		fprintf(stderr, "****Error semantico en lin %d: Operacion aritmetica con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
		}
	$$.tipo = INT;
	$$.es_direccion = FALSE;

	cambiar_signo(yyout, $2.es_direccion);

 }
| exp TOK_AND exp {
	fprintf(yyout,";R77:\t<exp> ::= <exp> && <exp>\n");
	if($1.tipo == INT || $3.tipo == INT){
		fprintf(stderr, "****Error semantico en lin %d: Operacion logica con operandos int.\n", row);
		SymbolTable_free(table);
		 return -1;
		}
	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
	y(yyout, $1.es_direccion, $3.es_direccion);
 }
| exp TOK_OR exp {
	fprintf(yyout,";R78:\t<exp> ::= <exp> || <exp>\n");
	
	if($1.tipo == INT || $3.tipo == INT){
		fprintf(stderr, "****Error semantico en lin %d: Operacion logica con operandos int.\n", row);
		SymbolTable_free(table);
		 return -1;
		}
	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
	o(yyout, $1.es_direccion, $3.es_direccion);
 }
| TOK_NOT exp {
	fprintf(yyout,";R79:\t<exp> ::= ! <exp>\n");
	if($2.tipo == INT){
		fprintf(stderr, "****Error semantico en lin %d: Operacion logica con operandos int.\n", row);
		SymbolTable_free(table);
		 return -1;
		}
	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
	no(yyout, $2.es_direccion, counttag);
	counttag++;
 }

| TOK_IDENTIFICADOR {
	fprintf(yyout,";R80:\t<exp> ::= <identificador>\n");
	DataItem * item = SymbolTable_get(table, $1.lexema);
	if(!item){
		fprintf(stderr, "****Error semantico en lin %d: Acceso a variable no declarada (%s).\n", row, $1.lexema);
		SymbolTable_free(table);
		 return -1;
	}
	int cat = DataItem_get_category(item);
	int type = DataItem_get_type(item);
	int elem = DataItem_get_element_category(item);
	if(elem == FUNCTION || cat == VECTOR){
		fprintf(stderr, "****Error semantico en lin %d: Asignacion incompatible.\n", row);
		SymbolTable_free(table);
		 return -1;
	}


	$$.tipo=type;
	$$.es_direccion=TRUE;    /* ES UNA VARIABLE */
	/* Escritura en ensamblador de la introduccion en la pila de la dirección del identificador: push dword  _$1.lexema */
	if(islocal){ /* Local variable */

		if(elem == PARAMETER){
			escribirParametro(yyout, DataItem_get_pos_param(item), num_parametros_actual);
		} else {
			escribirVariableLocal(yyout, DataItem_get_pos_local_variable(item));
		}
	} else {
		escribir_operando(yyout, $1.lexema, TRUE);
	}

	strcpy($$.lexema, $1.lexema);
 }
| constante {
	fprintf(yyout,";R81:\t<exp> ::= <constante>\n");
	$$.tipo = $1.tipo;
	// will never be a "direction"
	$$.es_direccion = FALSE;
	$$.valor_entero = $1.valor_entero;
	sprintf($$.lexema, "%d", $1.valor_entero);

 }
| TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO {
	fprintf(yyout,";R82:\t<exp> ::= ( <exp> )\n");
	$$.tipo = $2.tipo;
	$$.es_direccion = $2.es_direccion;
 }
| TOK_PARENTESISIZQUIERDO comparacion TOK_PARENTESISDERECHO {
	fprintf(yyout,";R83:\t<exp> ::= ( <comparacion> )\n");
	$$.tipo = $2.tipo;
	$$.es_direccion = $2.es_direccion;
 }
| elemento_vector {
	fprintf(yyout,";R85:\t<exp> ::= <elemento_vector>\n");
	$$.tipo = $1.tipo;
	$$.es_direccion = $1.es_direccion;
 }
| idf_llamada_funcion TOK_PARENTESISIZQUIERDO lista_expresiones TOK_PARENTESISDERECHO {
	fprintf(yyout,";R88:\t<exp> ::= <identificador> ( <lista_expresiones> )\n");
	DataItem * item = SymbolTable_get(table, $1.lexema);
	int quantity = DataItem_get_num_params(item);

	if( num_parametros_llamada_actual != quantity){
		fprintf(stderr, "****Error semantico en lin %d: Numero incorrecto de parametros en llamada a funcion. num_parametros_llamada: %d vs quantity: %d\n", row, num_parametros_llamada_actual, quantity);
		SymbolTable_free(table);
		 return -1;
	}
	en_explist = 0;
	$$.tipo = DataItem_get_type(item);
	$$.es_direccion = 0;

	llamarFuncion(yyout, $1.lexema, quantity);
	};

idf_llamada_funcion: TOK_IDENTIFICADOR {
	fprintf(yyout,";R88.2:\tidf_llamada funcion\n");
	DataItem * item = SymbolTable_get(table, $1.lexema);
	/* if it doesn't exist*/
	if (!item) {
		fprintf(stderr, "****Error semantico en lin %d: Acceso a variable no declarada (%s)\n", row, $1.lexema);
		SymbolTable_free(table);
		 return -1;
	}

	if(DataItem_get_element_category(item) != FUNCTION) {
		//we didn't know exactly what error of the list would be here so we print this:
		fprintf(stderr, "****Error semantico en lin %d: Asignacion incompatible.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	if(en_explist == 1){
		fprintf(stderr, "****Error semantico en lin %d: No esta permitido el uso de llamadas a funciones como parametros de otras funciones.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	num_parametros_llamada_actual=0;
	en_explist = 1;
	strcpy($$.lexema, $1.lexema);
 };

exp_fn: exp {
    operandoEnPilaAArgumento(yyout, $1.es_direccion);
}

lista_expresiones: exp_fn resto_lista_expresiones {
	fprintf(yyout,";R89:\t<lista_expresiones> ::= <exp> <resto_lista_expresiones>\n");
	num_parametros_llamada_actual++;
	}
 | /* empty */ {fprintf(yyout,";R90:\t<lista_expresiones> ::=\n");};

resto_lista_expresiones: TOK_COMA exp_fn resto_lista_expresiones {
	fprintf(yyout,";R91:\t<resto_lista_expresiones> ::= , <exp> <resto_lista_expresiones>\n");
	num_parametros_llamada_actual++;
 }
  | /* empty */ {fprintf(yyout,";R92:\t<resto_lista_expresiones> ::=\n");
};



comparacion: exp TOK_IGUAL exp {fprintf(yyout,";R93:\t<comparacion> ::= <exp> == <exp>\n");
	if (($1.tipo == BOOLEAN) || ($3.tipo == BOOLEAN))
	{
		fprintf(stderr, "****Error semantico en lin %d: Comparacion con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	igual(yyout, $1.es_direccion, $3.es_direccion, counttag);
	counttag++;

	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
 }
 | exp TOK_DISTINTO exp {fprintf(yyout,";R94:\t<comparacion> ::= <exp> != <exp>\n"); /*R94*/
	if (($1.tipo == BOOLEAN) || ($3.tipo == BOOLEAN))
	{
		fprintf(stderr, "****Error semantico en lin %d: Comparacion con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	distinto(yyout, $1.es_direccion, $3.es_direccion, counttag);
	counttag++;

	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;

 }
 | exp TOK_MENORIGUAL exp {fprintf(yyout,";R95:\t<comparacion> ::= <exp> <= <exp>\n"); /*R95*/
	if (($1.tipo == BOOLEAN) || ($3.tipo == BOOLEAN))
	{
		fprintf(stderr, "****Error semantico en lin %d: Comparacion con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	menor_igual(yyout, $1.es_direccion, $3.es_direccion, counttag);
	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
 }
 | exp TOK_MAYORIGUAL exp {fprintf(yyout,";R96:\t<comparacion> ::= <exp> >= <exp>\n");/*R96*/
	if (($1.tipo == BOOLEAN) || ($3.tipo == BOOLEAN))
	{
		fprintf(stderr, "****Error semantico en lin %d: Comparacion con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	mayor_igual(yyout, $1.es_direccion, $3.es_direccion, counttag);
	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;

 }
 | exp TOK_MENOR exp {fprintf(yyout,";R97:\t<comparacion> ::= <exp> < <exp>\n"); /*R97*/
 	if (($1.tipo == BOOLEAN) || ($3.tipo == BOOLEAN))
	{
		fprintf(stderr, "****Error semantico en lin %d: Comparacion con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	menor(yyout, $1.es_direccion, $3.es_direccion, counttag);
	counttag++;

	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
 }
 | exp TOK_MAYOR exp {fprintf(yyout,";R98:\t<comparacion> ::= <exp> > <exp>\n"); /*R98*/
	if (($1.tipo == BOOLEAN) || ($3.tipo == BOOLEAN))
	{
		fprintf(stderr, "****Error semantico en lin %d: Comparacion con operandos boolean.\n", row);
		SymbolTable_free(table);
		 return -1;
	}

	mayor(yyout, $1.es_direccion, $3.es_direccion, counttag);
	counttag++;

	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
 };

constante: constante_logica {fprintf(yyout,";R99:\t<constante> ::= <constante_logica>\n"); /*R99*/
	$$.tipo = $1.tipo; 
	$$.es_direccion = $1.es_direccion;
	$$.valor_entero = $1.valor_entero;
 }
 | constante_entera { /*R100*/
	$$.tipo = $1.tipo;
	$$.es_direccion = $1.es_direccion;
	$$.valor_entero = $1.valor_entero;
	
};

constante_entera: TOK_CONSTANTE_ENTERA {fprintf(yyout,";R100:\t<constante> ::= TOK_CONSTANTE_ENTERA\n");
	$$.tipo = INT;
	$$.es_direccion = 0;
	$$.valor_entero = $1.valor_entero;
	//here it should be int_value but we replace it for lexema because we adapted alfa.l 
	escribir_operando(yyout, $1.lexema, FALSE);
 };

constante_logica: TOK_TRUE {fprintf(yyout,";R102:\t<constante_logica> ::= true\n");/*R102*/ 
	$$.valor_entero = TRUE;
	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
	escribir_operando(yyout, "1", FALSE);
  }
 | TOK_FALSE {fprintf(yyout,";R103:\t<constante_logica> ::= false\n"); /*R103*/
	$$.valor_entero = FALSE;
	$$.tipo = BOOLEAN;
	$$.es_direccion = FALSE;
	escribir_operando(yyout, "0", FALSE);
};

identificador: TOK_IDENTIFICADOR { fprintf(yyout,";R108:\t<identificador> ::= TOK_IDENTIFICADOR\n"); /*R108*/
	/* TOK_IDENTIFICADOR's lexema comes from alfa.l (check variable) */
	strcpy($$.lexema, $1.lexema); 
	if (SymbolTable_add(table, $1.lexema, tamanio_vector_actual, VARIABLE, tipo_actual, clase_actual,
						-1, -1, -1, pos_variable_local_actual) == ERROR)
	{
		/* Can't add to current context */
		fprintf(stderr, "****Error semantico en lin %d: Declaracion duplicada.\n", row);
		SymbolTable_free(table);
		 return -1;
	}
	if (islocal)
	{
		if(clase_actual != SCALAR){
			fprintf(stderr, "****Error semantico en lin %d: Variable local de tipo no escalar.\n", row);
			SymbolTable_free(table);
		 return -1;
		}

		num_variables_locales_actual++;
		pos_variable_local_actual++;
	}
	else {
		if(clase_actual == VECTOR){
			declarar_variable(yyout, $1.lexema, tipo_actual, tamanio_vector_actual);
		}
		else{
			declarar_variable(yyout, $1.lexema, tipo_actual, 1);
		}
	}
 };


%%


int yyerror(char* s){
	if(!(yylval.atributos.morfoerr))
		fprintf(stderr, "****Error sintactico en [lin %d, col %d]\n", row, column);
	
	return 0;
}
