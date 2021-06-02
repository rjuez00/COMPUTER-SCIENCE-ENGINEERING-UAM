########################################################
CC=gcc
CFLAGS= -g -Wall -pedantic -ansi
EJS = p4_e1 p4_e2 p4_e3 p4_test-node-tree p4_e4
########################################################
OBJECTSP4_E1 = p4_e1.o tree.o int.o
OBJECTSP4_E2 = p4_e2.o tree.o node.o int.o
OBJECTSP4_E3 = p4_e3.o tree.o node.o
OBJECTSP4_TNT = p4_test-node-tree.o tree.o node.o
OBJECTSP4_E4 = p4_e4.o tree.o string.o
########################################################

all: $(EJS) clear

p4_e1: $(OBJECTSP4_E1)
	$(CC) $(CFLAGS) -o p4_e1 $(OBJECTSP4_E1)

p4_e2: $(OBJECTSP4_E2)
	$(CC) $(CFLAGS) -o p4_e2 $(OBJECTSP4_E2)

p4_e3: $(OBJECTSP4_E3)
	$(CC) $(CFLAGS) -o p4_e3 $(OBJECTSP4_E3)

p4_test-node-tree: $(OBJECTSP4_TNT)
	$(CC) $(CFLAGS) -o p4_test-node-tree $(OBJECTSP4_TNT)

p4_e4: $(OBJECTSP4_E4)
	$(CC) $(CFLAGS) -o p4_e4 $(OBJECTSP4_E4)

p4_e1.o: p4_e1.c tree.h node.h
	$(CC) $(CFLAGS) -c p4_e1.c

p4_e2.o: p4_e2.c tree.h node.h
	$(CC) $(CFLAGS) -c p4_e2.c

p4_e3.o: p4_e3.c tree.h node.h
	$(CC) $(CFLAGS) -c p4_e3.c

p4_test-node-tree.o: p4_test-node-tree.c tree.h node.h
	$(CC) $(CFLAGS) -c p4_test-node-tree.c

p4_e4.o: p4_e4.c tree.h string.h
	$(CC) $(CFLAGS) -c p4_e4.c

string.o: string.c string.h
	$(CC) $(CFLAGS) -c string.c

tree.o: tree.c tree.h
	$(CC) $(CFLAGS) -c tree.c

node.o: node.c node.h
	$(CC) $(CFLAGS) -c node.c

clear:
	rm -rf *.o 

clean:
	rm -rf *.o $(EJS) .vscode/ipch

run:
	@echo ">>>>>>Running p4_e1"
	./p4_e1 numeros.txt
	@echo ">>>>>>Running p4_e2"
	./p4_e2 numeros.txt
	@echo ">>>>>>Running p4_test-node-tree"
	./p4_test-node-tree nodos.txt
	@echo ">>>>>>Running p4_e3 non balanced"
	./p4_e3 dict10.dat N
	@echo ">>>>>>Running p4_e3 balanced"
	./p4_e3 dict10.dat B
	@echo ">>>>>>Running p4_e4"
	./p4_e4 cadenas.txt

runv:
	@echo ">>>>>>Running p4_e1 with valgrind"
	valgrind --leak-check=full ./p4_e1 numeros.txt
	@echo ">>>>>>Running p4_e2 with valgrind"
	valgrind --leak-check=full ./p4_e2 numeros.txt
	@echo ">>>>>>Running p4_test-node-tree with valgrind"
	valgrind --leak-check=full ./p4_test-node-tree nodos.txt
	@echo ">>>>>>Running p4_e3 non balanced with valgrind"
	valgrind --leak-check=full ./p4_e3 dict10.dat N
	@echo ">>>>>>Running p4_e3 balanced with valgrind"
	valgrind --leak-check=full ./p4_e3 dict10.dat B
	@echo ">>>>>>Running p4_e4 with valgrind"
	valgrind --leak-check=full ./p4_e4 cadenas.txt
