CC = gcc 
CFLAGS = -g -Wall
EXE = newstate.o minimiza.o main.o 

all : main

clean:
	@rm -rf *.o *.pdf *.dot main

run: clean all
	valgrind --leak-check=full --track-origins=yes ./main
	make dot

valgrind: clean all
	valgrind --track-origins=yes ./main

leak: clean all
	valgrind --leak-check=full ./main

dot:
	dot -Tpdf *.dot -o AFD.pdf

main : $(EXE)
	@gcc -o main $(EXE) -L. -l_afnd_64
	@echo compiled

minimiza.o : minimiza.c minimiza.h
	@$(CC) $(CFLAGS) -c $<

newstate.o : newstate.c newstate.h
	@$(CC) $(CFLAGS) -c $<

main.o : main.c minimiza.h
	@$(CC) $(CFLAGS) -c $<
