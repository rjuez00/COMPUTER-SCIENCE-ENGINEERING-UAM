# -*- coding: utf-8 -*-

import sys
import traceback
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.pool import NullPool
import pymongo

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1",
                          echo=False, poolclass=NullPool)
db_meta = MetaData(bind=db_engine)


def obtain_image(name):
    '''
Función: obtain_image
Descripción: devuelve la imagen pedida
Argumentos: name
Return: imagen
'''
    return 'images/' + name.replace(" ", "").replace("'", "").\
        replace(",", "").replace(".", "") + '.jpg'


def db_checkUserEmail(email, pwd=None):
    '''
Función: db_checkUserEmail
Descripción: comprueba las credenciales del usuario son correctas
Argumentos: email, pwd(default None)
Return: True/False/None
'''
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        # Seleccionar las peliculas del anno 1949
        if pwd is None:
            db_result = list(db_conn.execute("SELECT email\
                                             FROM customers\
                                             WHERE email = '{}'".
                                             format(email)).fetchall())
            if len(list(db_result)) == 0:
                db_conn.close()
                return False
        else:
            db_result = list(db_conn.execute("SELECT email\
                                             FROM customers\
                                             WHERE\
                                             email = '{}'\
                                             AND password = '{}'".
                                             format(email, pwd)).fetchall())
            if len(list(db_result)) == 0:
                db_conn.close()
                return False
        db_conn.close()
        return True
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        return None


