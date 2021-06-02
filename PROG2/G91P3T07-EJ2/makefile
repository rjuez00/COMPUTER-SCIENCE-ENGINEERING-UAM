FLAGS = -Wall -ansi -pedantic -g
OBJECTS= list.o int.o p3_e2.o
.PHONY: all clean tidy 

all: clean ex2 tidy

ex2: $(OBJECTS)
	gcc $^ -o p3_e2

p3_e2.o: p3_e2.c
	gcc -c $(FLAGS) $^

int.o: int.c 
	gcc -c $(FLAGS) $^

list.o: list.c 
	gcc -c $(FLAGS) $^

clean:
	rm -f p3_e2
	rm -f *.o
tidy:
	rm -f *.o

runv:
	valgrind --leak-check=full ./p3_e2 5
	valgrind --leak-check=full ./p3_e2 8
	valgrind --leak-check=full ./p3_e2 99
	
run: all
	./p3_e2
