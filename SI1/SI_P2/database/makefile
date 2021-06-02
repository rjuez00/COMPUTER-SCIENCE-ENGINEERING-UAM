FOLDER = queries

all: reset_db actualiza
reset_db: drop_db create_db actualiza setPrice setOrderAmount getTopVentas getTopMonths updOrders updInventory


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

testupdOrder:
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/testupdOrder.sql

testupdInventory:
	psql alumnodb -h localhost -d si1 -f $(FOLDER)/testupdInventory.sql
