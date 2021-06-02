CC = gcc
SRCLIB = srclib
INCLUDE = includes
LIB = lib
SRC = src
OBJ = obj
CFLAGS = -Wall -g -I./$(INCLUDE)

.PHONY: server syslog cliente


all : main

main: main.o log.o servidor.o pool_thread.o socket.o picohttpparser.o cgi.o response.o http.o libraries tidy 
	gcc $(CFLAGS) -o main $(OBJ)/main.o -pthread -L/usr/local/lib $(LIB)/server.a -lconfuse $(LIB)/http.a

libraries:
	ar -rc http.a http.o cgi.o picohttpparser.o response.o
	ar -rc server.a servidor.o socket.o log.o pool_thread.o

server: main
	./main


cliente: $(SRC)/test_socket_client.c
	gcc $(SRC)/test_socket_client.c -o cliente 

log.o: $(SRCLIB)/log.c $(INCLUDE)/log.h
	gcc -c $(CFLAGS) $< 
	
response.o:
	gcc -c -Wall -g -I./includes srclib/response.c

servidor.o: $(SRCLIB)/servidor.c  $(INCLUDE)/servidor.h  $(INCLUDE)/log.h
	gcc -c $(CFLAGS) $< 

socket.o: $(SRCLIB)/socket.c  $(INCLUDE)/socket.h  $(INCLUDE)/log.h
	gcc -c $(CFLAGS) $<
	
pool_thread.o: $(SRCLIB)/pool_thread.c  $(INCLUDE)/pool_thread.h $(INCLUDE)/picohttpparser.h $(INCLUDE)/http.h $(INCLUDE)/log.h
	gcc -c $(CFLAGS) $<

http.o: $(SRCLIB)/http.c  $(INCLUDE)/http.h  $(INCLUDE)/cgi.h $(INCLUDE)/picohttpparser.h 
	gcc -c $(CFLAGS) $<

cgi.o: $(SRCLIB)/cgi.c  $(INCLUDE)/cgi.h
	gcc -c $(CFLAGS) $<
	
picohttpparser.o: $(SRCLIB)/picohttpparser.c  $(INCLUDE)/picohttpparser.h
	gcc -c $(CFLAGS) $<
	
main.o: $(SRC)/main.c $(INCLUDE)/servidor.h
	gcc -c $(CFLAGS) $<

tidy:
	mkdir -p obj
	mkdir -p lib
	mv *.o obj
	mv *.a lib

valgrind: main
	valgrind --leak-check=full --track-origins=yes ./main

clean:
	rm -rf *.o main cliente
	rm lib/*.a obj/*.o

syslog:
	tail -n 50  /var/log/syslog

hola:
	curl -i -X GET http://127.0.0.1:8080/hola

nohost: 
	curl -i -H 'Host:' -X GET http://127.0.0.1:8080/hola

closed:
	curl -i http://127.0.0.1:8080/a.html -H "Connection: close"

typetext:
	curl -i -X GET http://127.0.0.1:8080/a.html 

script:
	curl -i -X GET http://127.0.0.1:8080/scripts/backend.py?var1=abcd&var2=efgh 

typejpg:
	curl -i -X GET http://127.0.0.1:8080/eps.jpg 


options:
	curl -X OPTIONS http://127.0.0.1:8080/a.html -i

head:
	curl -I http://127.0.0.1:8080/a.html -i

compare:
	cmp -l htmlfiles/p.jpg imagen_enviada.jpg 

post:
	curl -d "say=Hi&to=Mom" -X POST http://127.0.0.1:8080/scripts/backend.py

post2:
	curl -d "say=Hi&to=Mom" -X POST http://127.0.0.1:8080/a.html

kill_server:
	kill -2 $$(ps -aux | grep ./main | head -n 1 | awk '{ print $$2 }')