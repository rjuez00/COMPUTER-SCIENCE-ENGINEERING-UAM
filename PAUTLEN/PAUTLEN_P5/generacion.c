#include "generacion.h"
//#include <string.h>
/* https://moodle.uam.es/pluginfile.php/2635338/mod_resource/content/1/ioexample.asm */
/* https://moodle.uam.es/pluginfile.php/2618370/mod_resource/content/2/libreria_generacion_codigo.pdf */
void escribir_cabecera_bss(FILE* fpasm) {
	if (!fpasm) return;
	
	fprintf(fpasm, "segment .bss\n__esp resd 1\n");
}

void escribir_subseccion_data(FILE* fpasm) {
	if (!fpasm) return;
	
	fprintf(fpasm, "segment .data\n\tmsg_error_division db \"Error: División por 0.\", 0\n\
	msg_error_indice_vector db \"Error: Indice fuera de rango\", 0\n");

}

void declarar_variable(FILE* fpasm, char * nombre, int tipo, int tamano) {
	
	if (!fpasm || !nombre) return;
	
	fprintf(fpasm, "_%s resd %d\n", nombre, tamano);
}


void escribir_segmento_codigo(FILE* fpasm) {
	if(!fpasm) return;

	fprintf(fpasm, "segment .text\n\tglobal main\n\textern scan_int, print_int, scan_boolean, print_boolean\n\textern print_endofline, print_blank, print_string\n");

}

void escribir_inicio_main(FILE* fpasm) {	
    
	if (!fpasm) return;

	fprintf(fpasm, "main:\n\tmov dword [__esp], esp\n");

}

void escribir_fin(FILE* fpasm) {
	
	if (!fpasm) return;
	
	fprintf(fpasm, "\tjmp near fin\n");
	fprintf(fpasm, "end_division_zero:\n");
	fprintf(fpasm, "\tpush dword msg_error_division\n");
	fprintf(fpasm, "\tcall print_string\n");
	fprintf(fpasm, "\tadd esp, 4\n");
	fprintf(fpasm, "\tcall print_endofline\n");
	fprintf(fpasm, "\tjmp near fin\n");
	fprintf(fpasm, "end_index_out_of_range:\n");
	fprintf(fpasm, "\tpush dword msg_error_indice_vector\n");
	fprintf(fpasm, "\tcall print_string\n");
	fprintf(fpasm, "\tadd esp, 4\n");
	fprintf(fpasm, "\tcall print_endofline\n");
	fprintf(fpasm, "\tjmp near fin\n");
	fprintf(fpasm, "fin:\n");
	fprintf(fpasm, "\tmov esp, [__esp]\n");
	fprintf(fpasm, "\tmov eax, 0\n");
	fprintf(fpasm, "\tmov edx, 0\n");
	fprintf(fpasm, "\tret\n");
}

void escribir_operando(FILE* fpasm, char* nombre, int es_variable){
	if (!fpasm || !nombre) return;

	if (!es_variable) {
		fprintf(fpasm, "\tpush dword %s\n", nombre);
	}
	else {
		fprintf(fpasm, "\tpush dword _%s\n", nombre);
	}
}

void asignar(FILE* fpasm, char* nombre, int es_variable){
	if (!fpasm || !nombre) return;
	fprintf(fpasm, "\tpop dword eax\n");

	if (es_variable == 1) { //this is a reference so we need to extract the content with []
		fprintf(fpasm, "\tmov dword eax, [eax]\n"); 
	}
	fprintf(fpasm, "\tmov dword [_%s], eax\n", nombre);
	
}

void pop_variable(FILE* fpasm, char* registro, int es_variable){
	fprintf(fpasm, "\tpop dword %s\n", registro);
	if (es_variable == 1) {
		fprintf(fpasm, "\tmov dword %s, [%s]\n", registro, registro);
	}
}

void push_variable(FILE* fpasm, char* registro, int es_variable){
	if (es_variable == 1) {
		fprintf(fpasm, "\tmov dword [%s], %s\n", registro, registro);
	}
	fprintf(fpasm, "\tpush dword %s\n", registro);
}

/* Private function to reuse code */
void arithmetic_operation(FILE* fpasm, char* operacion, int es_variable_1, int es_variable_2) {
	if (!fpasm) return;

	pop_variable(fpasm, "ebx", es_variable_2);
	pop_variable(fpasm, "eax", es_variable_1);	
	fprintf(fpasm, "\t%s eax, ebx\n\tpush dword eax\n", operacion);
}