def db_getUserbyEmail(email):
    '''
Función: db_getUserbyEmail
Descripción: devuelve el nombre de usuario y su id a partir del email
Argumentos: email
Return: db_result
'''
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_result = list(db_conn.execute("    SELECT username, customerid\
                                              FROM customers\
                                              WHERE\
                                                email = '{}'\
                                          ".format(email)).fetchall())
        db_result = {'username': db_result[0][0], 'id': db_result[0][1]}

        db_conn.close()
        return db_result
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_getHistory(customerid):
    '''
Función: db_getHistory
Descripción: devuelve el historial de un usuario dado por su customerid
Argumentos: customerid
Return: historial
'''
    query = "   SELECT  orders.orderid, orderdate, totalamount, status,\
                imdb_movies.movietitle, quantity\
                FROM orders\
                INNER JOIN orderdetail\
                    ON orderdetail.orderid = orders.orderid\
                INNER JOIN products ON\
                    products.prod_id = orderdetail.prod_id\
                INNER JOIN imdb_movies ON\
                    products.movieid = imdb_movies.movieid\
                WHERE\
                    orders.customerid = {}\
                    AND orders.status <> ''\
                ORDER BY orderdate DESC".format(customerid)
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_result = list(db_conn.execute(query).fetchall())
        historial = {}
        # key el orderid
        # value tupla (orderdate, totalamount, status, [(prod_id, quantity)])
        for row in db_result:
            value = historial.get(row[0])
            if value is None:
                historial[row[0]] = (row[1], row[2], row[3],
                                     [(row[4], row[5])])
                # (orderdate, totalamount, status, [(prod_id, quantity)])
            else:
                orderdate, totalamount, status, orders = value
                orders.append((row[4], row[5]))

        db_conn.close()
        return historial
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_newUser(address1, city, country, email, creditcard,
               creditcardexpiration, username, password):
    '''
Función: db_newUser
Descripción: crea un nuevo usuario a partir de los datos pasados por argumentos
Argumentos: address1, city, country, email, creditcard,
creditcardexpiration, username, password
Return: Void
'''
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        print("CREATING NEW USER")

        customerid = db_conn.execute("   SELECT customerid\
                                        FROM customers\
                                        ORDER BY customerid DESC\
                                        LIMIT 1").scalar() + 1

        db_conn.execute("\
            INSERT INTO customers\
            (income, customerid, firstname, lastname,\
            address1, city, country, region, email,\
            creditcardtype, creditcard, creditcardexpiration,\
            username, password)\
            VALUES\
                (0, {}, 'NA', 'NA', '{}', '{}', '{}', '{}', '{}', 'NA',\
                '{}', '{}', '{}', '{}')".format(
                 customerid, address1, city, country, country, email,
                 creditcard, creditcardexpiration, username, password
                ))

        db_conn.close()
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_getPreviewMovie(id):
    '''
Función: db_getPreviewMovie
Descripción: devuelve el título, géneros, imagen e id de la película solicitada
Argumentos: id
Return: db_result
'''
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Seleccionar titulo y año
        db_result = list(db_conn.execute("\
                        SELECT imdb_movies.movietitle, imdb_genres.genre\
                        FROM imdb_movies\
                        INNER JOIN imdb_genremovies ON\
                            imdb_genremovies.movieid = imdb_movies.movieid\
                        INNER JOIN imdb_genres ON\
                            imdb_genres.genreid = imdb_genremovies.genreid\
                        WHERE imdb_movies.movieid = {};"
                         .format(id)).fetchall())
        if len(db_result) == 0:
            return None
        db_conn.close()
        return {'title': db_result[0][0],
                'genres': [row[1] for row in db_result],
                'img': obtain_image(db_result[0][0]),
                'id': id}
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_getSimpleInfoMovie(id):
    '''
Función: db_getSimpleInfoMovie
Descripción: devuelve el título, géneros, directores,
poster y precio de la película solicitada para mostrarse en el carrito
Argumentos: id
Return: db_result/None
'''
    try:
        db_conn = None
        db_conn = db_engine.connect()
        result = {}
        db_result = list(db_conn.execute("\
                                        SELECT price, movietitle\
                                        FROM imdb_movies\
                                        INNER JOIN products ON \
                                        imdb_movies.movieid = products.movieid\
                                        WHERE imdb_movies.movieid = {}"
                                         .format(id)).fetchall())

        result['precio'] = db_result[0][0]
        result['titulo'] = db_result[0][1]
        result['poster'] = obtain_image(result['titulo'])

        result['director'] = [director for director, in list(db_conn.execute("\
                                SELECT distinct(imdb_directors.directorname)\
                                FROM imdb_movies\
                                INNER JOIN products ON \
                                imdb_movies.movieid = products.movieid\
                                INNER JOIN imdb_directormovies ON\
                                imdb_movies.movieid =\
                                imdb_directormovies.movieid\
                                INNER JOIN imdb_directors ON\
                                imdb_directormovies.directorid =\
                                imdb_directors.directorid\
                                WHERE imdb_movies.movieid = {}\
                                ".format(id)).fetchall())]

        result['categoria'] = [genre for genre, in list(db_conn.execute("\
                                SELECT distinct(imdb_genres.genre)\
                                FROM imdb_movies\
                                INNER JOIN products ON \
                                imdb_movies.movieid = products.movieid\
                                INNER JOIN imdb_genremovies ON\
                                imdb_genremovies.movieid =\
                                imdb_movies.movieid\
                                INNER JOIN imdb_genres ON\
                                imdb_genres.genreid =\
                                imdb_genremovies.genreid\
                                WHERE imdb_movies.movieid = {}\
                                ".format(id)).fetchall())]

        if len(db_result) == 0:
            return None
        db_conn.close()
        return result
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_getInfoMovie(id):
    '''
Función: db_getInfoMovie
Descripción: devuelve el título, géneros, directores, actores,
poster, precio y el año de la película solicitada para mostrarse
en la sección de información de una pelíclua
Argumentos: id
Return: result, resultactors/ None, None
'''
    # title, año(year), director, genre,
    # lista actores.actorname con nombre(actors.)
    # y personaje (actormovies.ascharacter)
    result = {}
    resultactors = []
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Seleccionar titulo y año
        db_result = db_conn.execute("SELECT movietitle, year\
        FROM imdb_movies WHERE movieid = {};".format(id)).fetchall()

        db_result = list(db_result)
        if len(db_result) == 0:
            return None, None

        result['title'] = db_result[0][0]
        result['img'] = obtain_image(result['title'])

        result['year'] = db_result[0][1]

        # Selecciona género
        db_result = db_conn.execute("SELECT imdb_genres.genre\
                                    FROM imdb_genremovies\
                                    JOIN imdb_genres ON imdb_genres.genreid =\
                                    imdb_genremovies.genreid\
                                    WHERE movieid = {};".format(id))

        result['genre'] = list(db_result.fetchall())

        # Selecciona director
        db_result = db_conn.execute("SELECT imdb_directors.directorname\
                                     FROM imdb_directormovies\
                                     JOIN imdb_directors ON\
                                     imdb_directors.directorid =\
                                     imdb_directormovies.directorid\
                                     WHERE movieid = {};".format(id))

        result['director'] = list(db_result.fetchall())

        result['price'] = db_conn.execute("SELECT price\
                                                FROM products\
                                                WHERE movieid = {}\
                                                ORDER BY price\
                                                LIMIT 1;".format(id)).scalar()

        db_actors_result = db_conn.execute("SELECT character, actorname\
                                            FROM imdb_actormovies\
                                            INNER JOIN imdb_actors ON\
                                            imdb_actors.actorid =\
                                            imdb_actormovies.actorid\
                                            WHERE imdb_actormovies.movieid ={}"
                                           .format(id)).fetchall()
        db_conn.close()
        for row in list(db_actors_result):
            resultactors.append({'character': row[0],
                                'name': row[1], 'img': obtain_image(row[1])})

        return result, resultactors
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


