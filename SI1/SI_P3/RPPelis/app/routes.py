#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random

from app import app, database
from flask import render_template
from flask import request, url_for, redirect
from flask import session, send_from_directory
from flask import flash


def load_user_session(email):
    '''
Función: load_user_session
Descripción: carga en la coockie de sesión
los datos del usuario
Argumentos: email
Return: Void
'''
    info = database.db_getUserbyEmail(email)
    session["email"] = email
    session['nombre'] = info['username']
    session['id'] = int(info['id'])
    session.modified = True


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    '''
Función: index
Descripción: view encargada de la página principal,
carga desde la base de datos las TopVentas de los últimos
3 años, perimite aplica filtros de búsqueda por palabras
y/o género
Argumentos: Void
Return: render_template
'''
    topVentas = database.db_getTopVentas()

    categories = database.db_getSetGenres()
    filtro = []
    busqueda = "Buscar..."
    if 'buscar' in request.form and (request
                                     .form['buscar'] != ""
                                     or request.form['genero'] != "todo"):
        genero = (None if request.form['genero'] == 'todo'
                  else int(request.form['genero']))
        filtro = database.db_searchMovie(request.form['buscar'], genero)
        if len(filtro) != 0:
            filtro = [database.db_getPreviewMovie(movieid)
                      for movieid in filtro]
        else:
            filtro = []
        busqueda = request.form['buscar']

    return render_template('index.html',
                           movies=filtro,
                           categorias=categories,
                           novedades=topVentas,
                           busqueda=busqueda)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    '''
Función: registro
Descripción: view encargada de registrar a un nuevo usuario
si recibe un post, checkea en la base de datos los datos
proporcionados por el usuario en el formulario, si el
usuario no existe lo crea y redirecciona al usuario al index, sino
informa de que el usuario ya existe
Argumentos: Void
Return: render_template
'''
    if 'email' in request.form:
        if database.db_checkUserEmail(request.form['email']):
            return render_template('formulario_registro.html',
                                   title="Sign In",
                                   alerta="Usuario ya creado")
        else:
            database.db_newUser(request.form['address1'],
                                request.form['city'],
                                request.form['country'],
                                request.form['email'],
                                request.form['ncredito'],
                                str(request.form['fcredito']),
                                request.form['nombre'], request.form['psw1'])
            load_user_session(request.form['email'])
            return index()

    return render_template("formulario_registro.html")


@app.route('/info_peli/<film_id>', methods=['GET', 'POST'])
def info_peli(film_id):
    '''
Función: info_peli
Descripción: view encargada de mostrar la información
de una película, también ofrece la posibilidad de añadir
la película al carrito pulsando el botón comprar.
La view muestra información sobre la película como:
título, precio, año, poster, directores, género,
actores
Argumentos: film_id
Return: render_template
'''
    print('request en info_peli')

    if 'carrito' not in session:
        session['carrito'] = []
        session.modified = True

    if 'id' in request.form and request.form['id'] not in session['carrito']:
        print('post en info_peli', session['carrito'])
        if database.db_obtainStock(request.form['id']) > 0:
            print('APPEND')
            session['carrito'].append(request.form['id'])
            session.modified = True
            if 'id' in session:
                database.db_updateCarrito(session['id'],
                                          int(request.form['id']),
                                          1)
        else:
            flash('no hay stock')

    movieresult, actorsresult = database.db_getInfoMovie(film_id)
    if movieresult is None:
        return "Film not found!"

    movieresult['id'] = film_id

    return render_template("info_pelicula.html",
                           movie=movieresult, actors=actorsresult)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
Función: login
Descripción: view encargada de loggear a un usuario,
si recibe un post, checkea que el email y la contraseña
del usuario son correctas, si es así, lo redirecciona a index,
sino le advierte de que las credenciales son incorrectas
Argumentos: Void
Return: render_template
'''
    if 'email' in request.form:
        if database.db_checkUserEmail(request.form['email'],
                                      request.form['psw1']):
            load_user_session(request.form['email'])

            traslada_carrito()

            return redirect(url_for('index'))
        else:
            return render_template('login.html',
                                   title="Sign In",
                                   alerta="Credenciales Incorrectas")
    else:
        return render_template('login.html', title="Sign In")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''
Función: logout
Descripción: función para hacer logout de un usuario,
borra la coockie de sesión (usuario y carrito) y redirecciona
a index
Argumentos: Void
Return: redirect
'''
    session.pop('nombre', None)
    if 'carrito' in session:
        session.pop('carrito')

    session.modified = True
    return redirect(url_for('index'))


@app.route('/carrito', methods=['GET'])
def carrito():
    '''
Función: carrito
Descripción: view encargada de mostrar el carrito,
coge la coockie de carrito y la procesa para coger de
la base de datos la información de cada película que contiene
Argumentos: Void
Return: render_template
'''
    carritocompleto = {}
    if 'carrito' not in session:
        session['carrito'] = []
        session.modified = True
        return render_template("carrito.html", carrito=None)

    print(session['carrito'])
    if len(session['carrito']) == 0:
        carritocompleto = None
    else:
        films = session['carrito']
        for film in films:
            if carritocompleto.get(film) is None:
                carritocompleto[film] = {}
                carritocompleto[film]['info'] =\
                    database.db_getSimpleInfoMovie(int(film))
                carritocompleto[film]['quantity'] = 1
            else:
                carritocompleto[film]['quantity'] =\
                    carritocompleto[film]['quantity'] + 1

    return render_template("carrito.html", carrito=carritocompleto)


