#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import random
import sys
from datetime import datetime

from app import app
from flask import render_template
from flask import request, url_for, redirect
from flask import session, flash, send_from_directory


def load_user_session(username):
    session["nombre"] = username
    session.modified = True


def load_catalogue():
    catalogue_data = open(os.path.join(app.root_path,
                                       'catalogue/catalogue.json'),
                          encoding="utf-8").read()
    return json.loads(catalogue_data)


def load_categories(catalogue):
    categorias = {}
    for pelicula in catalogue['peliculas']:
        categorias.setdefault(pelicula["categoria"], [])
        categorias[pelicula["categoria"]].append(pelicula)
    return categorias


def get_film_by_id(id):
    catalogue = load_catalogue()
    for film in catalogue['peliculas']:
        if film['id'] == id:
            return film
    return None


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    catalogue = load_catalogue()
    categories = load_categories(catalogue)
    filtro = catalogue['peliculas'].copy()
    busqueda = "Buscar..."
    if 'buscar' in request.form:
        if request.form['buscar'] != "":
            filtro = []
            busqueda = request.form['buscar']
            if request.form['genero'] != "todo":
                catalogue['peliculas'] = categories[request.form['genero']]

            for peli in catalogue['peliculas']:
                if peli['titulo'].lower().find(
                                            request.form['buscar'].lower()
                                              ) != -1:
                    filtro.append(peli)

        elif request.form['genero'] != "todo":
            filtro = categories[request.form['genero']]

        if request.form['genero'] != "todo":
            originalvalue = request.form['genero']
            value = categories[request.form['genero']]
            key = request.form['genero'] + " selected"
            del categories[originalvalue]
            categories[key] = value

    return render_template('index.html',
                           movies=filtro,
                           categorias=categories,
                           novedades=catalogue[
                               'peliculas'][
                                -min(3, len(catalogue['peliculas'])):],
                           busqueda=busqueda)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'nombre' in request.form:
        if request.form['nombre'] in os.listdir(
                os.path.join(
                    app.root_path, '../usuarios/')):

            return render_template('formulario_registro.html',
                                   title="Sign In",
                                   alerta="Usuario ya creado")
        else:
            os.umask(0)
            os.mkdir(os.path.join(
                app.root_path, '../usuarios/' + request.form['nombre']),
                mode=0o777)

            request_c = request.form.copy()
            pedidos = {'pedidos': []}
            del request_c['psw2']
            request_c['psw1'] = hashlib.sha512(
                ('qwertyuiop' + request_c['psw1']).encode('utf-8')
                                               ).hexdigest()
            request_c['saldo'] = 0

            with open(os.path.join(app.root_path, '../usuarios/' +
                      request_c['nombre'] +
                      '/datos.dat'), 'w') as file:
                file.write(json.dumps(request_c))

            with open(os.path.join(app.root_path, '../usuarios/' +
                      request_c['nombre'] +
                      '/historial.json'), 'w') as file:
                file.write(json.dumps(pedidos))

            load_user_session(request.form['nombre'])
            return index()

    else:
        session['url_origen'] = request.referrer
        session.modified = True

        print(request.referrer, file=sys.stderr)
        return render_template("formulario_registro.html")