# name (string), genre(int)
def db_searchMovie(name, genre=None):
    '''
Función: db_searchMovie
Descripción: devuelve películas con nombre parecido al argumento y
género igual al alrgumento genre (si hubiera), esta función es la
encargada de realizar las búsquedas de películas en la página inicial
Argumentos: name, genre (default None)
Return: db_result
'''
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        name = name.replace("'", "''")
        if genre is None:
            db_result = [result for result,
                         in list(db_conn.execute(" SELECT movieid\
                                                   FROM imdb_movies\
                                                   WHERE\
                                                   imdb_movies.movietitle\
                                                   LIKE\
                                                   '%%" + name + "%%';")
                                 .fetchall())]
        else:
            db_result = [result for result, in list(db_conn.execute("\
            SELECT imdb_movies.movieid\
            FROM imdb_movies\
            INNER JOIN imdb_genremovies ON\
                imdb_genremovies.movieid = imdb_movies.movieid\
            WHERE\
                imdb_movies.movietitle LIKE '%%{}%%'\
                AND imdb_genremovies.genreid = {}\
            ".format(name, genre)
            ).fetchall())]

        print('resultado para ', name, ' y ', genre, ': ', db_result)
        db_conn.close()

        return db_result
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_getSetGenres():
    '''
Función: db_getSetGenres
Descripción: devuelve todos los géneros
de películas disponibles para mostrarlos en el
desplegable de selección de género de la página de inicio
Argumentos: Void
Return: db_result/None
'''
    try:
        db_conn = None
        db_conn = db_engine.connect()
        # Seleccionar las peliculas del anno 1949
        db_result = [{'id': row[0], 'name': row[1]} for row in list(db_conn.execute("SELECT genreid, genre\
                                                         FROM imdb_genres\
                                                         ORDER BY genre\
                                                        ").fetchall())]

        db_conn.close()
        return list(db_result)
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR DATABASE")
        return None


def db_getTopVentas():
    '''
Función: db_getTopVentas
Descripción: devuelve el id, año, título, ventas y poster
de las películas más vendidas en los últimos 3 años,
esto se muestra en la página inicial
Argumentos: Void
Return: db_result/None
'''
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Seleccionar las peliculas del anno 1949
        db_result = [{'id': db_searchMovie(row[1])[0], 'año': int(row[0]),
                      'pelicula': row[1], 'ventas': row[2],
                      'img': obtain_image(row[1])}
                     for row in list(db_conn.execute("SELECT * FROM getTopVentas(EXTRACT(year from NOW())-2,\
                                                     EXTRACT(year\
                                                     from NOW()));")
                                     .fetchall())]

        db_conn.close()
        return list(db_result)
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR DATABASE")
        return None


