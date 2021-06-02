# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si2", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):

    # TODO: implementar la consulta; asignar nombre 'cc' al contador resultante
    consulta = " ... "
    
    # TODO: ejecutar la consulta 
    # - mediante PREPARE, EXECUTE, DEALLOCATE si use_prepare es True
    # - mediante db_conn.execute() si es False

    # Array con resultados de la consulta para cada umbral
    dbr=[]

    for ii in range(niter):

        # TODO: ...

        # Guardar resultado de la query
        dbr.append({"umbral":iumbral,"contador":res['cc']})

        # TODO: si break0 es True, salir si contador resultante es cero
        
        # Actualizacion de umbral
        iumbral = iumbral + iintervalo
                
    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)
        
    resultproxy.close()  
    
    db_conn.close()  
    
    return a
    
def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()
    
    db_conn.close()

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}


def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
    # Array de trazas a mostrar en la página
    dbr = []
    del_customer = "DELETE FROM customers\
                    WHERE customerid = {}".format(customerid)
    del_order = "DELETE FROM orders\
                 WHERE customerid = {}".format(customerid)
    del_orderdetail = "DELETE FROM orderdetail\
                       USING orders WHERE orderdetail.orderid = orders.orderid\
                       AND orders.customerid = {}".format(customerid)

    estado_orderdetail = "SELECT *\
                       FROM orderdetail\
                       NATURAL JOIN orders\
                       WHERE orders.customerid = {}".format(customerid)

    estado_customer = "   SELECT *\
                            FROM customers\
                            WHERE customerid = {};".format(customerid)

    # DONE: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos
    #   en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()
    db_conn = db_engine.connect()
    connection = db_conn
    executecaller = None
    try:
        if bSQL:
            db_conn.execute("BEGIN")
            executecaller = db_conn
        else:
            db_conn = connection.begin()
            executecaller = connection
        dbr.append("Ejecutado BEGIN")
        dbr.append("Contenido Customers: " +
                   str(list(executecaller.execute(estado_customer))))
        dbr.append("Contenido OrderDetail: " +
                   str(list(executecaller.execute(estado_orderdetail))))

        executecaller.execute(del_orderdetail)

        if bCommit:
            if bSQL:
                executecaller.execute("COMMIT")
                executecaller.execute("BEGIN")
            else:
                db_conn.commit()
                db_conn = connection.begin()
            dbr.append("Ejecutando COMMIT")

        if bFallo:
            executecaller.execute(del_customer)
            if duerme != 0:
                time.sleep(duerme)
            executecaller.execute(del_order)
            dbr.append("Forzamos fallo (orden incorrecto)")
        else:
            executecaller.execute(del_order)
            if duerme != 0:
                time.sleep(duerme)
            executecaller.execute(del_customer)
            dbr.append("Ejecución normal")

        dbr.append("Durmiendo {} s...".format(duerme))

    except Exception as e:
        # deshacer en caso de error
        if bSQL:
            executecaller.execute("ROLLBACK")
        else:
            db_conn.rollback()
        dbr.append("Ejecución ROLLBACK por excepcion: " + str(e))
    else:
        # confirmar cambios si todo va bien
        if bSQL:
            executecaller.execute("COMMIT")
        else:
            db_conn.commit()
        dbr.append("Ejecución completa y correcta")

    dbr.append("Contenido Customers: " +
               str(list(executecaller.execute(estado_customer))))
    dbr.append("Contenido OrderDetail: " +
               str(list(executecaller.execute(estado_orderdetail))))
    db_conn.close()
    return dbr