@app.route('/info_peli/<film_id>', methods=['GET', 'POST'])
def info_peli(film_id):
    catalogue_data = open(os.path.join(app.root_path,
                          'catalogue/catalogue.json'),
                          encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    if 'carrito' not in session:
        session['carrito'] = []
        session.modified = True

    if 'id' in request.form:
        session['carrito'].append(request.form['id'])
        session.modified = True

    for peli in catalogue['peliculas']:
        if peli['id'] == int(film_id):
            return render_template("info_pelicula.html", movie=peli)

    return "Film not found!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'nombre' in request.form:
        if request.form['nombre'] in os.listdir(os.path.join(
                                                app.root_path,
                                                '../usuarios/')):

            ubicacion = open(os.path.join(app.root_path,
                             '../usuarios/' +
                                          request.form['nombre'] +
                                          '/datos.dat'),
                             encoding="utf-8").read()

            datos = json.loads(ubicacion)
            loginpwd = hashlib.sha512(('qwertyuiop' +
                                       request.form['psw1']
                                       ).encode('utf-8')).hexdigest()

            if loginpwd == datos['psw1']:
                load_user_session(request.form['nombre'])
                return redirect(url_for('index'))
            else:
                return render_template('login.html',
                                       title="Sign In",
                                       alerta="Contraseña incorrecta")

        else:
            return render_template('login.html',
                                   title="Sign In",
                                   alerta="Usuario incorrecto")
    else:
        # se puede guardar la pagina desde la que se invoca
        session['url_origen'] = request.referrer
        session.modified = True
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print(request.referrer, file=sys.stderr)
        return render_template('login.html', title="Sign In")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('nombre', None)
    if 'carrito' in session:
        session.pop('carrito')

    session.modified = True
    return redirect(url_for('index'))


@app.route('/historial', methods=['GET', 'POST'])
def historial():
    if 'nombre' in session:
        user_data = open(os.path.join(app.root_path, '../usuarios/' +
                                      session['nombre'] +
                                      '/datos.dat'),
                         encoding="utf-8").read()
        usuario = json.loads(user_data)
        pedidos_data = open(os.path.join(app.root_path, '../usuarios/' +
                                         session['nombre'] +
                                         '/historial.json'),
                            encoding="utf-8").read()

        pedidos = json.loads(pedidos_data)
        for pedido in pedidos['pedidos']:
            pedido['pelicula'] = get_film_by_id(pedido['id_pelicula'])

        if 'cantidadsaldo' in request.form and request.form[
                                                'cantidadsaldo'] != "":
            usuario['saldo'] = float(usuario['saldo']) +\
                               float(request.form['cantidadsaldo'])
            with open(os.path.join(app.root_path, '../usuarios/' +
                                   usuario['nombre'] +
                                   '/datos.dat'), 'w') as file:
                file.write(json.dumps(usuario))

        return render_template("historial.html",
                               pedidos=pedidos,
                               saldo=usuario['saldo'])

    return redirect(url_for('login'))


@app.route('/carrito', methods=['GET'])
def carrito():
    carritocompleto = []
    if 'carrito' not in session:
        session['carrito'] = []
        session.modified = True
        return render_template("carrito.html", carrito=None)

    if len(session['carrito']) == 0:
        carritocompleto = None
    else:
        films = set(session['carrito'])
        for film in films:
            peliculatemp = get_film_by_id(int(film))
            peliculatemp['cuantity'] = session['carrito'].count(film)
            carritocompleto.append(peliculatemp)

    return render_template("carrito.html", carrito=carritocompleto)


@app.route('/carrito', methods=['POST'])
def post_carrito():
    if 'deletefilm' in request.form:
        peliculas = [i for i in session['carrito'] if i != str(
                                                    request.form['deletefilm']
                                                              )]
        session['carrito'] = peliculas
        session.modified = True
    elif 'cantidad1' in request.form:
        if 'nombre' not in session:
            return redirect(url_for('login'))
        peliculas = set(session['carrito'])

        cantidades = [value for key, value in request.form.items()]

        pedidos_data = open(os.path.join(app.root_path, '../usuarios/' +
                                         session['nombre'] +
                                         '/historial.json'),
                            encoding="utf-8").read()
        pedidos = json.loads(pedidos_data)
        user_data = open(os.path.join(app.root_path, '../usuarios/' +
                                      session['nombre'] +
                                      '/datos.dat'),
                         encoding="utf-8").read()
        usuario = json.loads(user_data)

        cantidadtotal = 0
        for pelicula, cantidad in zip(peliculas, cantidades):
            peliculatotal = get_film_by_id(int(pelicula))
            pedidos['pedidos'].append({
                "id_pelicula": peliculatotal['id'],
                "precio": peliculatotal['precio'],
                "unidades": int(cantidad),
                "fecha": str(datetime.now().strftime("%m/%d/%Y"))
            })
            cantidadtotal = cantidadtotal + float(
                peliculatotal['precio']) * float(cantidad)

        if cantidadtotal > usuario['saldo']:
            flash('No tienes suficiente saldo')
            return redirect(url_for('carrito'))
        usuario['saldo'] -= cantidadtotal

        with open(os.path.join(app.root_path, '../usuarios/' +
                                              session['nombre'] +
                                              '/datos.dat'), 'w') as file:
            file.write(json.dumps(usuario))
        with open(os.path.join(app.root_path, '../usuarios/' +
                                              session['nombre'] +
                                              '/historial.json'), 'w') as file:
            file.write(json.dumps(pedidos))

        session.pop('carrito')
        session.modified = True

        return redirect(url_for('historial'))

    return redirect(url_for('carrito'))


@app.route('/users')
def users():
    return str(random.randint(0, 10000))


@app.route('/ajaxquantity', methods=['POST'])
def ajaxquantity():
    if 'pelid' in request.form:
        try:
            while True:
                session['carrito'].remove(request.form['pelid'])
        except ValueError:
            pass
        session['carrito'].extend(request.form['pelid'] *
                                  int(request.form['newquantity']))
        session.modified = True
        return request.form['pelid'] + 'ahora ' + request.form['newquantity']

    return 'NULL'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')
