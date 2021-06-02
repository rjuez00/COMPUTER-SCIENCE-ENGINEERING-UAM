%{
#include <stdio.h>

extern int yylex();
extern FILE* yyout;
int yyerror();
extern int column, row;

%}


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

/* Smbolos */
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

/* Identificadores*/
%token TOK_IDENTIFICADOR

/* Constantes */ 
%token TOK_CONSTANTE_ENTERA
%token TOK_TRUE
%token TOK_FALSE

/* Error */
%token TOK_ERROR

/* Precedence */
%left TOK_MAS TOK_MENOS
%left TOK_ASTERISCO TOK_DIVISION

%left TOK_NOT
%left TOK_AND TOK_OR

%%

/*plantilla:
	{fprintf(yyout,";R?:\t<left> ::= <right>\n");}
*/

programa: TOK_MAIN TOK_LLAVEIZQUIERDA declaraciones funciones sentencias TOK_LLAVEDERECHA {fprintf(yyout,";R1:\t<programa> ::= main { <declaraciones> <funciones> <sentencias> }\n" );};

declaraciones: declaracion {fprintf(yyout,";R2:\t<declaraciones> ::= <declaracion>\n");}
| declaracion declaraciones {fprintf(yyout,";R3:\t<declaraciones> ::= <declaracion> <declaraciones>\n");};

declaracion: clase identificadores TOK_PUNTOYCOMA {fprintf(yyout,";R4:\t<declaracion> ::= <clase> <identificadores> ;\n");};

clase: clase_escalar {fprintf(yyout,";R5:\t<clase> ::= <clase_escalar>\n");}
| clase_vector {fprintf(yyout,";R7:\t<clase> ::= <clase_vector>\n");};

clase_escalar: tipo {fprintf(yyout,";R9:\t<clase_escalar> ::= <tipo>\n");};

tipo: TOK_INT {fprintf(yyout,";R10:\t<tipo> ::= int\n");}
| TOK_BOOLEAN {fprintf(yyout,";R11:\t<tipo> ::= boolean\n");};

clase_vector: TOK_ARRAY tipo TOK_CORCHETEIZQUIERDO TOK_CONSTANTE_ENTERA TOK_CORCHETEDERECHO {fprintf(yyout,";R15:\t<tipo> ::= array <tipo>[ TOK_CONSTANTE_ENTERA ]\n");};

identificadores: identificador {fprintf(yyout,";R18:\t<identificadores> ::= <identificador>\n");}
| identificador TOK_COMA identificadores {fprintf(yyout,";R19:\t<identificadores> ::= <identificador> , <identificadores>\n");};

funciones: funcion funciones {fprintf(yyout,";R20:\t<left> ::= <funcion> <funciones>\n");}
| /* empty */ {fprintf(yyout,";R21:\t<funciones> ::=\n");};

funcion: TOK_FUNCTION tipo identificador TOK_PARENTESISIZQUIERDO parametros_funcion TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA declaraciones_funcion sentencias TOK_LLAVEDERECHA
																							{fprintf(yyout,";R22:\t<funcion> ::= function <tipo> <identificador> ( <parametros_funcion> ) { <declaraciones_funcion> <sentencias> }\n");};

parametros_funcion: parametro_funcion resto_parametros_funcion {fprintf(yyout,";R23:\t<resto_parametros_funcion> ::= <parametro_funcion> <resto_parametros_funcion>\n");}
| /* empty */ {fprintf(yyout,";R24:\t<parametros_funcion> ::=\n");};

resto_parametros_funcion: TOK_PUNTOYCOMA parametro_funcion resto_parametros_funcion {fprintf(yyout,";R25:\t<resto_parametros_funcion> ::= ; <parametros_funcion> <resto_parametros_funcion>\n");}
| /* empty */ {fprintf(yyout,";R26:\t<resto_parametros_funcion> ::=\n");};

parametro_funcion: tipo identificador {fprintf(yyout,";R27:\t<parametro_funcion> ::= <tipo> <identificador>\n");};

