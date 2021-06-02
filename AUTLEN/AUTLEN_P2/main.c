#include <stdio.h>
#include "afnd.h"
#include "minimiza.h"


AFND *test1() {
	AFND * p_afnd;

	p_afnd = AFNDNuevo("test1",12,2);
	AFNDInsertaSimbolo(p_afnd,"0");
	AFNDInsertaSimbolo(p_afnd,"1");
	AFNDInsertaEstado(p_afnd,"q0",INICIAL_Y_FINAL);
	AFNDInsertaEstado(p_afnd,"q1",NORMAL);
	AFNDInsertaEstado(p_afnd,"q2",NORMAL);
	AFNDInsertaEstado(p_afnd,"q3",NORMAL);
	AFNDInsertaEstado(p_afnd,"q4",FINAL);
	AFNDInsertaEstado(p_afnd,"q5",NORMAL);
	AFNDInsertaEstado(p_afnd,"q6",NORMAL);
	AFNDInsertaEstado(p_afnd,"q7",NORMAL);
	AFNDInsertaEstado(p_afnd,"q8",FINAL);
	AFNDInsertaEstado(p_afnd,"q9",NORMAL);
	AFNDInsertaEstado(p_afnd,"q10",NORMAL);
	AFNDInsertaEstado(p_afnd,"q11",NORMAL);
	AFNDInsertaTransicion(p_afnd, "q0", "0", "q1");
	AFNDInsertaTransicion(p_afnd, "q0", "1", "q1");
	AFNDInsertaTransicion(p_afnd, "q1", "0", "q2");
	AFNDInsertaTransicion(p_afnd, "q1", "1", "q2");
	AFNDInsertaTransicion(p_afnd, "q2", "0", "q3");
	AFNDInsertaTransicion(p_afnd, "q2", "1", "q3");
	AFNDInsertaTransicion(p_afnd, "q3", "0", "q4");
	AFNDInsertaTransicion(p_afnd, "q3", "1", "q4");
	AFNDInsertaTransicion(p_afnd, "q4", "0", "q5");
	AFNDInsertaTransicion(p_afnd, "q4", "1", "q5");
	AFNDInsertaTransicion(p_afnd, "q5", "0", "q6");
	AFNDInsertaTransicion(p_afnd, "q5", "1", "q6");
	AFNDInsertaTransicion(p_afnd, "q6", "0", "q7");
	AFNDInsertaTransicion(p_afnd, "q6", "1", "q7");
	AFNDInsertaTransicion(p_afnd, "q7", "0", "q8");
	AFNDInsertaTransicion(p_afnd, "q7", "1", "q8");
	AFNDInsertaTransicion(p_afnd, "q8", "0", "q9");
	AFNDInsertaTransicion(p_afnd, "q8", "1", "q9");
	AFNDInsertaTransicion(p_afnd, "q9", "0", "q10");
	AFNDInsertaTransicion(p_afnd, "q9", "1", "q10");
	AFNDInsertaTransicion(p_afnd, "q10", "0", "q11");
	AFNDInsertaTransicion(p_afnd, "q10", "1", "q11");
	AFNDInsertaTransicion(p_afnd, "q11", "0", "q0");
	AFNDInsertaTransicion(p_afnd, "q11", "1", "q0");

	return p_afnd;
}

AFND *test2() {
	AFND * p_afnd;

	p_afnd = AFNDNuevo("test2",8,2);
	AFNDInsertaSimbolo(p_afnd,"0");
	AFNDInsertaSimbolo(p_afnd,"1");

	AFNDInsertaEstado(p_afnd,"A", INICIAL);
	AFNDInsertaEstado(p_afnd,"B", NORMAL);
	AFNDInsertaEstado(p_afnd,"C", FINAL);
	AFNDInsertaEstado(p_afnd,"D", NORMAL);
	AFNDInsertaEstado(p_afnd,"E", NORMAL);
	AFNDInsertaEstado(p_afnd,"F", NORMAL);
	AFNDInsertaEstado(p_afnd,"G", NORMAL);
	AFNDInsertaEstado(p_afnd,"H", NORMAL);

	AFNDInsertaTransicion(p_afnd, "A", "0", "B");
	AFNDInsertaTransicion(p_afnd, "A", "1", "F");

	AFNDInsertaTransicion(p_afnd, "B", "0", "G");
	AFNDInsertaTransicion(p_afnd, "B", "1", "C");
	AFNDInsertaTransicion(p_afnd, "C", "0", "A");
	AFNDInsertaTransicion(p_afnd, "C", "1", "C");
	AFNDInsertaTransicion(p_afnd, "D", "0", "C");
	AFNDInsertaTransicion(p_afnd, "D", "1", "G");
	AFNDInsertaTransicion(p_afnd, "E", "0", "H");
	AFNDInsertaTransicion(p_afnd, "E", "1", "F");
	AFNDInsertaTransicion(p_afnd, "F", "0", "C");
	AFNDInsertaTransicion(p_afnd, "F", "1", "G");
	AFNDInsertaTransicion(p_afnd, "G", "0", "G");
	AFNDInsertaTransicion(p_afnd, "G", "1", "E");
	AFNDInsertaTransicion(p_afnd, "H", "0", "G");
	AFNDInsertaTransicion(p_afnd, "H", "1", "C");

	return p_afnd;
}