def db_deleteOldCarrito(customerid):
    '''
Función: db_deleteOldCarrito
Descripción: borra el carrito del usuario
pasado como argumento
Argumentos: customerid
Return: Void
'''
    query = "   DELETE\
                FROM orders\
                WHERE \
                    customerid = {}\
                    AND status = ''".format(customerid)
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_conn.execute(query)

        db_conn.close()
        return
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_resetCarrito(customerid, carrito=None):
    '''
Función: db_resetCarrito
Descripción: resetea el carrito de un usuario,
copiando en él toda la información pasada por el argumento
Argumentos: customerid, carrito (default None)
Return: Void/None
'''
    orderid = "SELECT orderid FROM orders ORDER BY orderid DESC LIMIT 1"
    creationcarrito = "     INSERT INTO orders\
                            (orderid, orderdate, customerid,\
                            netamount, tax, totalamount, status)\
                            VALUES\
                            ({}, NOW(), {}, 0, 21, 0, '')\
                            "
    insertmovie = " INSERT INTO orderdetail\
                        (orderid, prod_id, price, quantity)\
                    VALUES\
                        ({}, {}, {}, {})"
    prodidprice = " SELECT prod_id, price\
                    FROM products\
                    WHERE movieid = {}\
                    ORDER BY price\
                    LIMIT 1"
    db_deleteOldCarrito(customerid)
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        orderid = db_conn.execute(orderid).scalar()+1
        db_result = db_conn.execute(creationcarrito
                                    .format(orderid, customerid))

        if carrito is None:
            db_conn.close()
            return

        cantidades = {}
        for movieid in carrito:
            cantidades[movieid] = cantidades.get(movieid, 0)+1

        products = {}
        prices = {}
        for movieid in cantidades:
            db_result = list(db_conn.execute(prodidprice
                                             .format(movieid)).fetchall())
            products[movieid] = db_result[0][0]
            prices[movieid] = db_result[0][1]

        for movieid, quantity in cantidades.items():
            db_result = db_conn.execute(insertmovie
                                        .format(orderid, products[movieid],
                                                prices[movieid], quantity))

        db_conn.close()
        return
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR DATABASE")
        return None