declaraciones_funcion: declaraciones {fprintf(yyout,";R28:\t<declaraciones_funcion> ::= <declaraciones>\n");} 
| /* empty */ {fprintf(yyout,";R29:\t<declaraciones_funcion> ::=\n");};

sentencias: sentencia {fprintf(yyout,";R30:\t<sentencias> ::= <sentencia>\n");}
| sentencia sentencias {fprintf(yyout,";R31:\t<sentencias> ::= <sentencia> <sentencias>\n");};

sentencia: sentencia_simple TOK_PUNTOYCOMA {fprintf(yyout,";R32:\t<sentencia> ::= <sentencia_simple> ;\n");}
| bloque {fprintf(yyout,";R33:\t<sentencia> ::= <bloque>\n");};

sentencia_simple: asignacion {fprintf(yyout,";R34:\t<sentencia_simple> ::= <asignacion>\n");}
| lectura {fprintf(yyout,";R35:\t<sentencia_simple> ::= <lectura>\n");}
| escritura {fprintf(yyout,";R36:\t<sentencia_simple> ::= <escritura>\n");}
| retorno_funcion {fprintf(yyout,";R38:\t<sentencia_simple> ::= <retorno_funcion>\n");};

bloque: condicional {fprintf(yyout,";R40:\t<bloque> ::= <condicional>\n");}
| bucle {fprintf(yyout,";R41:\t<bloque> ::= <bucle>\n");};

asignacion: identificador TOK_ASIGNACION exp {fprintf(yyout,";R43:\t<asignacion> ::= <identificador> = <exp>\n");}
| elemento_vector TOK_ASIGNACION exp {fprintf(yyout,";R44:\t<asignacion> ::= <elemento_vector> = <exp>\n");};

elemento_vector: identificador TOK_CORCHETEIZQUIERDO exp TOK_CORCHETEDERECHO {fprintf(yyout,";R48:\t<elemento_vector> ::= <identificador> [ <exp> ]\n");};

condicional: TOK_IF TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA {fprintf(yyout,";R50:\t<condicional> ::= if ( <exp> ) { <sentencias> }\n");}
| TOK_IF TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA TOK_ELSE TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA {fprintf(yyout,";R51:\t<condicional> ::= if ( <exp> ) { <sentencias> } else { <sentencias> }\n");};

bucle: TOK_WHILE TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO TOK_LLAVEIZQUIERDA sentencias TOK_LLAVEDERECHA {fprintf(yyout,";R52:\t<bucle> ::= while ( <exp> ) { <sentencias> }\n");};

lectura: TOK_SCANF identificador {fprintf(yyout,";R54:\t<lectura> ::= scanf <identificador>\n");};

escritura: TOK_PRINTF exp {fprintf(yyout,";R56:\t<escritura> ::= printf <exp>\n");};

retorno_funcion: TOK_RETURN exp {fprintf(yyout,";R61:\t<retorno_funcion> ::= return <exp>\n");};

exp: exp TOK_MAS exp {fprintf(yyout,";R72:\t<exp> ::= <exp> + <exp>\n");}
| exp TOK_MENOS exp {fprintf(yyout,";R73:\t<exp> ::= <exp> - <exp>\n");}
| exp TOK_DIVISION exp {fprintf(yyout,";R74:\t<exp> ::= <exp> / <exp>\n");}
| exp TOK_ASTERISCO exp {fprintf(yyout,";R75:\t<exp> ::= <exp> * <exp>\n");}
| TOK_MENOS exp {fprintf(yyout,";R76:\t<exp> ::= - <exp>\n");}
| exp TOK_AND exp {fprintf(yyout,";R77:\t<exp> ::= <exp> && <exp>\n");}
| exp TOK_OR exp {fprintf(yyout,";R78:\t<exp> ::= <exp> || <exp>\n");}
| TOK_NOT exp {fprintf(yyout,";R79:\t<exp> ::= ! <exp>\n");}
| identificador {fprintf(yyout,";R80:\t<exp> ::= <identificador>\n");}
| constante {fprintf(yyout,";R81:\t<exp> ::= <constante>\n");}
| TOK_PARENTESISIZQUIERDO exp TOK_PARENTESISDERECHO {fprintf(yyout,";R82:\t<exp> ::= ( <exp> )\n");}
| TOK_PARENTESISIZQUIERDO comparacion TOK_PARENTESISDERECHO {fprintf(yyout,";R83:\t<exp> ::= ( <comparacion> )\n");}
| elemento_vector {fprintf(yyout,";R85:\t<exp> ::= <elemento_vector>\n");}
| identificador TOK_PARENTESISIZQUIERDO lista_expresiones TOK_PARENTESISDERECHO {fprintf(yyout,";R88:\t<exp> ::= <identificador> ( <lista_expresiones> )\n");};

