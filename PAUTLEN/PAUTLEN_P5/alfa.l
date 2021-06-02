%{  /* here includes and declaration of variables */
/*
AUTORES:
    Jose Manuel Freire Porras
    Jorge González Gómez
    Rodrigo Juez Hernández
*/

#include "alfa.h"
#include <stdio.h>
#include "y.tab.h"
    
int row = 1;
int column = 1;

%}

/* here options and rules */
%option noyywrap
%option nounput
%option noinput

VARIABLE [a-zA-Z][a-zA-Z0-9]*
INTEGER [0-9]+
WHITESPACEORTAB [ \t]
NEWLINE [(\r\n)|(\n)]
COMMENT "//".*\n
EVERYTHINGELSE .

/* here what it looks for */
%%

main { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_MAIN; }
int { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_INT; }
boolean { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_BOOLEAN; }
array { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_ARRAY; }
function { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_FUNCTION; }
if { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_IF; }
else { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_ELSE; }
while { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_WHILE; }
scanf { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_SCANF; }
printf { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_PRINTF; }
return { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_RETURN; }
true { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_TRUE; }
false { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_FALSE; }


";" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_PUNTOYCOMA; }
"," { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_COMA; }
"(" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_PARENTESISIZQUIERDO; }
")" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_PARENTESISDERECHO; }
"[" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_CORCHETEIZQUIERDO; }
"]" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_CORCHETEDERECHO; }
"{" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_LLAVEIZQUIERDA; }
"}" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_LLAVEDERECHA; }
"=" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_ASIGNACION; }
"+" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_MAS; }
"-" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_MENOS; }
"/" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_DIVISION; }
"*" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_ASTERISCO; }
"&&" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_AND; }
"||" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_OR; }
"!" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_NOT; }
"==" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_IGUAL; }
"!=" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_DISTINTO; }
"<=" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_MENORIGUAL; }
">=" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_MAYORIGUAL; }
"<" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_MENOR; }
">" { column += yyleng; fprintf(yyout, ";D:\t%s\n", yytext); return TOK_MAYOR; }

{COMMENT} { column = 1; row += 1; /*ignore*/}
{NEWLINE} { column = 1; row += 1; /*ignore*/ } 
{WHITESPACEORTAB} { column += yyleng; /*ignore*/ } 

{VARIABLE}  {  
    if (yyleng > 100){
        fprintf(stderr, "****Error en [lin %d, col %d]: identificador demasiado largo %s\n", row, column, yytext);
        yylval.atributos.morfoerr = 1;
        return TOK_ERROR;
    }
    column += yyleng;
    strcpy(yylval.atributos.lexema, yytext);
    fprintf(yyout, ";D:\t%s\n", yytext); 
    return TOK_IDENTIFICADOR; 
}

{INTEGER} { 
    column += yyleng;
    /* much better doing this than converting it to int back and forth */
    strcpy(yylval.atributos.lexema, yytext);
    yylval.atributos.valor_entero = atoi(yytext);
    return TOK_CONSTANTE_ENTERA;
}

{EVERYTHINGELSE} { 
    fprintf(stderr, "****Error en [lin %d, col %d]: simbolo no permitido %s\n", row, column, yytext);
    yylval.atributos.morfoerr = 1;
    return TOK_ERROR; 
}


%%


/*regex used to change alfa.l
fprintf\(yyout, "TOK_(.*)"\) --> fprintf(yyout, ";D:\\t%s\\n", yytext);
*/
