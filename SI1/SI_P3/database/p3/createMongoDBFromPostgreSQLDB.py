# -*- coding: utf-8 -*-

import sys
import traceback
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.pool import NullPool
import math
import pymongo


# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si2",
                          echo=False, poolclass=NullPool)
db_meta = MetaData(bind=db_engine)

movies = {}
try:
    # conexion a la base de datos
    db_conn = None
    db_conn = db_engine.connect()
    # Seleccionar las peliculas del anno 1949
    query = "SELECT imdb_movies.movieid, imdb_movies.movietitle, imdb_movies.year\
        FROM imdb_movies\
        NATURAL JOIN imdb_moviecountries\
        WHERE imdb_moviecountries.country = 'USA'\
        ORDER BY imdb_movies.year DESC, imdb_movies.movietitle\
        LIMIT 800"

    db_result = list(db_conn.execute(query).fetchall())

    if len(db_result) == 0:
        db_conn.close()
        exit()

    for movie in db_result:
        movieid = movie[0]
        movies[movieid] = {'title': movie[1], 'year': movie[2]}

        query = "  SELECT genre\
                   FROM imdb_moviegenres\
                   WHERE imdb_moviegenres.movieid = {}".format(movieid)

        db_result = [genre for genre,
                     in list(db_conn.execute(query).fetchall())]

        if len(db_result) == 0:
            print("no genres", movieid)
        movies[movieid]['genres'] = db_result

        query = "   SELECT directorname\
                    FROM imdb_directors\
                    NATURAL JOIN imdb_directormovies\
                    WHERE imdb_directormovies.movieid = {} ".format(movieid)

        db_result = [director for director,
                     in list(db_conn.execute(query).fetchall())]

        if len(db_result) == 0:
            print("no directors", movieid)
        movies[movieid]['directors'] = db_result

        query = "   SELECT imdb_actors.actorname\
                    FROM imdb_actors\
                    NATURAL JOIN imdb_actormovies\
                    WHERE imdb_actormovies.movieid = {}".format(movieid)

        db_result = [actor for actor,
                     in list(db_conn.execute(query).fetchall())]
        if len(db_result) == 0:
            print("no actors ", movieid)
        movies[movieid]['actors'] = db_result
        movies[movieid]['most_related_movies'] = []
        movies[movieid]['related_movies'] = []
    db_conn.close()

except Exception:
    if db_conn is not None:
        db_conn.close()
    print("ERROR")
    traceback.print_exc(file=sys.stderr)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# TODO memoria: las relaciones son solo con peliculas de USA
# porque en el ejemplo no se ve ninguna pelicula que no sea de ese país
for peli1, value1 in movies.items():
    for peli2, value2 in movies.items():
        if len(value1['most_related_movies']) == 10\
         and len(value1['related_movies']) == 10:
            break

        if peli2 != peli1:
            coincidencia = len(intersection(value1['genres'],
                               value2['genres']))
            if coincidencia == len(value1['genres']) \
                    and len(value1['most_related_movies']) < 10:
                value1['most_related_movies'].append({'title': value2['title'],
                                                     'year': value2['year']})

            elif (coincidencia == math.ceil(len(value1['genres']) / 2)) \
                    and (len(value1['related_movies']) < 10):
                value1['related_movies'].append({'title': value2['title'],
                                                'year': value2['year']})


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
myclient.drop_database('si1')
db = myclient['si1']
db = myclient['si1']
col = db['topUSA']

mylist = [values for key, values in movies.items()]

x = col.insert_many(mylist)

myclient.close()