lista_expresiones: exp resto_lista_expresiones {fprintf(yyout,";R89:\t<lista_expresiones> ::= <exp> <resto_lista_expresiones>\n");}
| /* empty */ {fprintf(yyout,";R90:\t<lista_expresiones> ::=\n");};

resto_lista_expresiones: TOK_COMA exp resto_lista_expresiones {fprintf(yyout,";R91:\t<resto_lista_expresiones> ::= , <exp> <resto_lista_expresiones>\n");}
| /* empty */ {fprintf(yyout,";R92:\t<resto_lista_expresiones> ::=\n");};

comparacion: exp TOK_IGUAL exp {fprintf(yyout,";R93:\t<comparacion> ::= <exp> == <exp>\n");}
| exp TOK_DISTINTO exp {fprintf(yyout,";R94:\t<comparacion> ::= <exp> != <exp>\n");}
| exp TOK_MENORIGUAL exp {fprintf(yyout,";R95:\t<comparacion> ::= <exp> <= <exp>\n");}
| exp TOK_MAYORIGUAL exp {fprintf(yyout,";R96:\t<comparacion> ::= <exp> >= <exp>\n");}
| exp TOK_MENOR exp {fprintf(yyout,";R97:\t<comparacion> ::= <exp> < <exp>\n");}
| exp TOK_MAYOR exp {fprintf(yyout,";R98:\t<comparacion> ::= <exp> > <exp>\n");};

constante: constante_logica {fprintf(yyout,";R99:\t<constante> ::= <constante_logica>\n");}
| TOK_CONSTANTE_ENTERA {fprintf(yyout,";R100:\t<constante> ::= TOK_CONSTANTE_ENTERA\n");};

constante_logica: TOK_TRUE {fprintf(yyout,";R102:\t<constante_logica> ::= true\n");}
| TOK_FALSE {fprintf(yyout,";R103:\t<constante_logica> ::= false\n");};

identificador: TOK_IDENTIFICADOR {fprintf(yyout,";R108:\t<identificador> ::= TOK_IDENTIFICADOR\n");};


%%

/*
this is not necessary as by using TOK_IDENTIFICADOR and TOK_CONSTANTE_ENTERA we satisfy all these production rules:
		letra {fprintf(yyout,";R108:\t<identificador> ::= <letra>\n");}
		| letra cola_identificador {fprintf(yyout,";R109:\t<identificador> ::= <letra> <cola_identificador>\n");};

		cola_identificador: alfanumerico {fprintf(yyout,";R110:\t<cola_identificador> ::= <alfanumerico>\n");}
		| alfanumerico cola_identificador {fprintf(yyout,";R111:\t<cola_identificador> ::= <alfanumerico> <cola_identificador>\n");};

		alfanumerico: letra {fprintf(yyout,";R112:\t<alfanumerico> ::= <letra>\n");}
		| digito {fprintf(yyout,";R113:\t<alfanumerico> ::= <digito>\n");};

		letra: TOK_..*/

int yyerror(char* s){
	if(!yylval)
		printf("****Error sintactico en [lin %d, col %d]\n", row, column);
	
	return 0;
}
