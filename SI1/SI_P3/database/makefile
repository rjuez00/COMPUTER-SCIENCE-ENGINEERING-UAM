FOLDER = queries
FOLDERP4 = p3
all: create_db2 mongoDB setup actualiza updPromo

reset_db: drop_db create_db 

setup: create_db actualiza setPrice setOrderAmount getTopVentas getTopMonths updOrders updInventory

clean: drop_db2 drop_db

drop_db2:
	@echo eliminando db2...
	@dropdb -U alumnodb si2

create_db2:
	@echo creando db2...
	@createdb -U alumnodb si2
	@psql alumnodb -h localhost -d si2 -f dump_v1.2-P3.sql


mongoDB:
	python3 $(FOLDERP4)/createMongoDBFromPostgreSQLDB.py
	

drop_db:
	@echo eliminando db...
	@dropdb -U alumnodb si1

create_db:
	@echo creando db...
	@createdb -U alumnodb si1
	@gunzip -c dump_v1.4.sql.gz | psql -U alumnodb si1

actualiza: 
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/actualiza.sql

queries: setPrice setOrderAmount getTopVentas getTopMonths

setPrice:
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/setPrice.sql

setOrderAmount:
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/setOrderAmount.sql

getTopVentas:
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/getTopVentas.sql

getTopMonths:
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/getTopMonths.sql

updOrders:
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/updOrders.sql

updInventory:
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/updInventory.sql

clientesDistintos:
	psql alumnodb -h localhost -d si2 -f $(FOLDERP4)/clientesDistintos.sql

anexo1:
	psql alumnodb -h localhost -d si2 -f $(FOLDERP4)/anexo1.sql

countStatus:
	psql alumnodb -h localhost -d si2 -f $(FOLDERP4)/countStatus.sql

updPromo:
	psql alumnodb -h localhost -d si2 -f $(FOLDERP4)/updPromo.sql

testupdPromo:
	psql alumnodb -h localhost -d si2 -f $(FOLDERP4)/testupdPromo.sql

testSleep:
	psql alumnodb -h localhost -d si2 -f $(FOLDERP4)/testSleep.sql
