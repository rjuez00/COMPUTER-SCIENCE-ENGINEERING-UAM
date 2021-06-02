FLAGS = 


all: bison flex compile

syntax: bison y.tab.o

bison: alfa.y
	bison -d -y -v alfa.y

compile: y.tab.o lex.yy.o pruebaSintactico.o
	gcc -Wall -o pruebaSintactico $^ 

morfo: flex lex.yy.o

flex: alfa.l
	flex alfa.l

y.tab.o: y.tab.c
	gcc -Wall -c y.tab.c

lex.yy.o: lex.yy.c
	gcc -Wall -c lex.yy.c

pruebaSintactico.o: pruebaSintactico.c
	gcc -Wall -c pruebaSintactico.c

clean:
	rm -rf y.output y.tab.c y.tab.h lex.yy.c *.o pruebaSintactico misalida_sin_1.txt misalida_sin_2.txt misalida_sin_3.txt

tests: all
	bash tests.sh