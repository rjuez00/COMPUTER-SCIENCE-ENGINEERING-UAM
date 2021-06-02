FLAGS = -Wall -ansi -pedantic -g
OBJECTS= list.o node.o queuel.o p3_testqueuel.o
.PHONY: all clean tidy 

all: clean ex3 tidy

ex3: $(OBJECTS)
	gcc $^ -o p3_testqueuel

node.o: node.c 
	gcc -c $(FLAGS) $^

list.o: list.c 
	gcc -c $(FLAGS) $^

queuel.o: queuel.c 
	gcc -c $(FLAGS) $^

clean:
	rm -f p3_testqueuel
	rm -f *.o
tidy:
	rm -f *.o

runv:
	valgrind --leak-check=full ./p3_testqueuel nodes.txt
