'''################################################################
#
# @file: p1_tarea2.py
#
# @description: Practica 1: Fusion de imagenes mediante piramides
#                   -Tarea 2: piramide Gaussiana y piramide laplaciana
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
import sys
import numpy as np
from p1_tests import test_p1_tarea2
from p1_tarea1 import reduce, expand


#####################################
#
# Nombre: gaus_piramide
#
# Descripcion: Esta funcion crea una piramide Gaussiana a partir de una imagen.
#
#   1- Creamos una lista de imagenes (gaus_pyr) e insertamos la imagen pasada como parametro
#      de entrada.
#   2- Realizamos un bucle en funcion del numero de niveles que debe tener la pramide
#      gaussiana. En cada iteracion del bucle:
#           * Insertamos en "gaus_pyr" la ultima imagen insertada en dicha lista, pero reducida.
#
# Argumentos de Entrada:
#   -imagen: array numpy de dimension [imagen_height, imagen_width].
#   -niveles: entero positivo que especifica el numero de veces que se aplica la operacion 'reduce'.
#       * Si niveles=0 entonces se debe devolver una lista con la imagen de entrada.
#       * Si niveles=1 entonces se debe realizar una operacion de reduccion.
#
# Retorno:
#   -gauss_pyr: lista de arrays numpy con variable tamanio con "niveles+1" elementos.
#       gauss_pyr[0] es la imagen de entrada.
#       gauss_pyr[i] es el nivel i de la piramide.
#
# NOTA: algunas veces, la operacion 'expand' devuelve una imagen de tamaño mayor
# que el esperado. Entonces no coinciden las dimensiones de la imagen expandida
# del nivel k+1 y las dimensiones del nivel k.
#
# Verifique si ocurre esta situacion y en caso afirmativo, elimine los ultimos
# elementos de la imagen expandida hasta coincidir las dimensiones del nivel k.
#
# Por ejemplo, si el nivel tiene tamaño 5x7, tras aplicar 'reduce' y 'expand'
# obtendremos una imagen de tamaño 6x8. En este caso, elimine la 6 fila y 8
# columna para obtener una imagen de tamaño 5x7 donde pueda aplicar la resta.
#
#####################################
def gaus_piramide(imagen, niveles):
    # 1
    gaus_pyr = [imagen]
    # 2
    for _ in range(niveles):
        gaus_pyr.append(reduce(gaus_pyr[-1]))
    return gaus_pyr


#####################################
#
# Nombre: gaus_piramide
#
# Descripcion: Esta funcion crea una piramide Laplaciana a partir de una piramide Gaussiana.
#
# Argumentos de Entrada:
#   -gauss_pyr: lista de arrays numpy creada con la funcion 'gauss_piramide'.
#
# Retorno:
#   -lapla_pyr: lista de arrays numpy con variable tamanio con "niveles+1" elementos.
#       lapla_pyr[0] es el primera nivel de la piramide que contiene bordes.
#       lapla_pyr[i] es el nivel i de la piramide que contiene bordes.
#       lapla_pyr[niveles-1] es una imagen (escala de grises).
#
#####################################
def lapl_piramide(gaus_pyr):
    # las list comprehension estan bien porque python lee la linea entera de una sola vez y lo ejecuta múcho más rápido que si tiene que leer un bucle todo el rato
    # esto es una list comprehension, genera una lista a partir de un bucle y los resultados que saca [resultado for resultado in iterable]
    # lo que hago es calcular la longitud de las pirámides y iterar por los indices (no la lista en si)
    # con los indices voy calculando la expansion y la resta
    # a la expansion le hago indexing porque a veces da dimensiones incorrectas, entonces cojo la shape y especifico cual de las dos dimensiones quiero con el shape[0] y el shape[1] 
    return [gaus_pyr[k] - expand(gaus_pyr[k+1])[:gaus_pyr[k].shape[0], :gaus_pyr[k].shape[1]] for k in range(len(gaus_pyr)-1)] + [gaus_pyr[-1]]


#####################################
# MAIN
#####################################
if __name__ == "__main__":
    print("Practica 1 - Tarea 2 - Test autoevaluación\n")
    print(f"Tests completados = {test_p1_tarea2()}")

    sys.exit(0)

# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
