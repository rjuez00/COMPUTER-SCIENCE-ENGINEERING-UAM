// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// +++++++++++   Practica 3 - SBM 2020
// +++++++++++
// Nombre:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#include <stdlib.h>
#include <stdio.h>

int calculaMediana(int a, int b, int c, int d);
void enteroACadenaHexa (int num, char* outStr);
void calculaLetraDNI(char* inStr, char* letra);

int main(){
	int eleccion =0, salir=0,m1,m2,m3,m4,mediana;
	unsigned int a,b, c;
	char cadena[100];
	char cadena1;
	
	do{
		printf("Elija la funcion que desea utilizar (introduzca el numero):\n");
		printf("\t1.-Calcular la mediana de cuatro numeros\n");
		printf("\t2.-Transformar un entero dado a hexadecimal\n");
		printf("\t3.-Calcular la letra de un DNI dado\n");
		scanf("%d", &eleccion);
		switch(eleccion){
			case 1:
				printf("Introduzca el primer numero:\n");
				scanf("%d", &m1);
				printf("Introduzca el segundo numero:\n");
				scanf("%d", &m2);
				printf("Introduzca el tercer numero:\n");
				scanf("%d", &m3);
				printf("Introduzca el cuarto numero:\n");
				scanf("%d", &m4);
				mediana=calculaMediana(m1,m2,m3,m4);
				printf("La mediana de %d %d %d %d es %d\n", m1, m2, m3,m4,mediana);
				break;
			
			case 2:
				printf("Introduzca el numero\n");
				scanf("%d",&m1);
				enteroACadenaHexa (m1, cadena);
				printf("El numero %d en hexadecimal es: %s\n",m1,cadena);
				break;
			case 3:
				printf("Introduzca el DNI\n");
				scanf("%s",cadena);
				calculaLetraDNI(cadena, &cadena1);
				printf("La letra del DNI %s es: %c\n",cadena,cadena1);
				break;
			default:
				printf("Numero incorrecto\n");
				break;
		}
		printf("Desea ejecutar otra funcion? SI=0/ NO=1\n");
		scanf("%d",&salir);
	}while(salir==0);
	return 0;
}