void sumar(FILE* fpasm, int es_variable_1, int es_variable_2) {
	if (!fpasm) return;
	arithmetic_operation(fpasm, "add", es_variable_1, es_variable_2);
}

void restar(FILE* fpasm, int es_variable_1, int es_variable_2){
	if(!fpasm) return;
	arithmetic_operation(fpasm, "sub", es_variable_1, es_variable_2);
}

void multiplicar(FILE* fpasm, int es_variable_1, int es_variable_2){
	if(!fpasm) return;
	arithmetic_operation(fpasm, "imul", es_variable_1, es_variable_2);	
}

void dividir(FILE* fpasm, int es_variable_1, int es_variable_2){
	if(!fpasm) return; 
	//here we can't use arithmetic_operation because we need to check if we divide by 0!
	if (!fpasm) return;

	pop_variable(fpasm, "ecx", es_variable_2);
	pop_variable(fpasm, "eax", es_variable_1);

	fprintf(fpasm, "\tcmp ecx, 0\n\
	jz near end_division_zero\n"); /* check if dividing by 0, and if true, jump to error */ 
	fprintf(fpasm, "\tcdq\n"); /* TODO revise not sure it works but manual says it extends eax into edx REFERENCE B.4.19 */
	fprintf(fpasm, "\tidiv ecx\n\tpush dword eax\n");
}

void o(FILE* fpasm, int es_variable_1, int es_variable_2){
	if(!fpasm) return;
	arithmetic_operation(fpasm, "or", es_variable_1, es_variable_2);
}

void y(FILE* fpasm, int es_variable_1, int es_variable_2){
	if(!fpasm) return;
	arithmetic_operation(fpasm, "and", es_variable_1, es_variable_2);
}

void cambiar_signo(FILE* fpasm, int es_variable){
	if(!fpasm) return;
	
	pop_variable(fpasm, "eax", es_variable);
	
	fprintf(fpasm, "\tneg eax\n\tpush dword eax\n");
}

void no(FILE* fpasm, int es_variable, int cuantos_no){
	if(!fpasm) return;
	
	pop_variable(fpasm, "eax", es_variable);
	
	fprintf(fpasm, "\tor eax, eax\n");
	fprintf(fpasm, "\tjz near negate_false_%d\n", cuantos_no);
	fprintf(fpasm, "\tmov dword eax, 0\n");
	fprintf(fpasm, "\tjmp near end_negation_%d\n", cuantos_no);
	fprintf(fpasm, "negate_false_%d:\n\tmov dword eax, 1\n", cuantos_no);
	fprintf(fpasm, "\tend_negation_%d:\n\tpush dword eax\n", cuantos_no);
}

void compare_operation(FILE *fpasm, char* operation, int es_variable1, int es_variable2, int etiquetanumero, char* etiquetanombre, char* finetiquetanombre) {
	if(!fpasm) return;

	pop_variable(fpasm, "edx", es_variable2);
	pop_variable(fpasm, "eax", es_variable1);

	/* Check if the condition is met */
	fprintf(fpasm, "\tcmp eax, edx\n\
	%s near %s%d\n", operation, etiquetanombre, etiquetanumero);
	fprintf(fpasm, "\tpush dword 0\n");
	fprintf(fpasm, "\tjmp near %s%d\n", finetiquetanombre, etiquetanumero);
	fprintf(fpasm, "\t%s%d: push dword 1\n", etiquetanombre, etiquetanumero);
	fprintf(fpasm, "\t%s%d:\n", finetiquetanombre, etiquetanumero);
}

void igual(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta) {
	if(!fpasm) return;
	compare_operation(fpasm, "je", es_variable1, es_variable2, etiqueta, "equal", "end_equal");
}

void distinto(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta) {
	if(!fpasm) return;
	compare_operation(fpasm, "jne", es_variable1, es_variable2, etiqueta, "different", "end_different");
}

void menor_igual(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta) {
	if(!fpasm) return;
	compare_operation(fpasm, "jle", es_variable1, es_variable2, etiqueta, "less_equal", "end_less_equal");
}

void mayor_igual(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta) {
	if(!fpasm) return;
	compare_operation(fpasm, "jge", es_variable1, es_variable2, etiqueta, "more_equal", "more_equal_end");
}

