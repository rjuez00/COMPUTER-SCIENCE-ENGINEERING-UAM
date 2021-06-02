/*
AUTORES:
    Jose Manuel Freire Porras
    Jorge González Gómez
    Rodrigo Juez Hernández
*/


%{  /* here includes and declaration of variables */
    #include <stdio.h>
    #include <stdlib.h>
    #include "tokens.h"

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
NEWLINE [\n]
COMMENT "//".*\n
EVERYTHINGELSE .

/* here what it looks for */
%%

main { column += yyleng; fprintf(yyout, "TOK_MAIN"); return TOK_MAIN; }
int { column += yyleng; fprintf(yyout, "TOK_INT"); return TOK_INT; }
boolean { column += yyleng; fprintf(yyout, "TOK_BOOLEAN"); return TOK_BOOLEAN; }
array { column += yyleng; fprintf(yyout, "TOK_ARRAY"); return TOK_ARRAY; }
function { column += yyleng; fprintf(yyout, "TOK_FUNCTION"); return TOK_FUNCTION; }
if { column += yyleng; fprintf(yyout, "TOK_IF"); return TOK_IF; }
else { column += yyleng; fprintf(yyout, "TOK_ELSE"); return TOK_ELSE; }
while { column += yyleng; fprintf(yyout, "TOK_WHILE"); return TOK_WHILE; }
scanf { column += yyleng; fprintf(yyout, "TOK_SCANF"); return TOK_SCANF; }
printf { column += yyleng; fprintf(yyout, "TOK_PRINTF"); return TOK_PRINTF; }
return { column += yyleng; fprintf(yyout, "TOK_RETURN"); return TOK_RETURN; }


";" { column += yyleng; fprintf(yyout, "TOK_PUNTOYCOMA"); return TOK_PUNTOYCOMA; }
"," { column += yyleng; fprintf(yyout, "TOK_COMA"); return TOK_COMA; }
"(" { column += yyleng; fprintf(yyout, "TOK_PARENTESISIZQUIERDO"); return TOK_PARENTESISIZQUIERDO; }
")" { column += yyleng; fprintf(yyout, "TOK_PARENTESISDERECHO"); return TOK_PARENTESISDERECHO; }
"[" { column += yyleng; fprintf(yyout, "TOK_CORCHETEIZQUIERDO"); return TOK_CORCHETEIZQUIERDO; }
"]" { column += yyleng; fprintf(yyout, "TOK_CORCHETEDERECHO"); return TOK_CORCHETEDERECHO; }
"{" { column += yyleng; fprintf(yyout, "TOK_LLAVEIZQUIERDA"); return TOK_LLAVEIZQUIERDA; }
"}" { column += yyleng; fprintf(yyout, "TOK_LLAVEDERECHA"); return TOK_LLAVEDERECHA; }
"=" { column += yyleng; fprintf(yyout, "TOK_ASIGNACION"); return TOK_ASIGNACION; }
"+" { column += yyleng; fprintf(yyout, "TOK_MAS"); return TOK_MAS; }
"-" { column += yyleng; fprintf(yyout, "TOK_MENOS"); return TOK_MENOS; }
"/" { column += yyleng; fprintf(yyout, "TOK_DIVISION"); return TOK_DIVISION; }
"*" { column += yyleng; fprintf(yyout, "TOK_ASTERISCO"); return TOK_ASTERISCO; }
"&&" { column += yyleng; fprintf(yyout, "TOK_AND"); return TOK_AND; }
"||" { column += yyleng; fprintf(yyout, "TOK_OR"); return TOK_OR; }
"!" { column += yyleng; fprintf(yyout, "TOK_NOT"); return TOK_NOT; }
"==" { column += yyleng; fprintf(yyout, "TOK_IGUAL"); return TOK_IGUAL; }
"!=" { column += yyleng; fprintf(yyout, "TOK_DISTINTO"); return TOK_DISTINTO; }
"<=" { column += yyleng; fprintf(yyout, "TOK_MENORIGUAL"); return TOK_MENORIGUAL; }
">=" { column += yyleng; fprintf(yyout, "TOK_MAYORIGUAL"); return TOK_MAYORIGUAL; }
"<" { column += yyleng; fprintf(yyout, "TOK_MENOR"); return TOK_MENOR; }
">" { column += yyleng; fprintf(yyout, "TOK_MAYOR"); return TOK_MAYOR; }
true { column += yyleng; fprintf(yyout, "TOK_TRUE"); return TOK_TRUE; }
false { column += yyleng; fprintf(yyout, "TOK_FALSE"); return TOK_FALSE; }



{COMMENT} { column = 1; row += 1; /*ignore*/}
{NEWLINE} { column = 1; row += 1; /*ignore*/ } 
{WHITESPACEORTAB} { column += yyleng; /*ignore*/ } 

{VARIABLE}  {  
    if (yyleng > 100)
        return TOK_IDENTIFICADOR;
    
    column += yyleng; 
    fprintf(yyout, "TOK_IDENTIFICADOR"); 
    return TOK_IDENTIFICADOR; 
}

{INTEGER} { column += yyleng; fprintf(yyout, "TOK_CONSTANTE_ENTERA"); return TOK_CONSTANTE_ENTERA; }
{EVERYTHINGELSE} { return TOK_ERROR; }


%%

int main (int argc, char **argv){
    if(argc < 3){
        printf("Usage: %s input output\n", argv[0]);
        return EXIT_FAILURE;
    }
    int flagerror=0;
    int y=-1;
    yyin=NULL;
    yyin = fopen(argv[1], "r");
    if(!yyin){
        fprintf(stderr, "Error opening yyin");
        return EXIT_FAILURE;
    }
    yyout=NULL;
    yyout = fopen(argv[2], "w");
    if(!yyout){
        fprintf(stderr, "Error opening yyout");
        fclose(yyout);
        return EXIT_FAILURE;
    }
    

    while(1) {
        y=yylex();
        if(y == 0) break;

        if (y == TOK_ERROR){
            fprintf(stderr, "****Error en [lin %d, col %d]: simbolo no permitido %s\n", row, column, yytext);
            flagerror = 1;
            break;
        }
        else if (y == TOK_IDENTIFICADOR && yyleng > 100) {
            fprintf(stderr, "****Error en [lin %d, col %d]: identificador demasiado largo %s\n", row, column, yytext);
            flagerror = 1;
            break;
        }
        else
            fprintf(yyout, "\t%d\t%s\n", y, yytext);
    } 

    fclose(yyin);
    fclose(yyout);
    
    if(flagerror) return EXIT_FAILURE;
    return EXIT_SUCCESS;
}
