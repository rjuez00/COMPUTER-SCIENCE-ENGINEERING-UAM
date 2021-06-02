CC = gcc 
CFLAGS = -g -m32
NUMBERS = 1 2 3 4 5 6 7
SHELL=/bin/bash

all: clean generate_and_compile

generate_and_compile: ej1.o ej2.o ej3.o ej4.o ej5.o ej6.o ej7.o generacion.o
	$(foreach var,$(NUMBERS),\
		gcc -o ej$(var)_asm ej$(var).o generacion.o ;\
		./ej$(var)_asm ej$(var).asm ; \
		nasm -g -o ej$(var)nasm.o ej$(var).asm -f elf32 ; \
		gcc -Wall -g -m32 -o ej$(var) ej$(var)nasm.o alfalib.o ; \
	)
link_objects:
	for number in 1 2 3 4 5 6 7 ; do \
		./ej$$number_asm ej$$number.asm ; \
	gcc -Wall -g -m32 -o ej1 ej1nasm.o alfalib.o

%.o: %.c
	gcc -c $<

clean:
	@echo "rm !(*.c|makefile|alfalib.o|*.h)"
	@rm -rf ej1 ej1_asm ej1.asm ej1nasm.o ej1.o ej2 ej2_asm ej2.asm ej2nasm.o ej2.o ej3 ej3_asm ej3.asm ej3nasm.o ej3.o ej4 ej4_asm ej4.asm ej4nasm.o ej4.o ej5 ej5_asm ej5.asm ej5nasm.o ej5.o ej6 ej6_asm ej6.asm ej6nasm.o ej6.o ej7 ej7_asm ej7.asm ej7nasm.o ej7.o generacion.o