void menor(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta) {
	if(!fpasm) return;
	compare_operation(fpasm, "jl", es_variable1, es_variable2, etiqueta, "less", "end_less");
}

void mayor(FILE* fpasm, int es_variable1, int es_variable2, int etiqueta) {
	if(!fpasm) return;
	compare_operation(fpasm, "jg", es_variable1, es_variable2, etiqueta, "more", "end_more");
}

/* FUNCIONES DE ESCRITURA Y LECTURA */
/*
   Se necesita saber el tipo de datos que se va a procesar (ENTERO o BOOLEANO) ya que hay diferentes
   funciones de librería para la lectura (idem. escritura) de cada tipo.
   Se deben insertar en la pila los argumentos necesarios, realizar la llamada (call) a la función
   de librería correspondiente y limpiar la pila.
*/

void leer(FILE* fpasm, char* nombre, int tipo) {
	if(!fpasm || !nombre) return;

	fprintf(fpasm, "\tpush dword _%s\n", nombre);
		
	switch (tipo) {
		case ENTERO:
		default:
			fprintf(fpasm, "\tcall scan_int\n");
		break;
		case BOOLEANO:
			fprintf(fpasm, "\tcall scan_boolean\n");
		break;
	}
	/* We have to recover the esp pointer */
	fprintf(fpasm, "\tadd esp, 4\n");
}

void leer_local(FILE* fpasm, int posicion_variable_local, int tipo) {
	if(!fpasm) return;

	switch (tipo) {
		case ENTERO:
		default:
			fprintf(fpasm, "\tcall scan_int\n");
		break;
		case BOOLEANO:
			fprintf(fpasm, "\tcall scan_boolean\n");
		break;
	}
	/* We have to recover the esp pointer */
	fprintf(fpasm, "\tadd esp, 4\n");
}

void escribir(FILE* fpasm, int es_variable, int tipo) {
	if(!fpasm) return;
	
	if (es_variable == 1) {
		pop_variable(fpasm, "eax", 1);
		push_variable(fpasm, "eax", 0);
	}
	switch(tipo) {
		case ENTERO:
			fprintf(fpasm, "\tcall print_int\n");
			break;
		default:
			fprintf(fpasm, "\tcall print_boolean\n");
			break;
	}

	fprintf(fpasm, "\tadd esp, 4\n");
	fprintf(fpasm, "\tcall print_endofline\n");
}

void ifthenelse_inicio(FILE * fpasm, int exp_es_variable, int etiqueta) {
	if (!fpasm) return;
	
	pop_variable(fpasm, "eax", exp_es_variable);

	/* Code executes only if the boolean from the stack is 1 (TRUE)
	 if it's FALSE, then jump. If not, execute the "else"*/
	fprintf(fpasm, "\tcmp eax, 0\n");
	fprintf(fpasm, "\tje near else_%d\n", etiqueta);
	
}

void ifthen_inicio(FILE * fpasm, int exp_es_variable, int etiqueta) {
	if (!fpasm) return;
	
	pop_variable(fpasm, "eax", exp_es_variable);

	/* Code executes only if the boolean from the stack is 1 (TRUE)
	   if it's FALSE, then jump. */
	fprintf(fpasm, "\tcmp eax, 0\n");
	fprintf(fpasm, "\tje near endif_%d\n", etiqueta);
}

void ifthen_fin(FILE * fpasm, int etiqueta) {
	if (!fpasm) return;

	fprintf(fpasm, "endif_%d:\n", etiqueta);
}

/* else */
void ifthenelse_fin_then(FILE * fpasm, int etiqueta) {
	if (!fpasm) return;

	//Once the code inside the if has executed, it skips the else part,
	//jumping to the end of the if.
	fprintf(fpasm, "\tjmp near endif_else_%d\n", etiqueta);
	fprintf(fpasm, "else_%d:\n", etiqueta);
}

void ifthenelse_fin( FILE * fpasm, int etiqueta) {
	if (!fpasm) return;

	fprintf(fpasm, "endif_else_%d:\n", etiqueta);
}

void while_inicio(FILE * fpasm, int etiqueta) {
	if (!fpasm) return;

	fprintf(fpasm, "start_while_%d:\n", etiqueta);
}

