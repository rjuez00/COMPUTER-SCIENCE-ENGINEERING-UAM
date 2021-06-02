# Version 1.2
# Modificacion
# 1) Las consultas 1 y 2 se han intercambiado para que sigan el mismo orden 
#    que en el enunciado de la práctica
# 2) se ha añadido la opción allqueries la cual ejecuta todas las consultas
# Por lo general no se requiere modificar el fichero

export PGDATABASE:=dvdrental
export PGDATABASE4:= newdatabase
export PGUSER :=alumnodb
export PGPASSWORD :=alumnodb
export PGCLIENTENCODING:=LATIN9
export PGHOST:=localhost

DBNAME =$(PGDATABASE)
DBNAME4 = $(PGDATABASE4)
PSQL = psql
CREATEDB = createdb
DROPDB = dropdb --if-exists
PG_DUMP = pg_dump
PG_RESTORE = pg_restore


CC = gcc -ansi -pedantic
CFLAGS = -Wall -lrt -g -lodbc
EXE = dvdreq

all: clean_exe dvdreq dvdrent dvdfilm clean
db: dropdb createdb restore
c_db: clean_exe dropdb createdb restore dvdreq dvdrent dvdfilm clean
###################################### COMPILE ################################
dvdreq.o: dvdreq.c
	gcc -c $(CFLAGS) $<

dvdrent.o: dvdrent.c
	gcc -c $(CFLAGS) $<

dvdfilm.o: dvdfilm.c
	gcc -c $(CFLAGS) $<

odbc.o: odbc.c odbc.h
	gcc -c $(CFLAGS) $<

###################################### LINK ###################################

dvdreq: odbc.o dvdreq.o
	gcc $^ $(CFLAGS) -o dvdreq

dvdrent: odbc.o dvdrent.o
	gcc $^ $(CFLAGS) -o dvdrent

dvdfilm: odbc.o dvdfilm.o
	gcc $^ $(CFLAGS) -o dvdfilm

##################################### OTHER ####################################

clean: 
	rm -f *.o

clean_exe:
	rm -f *.o
	rm -f dvdreq
	rm -f dvdrent
	rm -f dvdfilm

####################################### SQL ####################################
createdb:
	@echo Creando BBDD
	@$(CREATEDB)
dropdb:
	@echo Eliminando BBDD
	@$(DROPDB) $(DBNAME)
	rm -f *.log
dump:
	@echo creando dumpfile
	@$(PG_DUMP) > $(DBNAME).sql
restore:
	@echo restore data base
	@cat $(DBNAME).sql | $(PSQL)  
shell:
	@echo create psql shell
	@$(PSQL)  

allqueries: query1 query2 query3 query4 query5 query6
	@cat query?.log > all_queries.log

query1:
	@echo query-1: "Alquireles por año" | tee query1.log
	@cat query1.sql | $(PSQL) | tee -a query1.log
query2:
	@echo query-2: "clienet que ha alquilado más peliculas" | tee query2.log
	@cat query2.sql | $(PSQL) | tee -a query2.log
query3:
	@echo query3: "Ciudades alquiler Bob Fawcett" | tee query3.log
	@cat query3.sql | $(PSQL) | tee -a query3.log
query4:
	@echo query4: "lenguaje en el que se producen más películas" | tee query4.log
	@cat query4.sql | $(PSQL) | tee -a query4.log
query5:
	@echo query5: "lenguaje en el que se alquilan más películas" | tee query5.log
	@cat query5.sql | $(PSQL) | tee -a query5.log
query6:
	@echo query6: "categoría favorita del cliente que alquila más peliculas" | tee query6.log
	@cat query6.sql | $(PSQL) | tee -a query6.log

newdatabase: dropdb createdb4 restore4

createdb4:
	@echo Creando BBDD
	@$(CREATEDB)

restore4:
	@echo restore data base
	@cat $(DBNAME4).sql | $(PSQL)