@app.route('/carrito', methods=['POST'])
def post_carrito():
    '''
Función: post_carrito
Descripción: función a la que se se llama cuando el usuario
decide modificar de alguna manera los productos de su carrito,
ya sea aumentado la cantidad de alguno de ellos, borrando alguno o
comprar el carrito. Si el usuario está loggeado, estos cambios son
guardadados en la base de datos también
Argumentos: Void
Return: redirect
'''
    if 'deletefilm' in request.form:
        peliculas = [i for i in session['carrito'] if i != str(
                                                    request.form['deletefilm']
                                                              )]
        session['carrito'] = peliculas
        session.modified = True
        if 'id' in session:
            database.db_deleteMovieCarrito(session['id'],
                                           int(request.form['deletefilm']))

    elif 'cantidad1' in request.form:
        if 'nombre' not in session:
            return redirect(url_for('login'))
        dontbuy = False
        if len(session['carrito']) == 0:
            return redirect(url_for('historial'))

        for movieid in set(session['carrito']):
            cantidad = session['carrito'].count(movieid)
            if database.db_obtainStock(int(movieid)) < cantidad:
                flash('No hay stock de ' + str(
                            database.db_getNamefromId(int(movieid))))
                dontbuy = True

        if dontbuy is True:
            return redirect(url_for('carrito'))

        database.db_buyCarrito(session['id'])

        session.pop('carrito')
        session.modified = True

        return redirect(url_for('historial'))

    return redirect(url_for('carrito'))


@app.route('/users')
def users():
    '''
Función: users
Descripción: función a la que se llama cada 3 segundos
haciendo uso de ajax y devuelve un número aleatorio entre
0 y 10000, que hace referencia la número de usuarios conectados
a la página web
Argumentos: Void
Return: str
'''
    return str(random.randint(0, 10000))


@app.route('/ajaxquantity', methods=['POST'])
def ajaxquantity():
    '''
Función: ajaxquantity
Descripción: función encargada de modificar la información del
carrito de manera asíncrona, tanto la información guardada en
la coockie de sesión como aquella guardada en la base de datos,
esta función es invocada cada vez que se modifica la cantidad
de cualquier artículo del carrito
Argumentos: Void
Return: str
'''
    if 'pelid' in request.form:
        try:
            while True:
                session['carrito'].remove(request.form['pelid'])
        except ValueError:
            pass
        print(request.form['pelid'])
        session['carrito'].extend([request.form['pelid']] *
                                  int(request.form['newquantity']))
        print(session['carrito'])
        if 'id' in session:
            database.db_updateCarrito(session['id'],
                                      int(request.form['pelid']),
                                      int(request.form['newquantity']))
        session.modified = True
        return request.form['pelid'] + 'ahora ' + request.form['newquantity']

    return 'NULL'


@app.route('/favicon.ico')
def favicon():
    '''
Función: favicon
Descripción: función que devuelve el icono de la página web
Argumentos: Void
Return: file
'''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.route('/historial', methods=['GET', 'POST'])
def historial():
    '''
Función: historial
Descripción: view encargada de mostrar el historial de un usuario,
si no hay ningún usuario loggeado lo redirecciona a login,
si lo hay obtiene el historial y el saldo del usuario registrado
desde la base de datos. Desde esta view el usuario también puede
incrementar su saldo, esto se actualizará también en la base de datos
Argumentos: Void
Return: render_template/redirect
'''
    if 'id' not in session:
        return redirect(url_for('login'))

    if 'cantidadsaldo' in request.form:
        database.db_updateSaldo(session['id'], request.form['cantidadsaldo'])
        return redirect(url_for('historial'))

    historial = database.db_getHistory(session['id'])
    for order, value in historial.items():
        print(order, value, '')
    # key el orderid
    # value tupla (orderdate, totalamount, status, [(prod_id, quantity)])
    return render_template("historial.html",
                           pedidos=historial,
                           saldo=database.db_getSaldo(session['id']))


def traslada_carrito():
    '''
Función: traslada_carrito
Descripción: función llamada cada vez que un usuario inicia sesión,
si el usuario ha generado un carrito mientras estaba sin loggear,
este carrito sobreescribe a aquel que estaba asociado a él en la
base de datos anteriromente, si no ha generado ningún carrito, entonces
el carrito de su último inicio de sesión será cargado
Argumentos: Void
Return: Void
'''
    if 'carrito' in session and len(session['carrito']) > 0:
        database.db_resetCarrito(session['id'], session['carrito'])
    else:
        session['carrito'] = database.db_loadCarrito(session['id'])
        session.modified = True


@app.route('/topusa')
def topusa():
    '''
Función: topusa
Descripción: función que devuelve la view del topUSA
Argumentos: Void
Return: render_template
'''
    return render_template("topusa.html",
                           life=database.mongodb_a(),
                           noventas=database.mongodb_b(),
                           jim_jhon=database.mongodb_c())
