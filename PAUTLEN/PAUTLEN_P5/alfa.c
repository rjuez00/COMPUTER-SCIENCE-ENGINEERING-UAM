#include <stdio.h>



int main (int argc, char **argv){
    extern FILE* yyin;
    extern FILE* yyout;
    int yyparse(); 



	short error = 1;
	if(argc < 3){
		printf("Usage: %s input output\n", argv[0]);
		return 1;
	}

	yyin = fopen(argv[1], "r");
	if(!yyin){
		fprintf(stderr, "Error opening input file\n");
		return 1;
	}
    yyout = fopen(argv[2], "w");
	if(!yyout){
		fprintf(stderr, "Error opening output file\n");
		fclose(yyin);
		return 1;
	}

	error = yyparse();
	fclose(yyin);
	fclose(yyout);

	return error;
}
