CC = gcc 
CFLAGS = -g -m32
NUMBERS = 1 2 3 4 5 6 7
SHELL=/bin/bash
FOLDER = ficheros_prueba_morfologico

.PHONY: ejemplo1 ejemplo2 ejemplo3 separator
all: do 
test: ejemplo1 separator ejemplo2 ejemplo3


do:
	@echo calling flex
	@flex alfa.l
	@echo compiling lex.yy.c
	@gcc -Wall -o pruebaMorfo lex.yy.c 


clean:
	@echo cleaning
	@rm -rf lex.yy.c pruebaMorfo CLUTTER_IM_MODULE=xim myoutput1.txt myoutput2.txt myoutput3.txt
