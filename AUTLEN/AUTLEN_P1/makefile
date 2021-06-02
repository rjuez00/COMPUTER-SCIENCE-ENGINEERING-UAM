CC = gcc 
CFLAGS = -g -Wall
EXE = newstate.o transforma.o  main.o 

all : main

clean:
	@rm -rf *.o *.pdf *.dot main

run: clean all
	./main

valgrind: clean all
	valgrind --track-origins=yes ./main

leak: clean all
	valgrind --leak-check=full ./main

dot:
	dot -Tpdf *.dot -o AFD.pdf

main : $(EXE)
	@gcc -o main $(EXE) -L. -l_afnd_64
	@echo compiled

newstate.o : newstate.c newstate.h
	@$(CC) $(CFLAGS) -c $<

transforma.o : transforma.c transforma.h
	@$(CC) $(CFLAGS) -c $<

main.o : main.c transforma.h newstate.h
	@$(CC) $(CFLAGS) -c $<