def db_loadCarrito(customerid):
    '''
Función: db_loadCarrito
Descripción: devuelve el carrito de la
base de datos asociado al usuario pedido
Argumentos: customerid
Return: carrito
'''
    query = "   SELECT distinct(products.movieid)\
                FROM orders\
                INNER JOIN orderdetail ON\
                    orders.orderid = orderdetail.orderid\
                INNER JOIN products ON\
                    products.prod_id = orderdetail.prod_id\
                WHERE\
                    orders.customerid = {}\
                    AND orders.status = ''"
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        carrito = [str(movieid) for movieid,
                   in list(db_conn.execute(query
                                           .format(customerid)).fetchall())]

        db_conn.close()
        return carrito
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_updateCarrito(customerid, movieid, quantity):
    '''
Función: db_updateCarrito
Descripción: actualiza el carrito del usuario
pedido, modificando la cantidad de una película o
añadiendo una película nueva
Argumentos: customerid, movieid, quantity
Return: Void
'''
    orderid = " SELECT orderid\
                FROM orders\
                WHERE\
                    customerid = {}\
                    AND status = ''"
    addmovie = "INSERT INTO orderdetail\
                    (orderid, prod_id, price, quantity)\
                VALUES\
                    ({}, {}, {}, {})"
    dropmovie = "DELETE\
                FROM orderdetail\
                WHERE\
                    orderid = {}\
                    AND prod_id = {}"
    prodidprice = "SELECT prod_id, price\
                    FROM products\
                    WHERE movieid = {}\
                    ORDER BY price\
                    LIMIT 1"
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        orderid = db_conn.execute(orderid.format(customerid)).scalar()
        db_result = list(db_conn.execute(prodidprice
                                         .format(movieid)).fetchall())
        prodid = db_result[0][0]
        price = db_result[0][1]

        db_result = db_conn.execute(dropmovie.format(orderid, prodid))
        db_result = db_conn.execute(addmovie
                                    .format(orderid, prodid, price, quantity))
        db_conn.close()
        return
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_deleteMovieCarrito(customerid, movieid):
    '''
Función: db_deleteMovieCarrito
Descripción: borra la película solicitada
del carrito del usuario pedido
Argumentos: customerid, movieid
Return: Void
'''
    orderid = " SELECT orderid\
                FROM orders\
                WHERE\
                    customerid = {}\
                    AND status = ''"

    dropmovie = "DELETE\
                FROM orderdetail\
                WHERE\
                    orderid = {}\
                    AND prod_id = {}"

    prodidprice = "SELECT prod_id\
                    FROM products\
                    WHERE movieid = {}\
                    ORDER BY price\
                    LIMIT 1"
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        orderid = db_conn.execute(orderid.format(customerid)).scalar()
        db_result = list(db_conn.execute(prodidprice
                                         .format(movieid)).fetchall())
        prodid = db_result[0][0]

        db_result = db_conn.execute(dropmovie.format(orderid, prodid))

        db_conn.close()
        return
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_getSaldo(customerid):
    '''
Función: db_getSaldo
Descripción: devuelve el saldo de el usuario
pedido, esto se mostrará en la página de historial
Argumentos: customerid
Return: saldo
'''
    query = "   SELECT income\
                FROM customers\
                WHERE customerid = {}".format(customerid)
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        saldo = db_conn.execute(query).scalar()
        db_conn.close()
        return saldo
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_updateSaldo(customerid, addsaldo):
    '''
Función: db_updateSaldo
Descripción: añade saldo al usuario pedido
Argumentos: customerid, addsaldo
Return: Void
'''
    query = "\
        UPDATE customers\
        SET income = income + {}\
        WHERE customerid = {}\
    ".format(addsaldo, customerid)
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        db_conn.execute(query)
        db_conn.close()
        return
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_buyCarrito(customerid):
    '''
Función: db_buyCarrito
Descripción: realiza las modificaciones necesarias
en la base de datos cuando el usuario compra el carrito,
resta el saldo correspondiente al pedido, actualiza el
estado del pedido a 'Pais', lo que hace que se active el
trigger de updInventory y actualice el stock y los sales
Argumentos: customerid
Return: Void
'''
    totalamount = " SELECT totalamount\
                    FROM orders\
                    WHERE \
                        customerid = {}\
                        AND status = ''\
                    ".format(customerid)
    updatesaldo = "\
        UPDATE customers\
        SET income = income - {}\
        WHERE customerid = {}\
            "
    setpaid = " UPDATE orders\
                SET status = 'Paid'\
                WHERE\
                    customerid = {}\
                    AND status = ''".format(customerid)
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        totalamount = db_conn.execute(totalamount).scalar()
        db_conn.execute(updatesaldo.format(totalamount, customerid))
        db_conn.execute(setpaid)

        db_resetCarrito(customerid=customerid)

        db_conn.close()
        return
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_obtainStock(movieid):
    query = "   SELECT stock\
                FROM inventory\
                INNER JOIN products ON\
                    products.prod_id = inventory.prod_id\
                WHERE products.movieid = {}\
                ORDER BY products.price\
                LIMIT 1".format(movieid)
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        stock = db_conn.execute(query).scalar()

        db_conn.close()
        return stock
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def db_getNamefromId(movieid):
    query = "SELECT movietitle\
                FROM imdb_movies\
                WHERE movieid = {}".format(movieid)
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        name = list(db_conn.execute(query).fetchall())[0][0]

        db_conn.close()
        return name
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("ERROR")
        traceback.print_exc(file=sys.stderr)


def mongodb_a():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    col = myclient['si1']['topUSA']
    a = col.find({'year': '1997',
                  'title': {"$regex": "Life+"},
                  'genres': 'Comedy'
                  })
    myclient.close()
    return a


def mongodb_b():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    col = myclient['si1']['topUSA']
    b = col.find({'directors': "Allen, Woody",
                  'year': {"$regex": "199+"}
                  })
    myclient.close()
    return b


def mongodb_c():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    col = myclient['si1']['topUSA']
    c = col.find({'actors': {"$all": ["Parsons, Jim (II)",
                                      "Galecki, Johnny"]}})
    myclient.close()
    return c