AFND *test3() {
	AFND * p_afnd;

	p_afnd = AFNDNuevo("test3",5,2);
	AFNDInsertaSimbolo(p_afnd,"0");
	AFNDInsertaSimbolo(p_afnd,"1");

	AFNDInsertaEstado(p_afnd,"A", INICIAL);
	AFNDInsertaEstado(p_afnd,"B", NORMAL);
	AFNDInsertaEstado(p_afnd,"C", NORMAL);
	AFNDInsertaEstado(p_afnd,"D", NORMAL);
	AFNDInsertaEstado(p_afnd,"E", FINAL);

	AFNDInsertaTransicion(p_afnd, "A", "0", "B");
	AFNDInsertaTransicion(p_afnd, "A", "1", "C");
	AFNDInsertaTransicion(p_afnd, "B", "0", "B");
	AFNDInsertaTransicion(p_afnd, "B", "1", "D");
	AFNDInsertaTransicion(p_afnd, "C", "0", "B");
	AFNDInsertaTransicion(p_afnd, "C", "1", "C");
	AFNDInsertaTransicion(p_afnd, "D", "0", "B");
	AFNDInsertaTransicion(p_afnd, "D", "1", "E");
	AFNDInsertaTransicion(p_afnd, "E", "0", "B");
	AFNDInsertaTransicion(p_afnd, "E", "1", "C");

	return p_afnd;
}

AFND *test4() {
	AFND * p_afnd;

	p_afnd = AFNDNuevo("test4",5,2);
	AFNDInsertaSimbolo(p_afnd,"a");
	AFNDInsertaSimbolo(p_afnd,"b");

	AFNDInsertaEstado(p_afnd,"1", INICIAL);
	AFNDInsertaEstado(p_afnd,"2", NORMAL);
	AFNDInsertaEstado(p_afnd,"3", NORMAL);
	AFNDInsertaEstado(p_afnd,"4", NORMAL);
	AFNDInsertaEstado(p_afnd,"5", FINAL);

	AFNDInsertaTransicion(p_afnd, "1", "a", "2");
	AFNDInsertaTransicion(p_afnd, "1", "b", "3");
	AFNDInsertaTransicion(p_afnd, "2", "a", "2");
	AFNDInsertaTransicion(p_afnd, "2", "b", "4");
	AFNDInsertaTransicion(p_afnd, "3", "a", "2");
	AFNDInsertaTransicion(p_afnd, "3", "b", "3");
	AFNDInsertaTransicion(p_afnd, "4", "a", "2");
	AFNDInsertaTransicion(p_afnd, "4", "b", "5");
	AFNDInsertaTransicion(p_afnd, "5", "a", "2");
	AFNDInsertaTransicion(p_afnd, "5", "b", "1");

	return p_afnd;
}

AFND *test5() {
	AFND * p_afnd;

	p_afnd = AFNDNuevo("test5",9,2);
	AFNDInsertaSimbolo(p_afnd,"0");
	AFNDInsertaSimbolo(p_afnd,"1");

	AFNDInsertaEstado(p_afnd,"a", INICIAL);
	AFNDInsertaEstado(p_afnd,"b", NORMAL);
	AFNDInsertaEstado(p_afnd,"c", FINAL);
	AFNDInsertaEstado(p_afnd,"d", NORMAL);
	AFNDInsertaEstado(p_afnd,"e", NORMAL);
	AFNDInsertaEstado(p_afnd,"f", NORMAL);
	AFNDInsertaEstado(p_afnd,"g", NORMAL);
	AFNDInsertaEstado(p_afnd,"h", NORMAL);
	AFNDInsertaEstado(p_afnd,"i", FINAL);

	AFNDInsertaTransicion(p_afnd, "a", "0", "b");
	AFNDInsertaTransicion(p_afnd, "a", "1", "f");
	AFNDInsertaTransicion(p_afnd, "b", "0", "g");
	AFNDInsertaTransicion(p_afnd, "b", "1", "c");
	AFNDInsertaTransicion(p_afnd, "c", "0", "a");
	AFNDInsertaTransicion(p_afnd, "c", "1", "c");
	AFNDInsertaTransicion(p_afnd, "d", "0", "c");
	AFNDInsertaTransicion(p_afnd, "d", "1", "e");
	AFNDInsertaTransicion(p_afnd, "e", "0", "h");
	AFNDInsertaTransicion(p_afnd, "e", "1", "f");
	AFNDInsertaTransicion(p_afnd, "f", "0", "c");
	AFNDInsertaTransicion(p_afnd, "f", "1", "g");
	AFNDInsertaTransicion(p_afnd, "g", "0", "g");
	AFNDInsertaTransicion(p_afnd, "g", "1", "e");
	AFNDInsertaTransicion(p_afnd, "h", "0", "c");
	AFNDInsertaTransicion(p_afnd, "h", "1", "g");
	AFNDInsertaTransicion(p_afnd, "i", "0", "i");
	AFNDInsertaTransicion(p_afnd, "i", "1", "d");
	
	
	return p_afnd;
}

int main(int argc, char ** argv)
{
	AFND * p_afnd;
	AFND * p_afnd_min;
	
	p_afnd = test1();

	p_afnd_min = AFNDMinimiza(p_afnd);

	if (p_afnd_min != NULL) {

		AFNDADot(p_afnd_min);
		AFNDImprime(stdout,p_afnd_min);
		AFNDElimina(p_afnd_min);

	}
	
	
	AFNDElimina(p_afnd);
	

	return 0;
}