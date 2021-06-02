CC = gcc 
CFLAGS = -g 
NUMBERS = 1 2 3 4 5 6 7
SHELL=/bin/bash
FOLDER = tests
.PHONY = exec clean

all: prueba_tabla


prueba_tabla: hash.o SymbolTable.o main.o
	$(CC) $(CFLAGS) -o prueba_tabla $^
	
test_hash: hash.o test_hash.o
	$(CC) $(CFLAGS) -o test_hash $^
	./test_hash

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	@echo cleaning
	@rm -rf *.o prueba_tabla test_hash

valgrind: prueba_tabla
	valgrind --leak-check=full ./prueba_tabla tests/input1.txt tests/ouroutput1.txt 

diff:
	@diff -Bb $(FOLDER)/output1.txt myoutput1.txt
 
execute: prueba_tabla
	./prueba_tabla $(FOLDER)/input1.txt myoutput1.txt
	diff -Bb $(FOLDER)/output1.txt myoutput1.txt
	make clean