void while_exp_pila (FILE * fpasm, int exp_es_variable, int etiqueta) {
	if (!fpasm) return;

	pop_variable(fpasm, "eax", exp_es_variable);

	fprintf(fpasm, "\tcmp eax, 0\n");
	fprintf(fpasm, "\tje near end_while_%d\n", etiqueta);
}

void while_fin( FILE * fpasm, int etiqueta){
	if (!fpasm) return;

	fprintf(fpasm, "\tjmp near start_while_%d\n", etiqueta);
	fprintf(fpasm, "end_while_%d:\n", etiqueta);
}

void escribir_elemento_vector(FILE * fpasm,char * nombre_vector, 
                   int tam_max, int exp_es_direccion) {
	if (!fpasm) return;
	/* Get the index from the stack */
	pop_variable(fpasm, "eax", exp_es_direccion);
	
	/* First, check if the indexes are out of range */
	fprintf(fpasm, "\tcmp eax, 0\n"); /* negative index */
	fprintf(fpasm, "\tjl end_index_out_of_range\n");
	fprintf(fpasm, "\tcmp eax, %d\n", tam_max - 1); /* over max size */
	fprintf(fpasm, "\tjg end_index_out_of_range\n");

	/* Save the offset of nombre_vector in edx */
	fprintf(fpasm, "\tmov dword edx, _%s\n", nombre_vector);
	/* Load the array data for the index (eax) */
	fprintf(fpasm, "\tlea eax, [edx + eax*4]\n");
	fprintf(fpasm, "\tpush dword eax\n");
}

void declararFuncion(FILE * fd_asm, char * nombre_funcion, int num_var_loc) {
	if(!fd_asm || !nombre_funcion) return;

	/* Taken from the slides */
	fprintf(fd_asm, "_%s:\n", nombre_funcion);
	fprintf(fd_asm, "\tpush ebp\n");
	fprintf(fd_asm, "\tmov ebp, esp\n");
	fprintf(fd_asm, "\tsub esp, %d\n", 4 * num_var_loc);
}

void retornarFuncion(FILE * fd_asm, int es_variable) {
	if (!fd_asm) return;
	/* Pop the variable to be returned */
	pop_variable(fd_asm, "eax", es_variable);

    fprintf(fd_asm, "\tmov esp, ebp\n");
    fprintf(fd_asm, "\tpop ebp\n");
    fprintf(fd_asm, "\tret\n");
}

void escribirParametro(FILE* fpasm, int pos_parametro, int num_total_parametros) {
	if (!fpasm) return;
	fprintf(fpasm, "\tlea eax, [ebp + %d]\n", 4+4*(num_total_parametros - pos_parametro));
	fprintf(fpasm, "\tpush dword eax\n");
}

void escribirVariableLocal(FILE* fpasm, int posicion_variable_local) {
	if (!fpasm) return;
	fprintf(fpasm, "\tlea eax, [ebp - %d]\n", 4*(posicion_variable_local));
	fprintf(fpasm, "\tpush dword eax\n");
}

void asignarDestinoEnPila(FILE* fpasm, int es_variable) {
	if (!fpasm) return;
	pop_variable(fpasm, "ebx", 0);
	pop_variable(fpasm, "eax", es_variable);
	
	fprintf(fpasm, "\tmov dword [ebx], eax\n");
}


void asignarDestinoEnPila_paraVector(FILE* fpasm, int es_variable) {
	if (!fpasm) return;
	pop_variable(fpasm, "eax", es_variable);
	pop_variable(fpasm, "ebx", 0);
	
	fprintf(fpasm, "\tmov dword [ebx], eax\n");
}

void operandoEnPilaAArgumento(FILE * fd_asm, int es_variable) {
	if (!fd_asm) return;

	if (es_variable == 1) {
		fprintf(fd_asm, "\tpop eax\n");
		fprintf(fd_asm, "\tmov eax, [eax]\n");
		fprintf(fd_asm, "\tpush eax\n");
	}
}

void llamarFuncion(FILE * fd_asm, char * nombre_funcion, int num_argumentos) {
	if (!fd_asm) return;
	fprintf(fd_asm, "\tcall _%s\n", nombre_funcion);
	fprintf(fd_asm, "\tadd esp, %d*4\n", num_argumentos);
	fprintf(fd_asm, "\tpush dword eax\n");
}

void limpiarPila(FILE * fd_asm, int num_argumentos){
	if (!fd_asm) return;
	fprintf(fd_asm, "\tadd esp, %d\n", num_argumentos*4);
}