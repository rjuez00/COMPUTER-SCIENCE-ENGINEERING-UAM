FLAGS = -Wall -ansi -pedantic -g
OBJECTSTEST= p3_testqueue.o queue.o node.o graph.o
OBJECTS= queue.o node.o graph.o p3_e1.o
.PHONY: all clean tidy 

all: clean queuetest ex1 tidy

p3_testqueue.o: p3_testqueue.c
	gcc -c $(FLAGS) $^

p3_e1.o: p3_e1.c
	gcc -c $(FLAGS) $^

node.o: node.c 
	gcc -c $(FLAGS) $^

graph.o: graph.c 
	gcc -c $(FLAGS) $^

queue.o: queue.c
	gcc -c $(FLAGS) $^

queuetest: $(OBJECTSTEST)
	gcc $^ -o p3_testqueue

ex1: $(OBJECTS)
	gcc $^ -o p3_e1

clean:
	rm -f p3_testqueue
	rm -f p3_e1
	rm -f *.o
	rm -rf .vscode/ipch

tidy:
	rm -f *.o
runv:
	valgrind --leak-check=full ./p3_testqueue nodes.txt
	valgrind --leak-check=full ./p3_e1 g1.txt 3 1
	valgrind --leak-check=full ./p3_e1 g1.txt 1 3
	valgrind --leak-check=full ./p3_e1 g2_u.txt 24 120

run: all
	./p3_testqueue nodes.txt
