'''################################################################
#
# @file: p1_tarea1.py
#
# @description: Practica 1: Fusion de imagenes mediante piramides
#                   -Tarea 1: metodos reduce y expand
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
import sys
import numpy as np
import scipy.signal as sp_sgl

from p1_tests import test_p1_tarea1
from p1_utils import generar_kernel_suavizado


#####################################
#
# Nombre: reduce
#
# Descripcion: Esta funcion implementa la operacion "reduce" sobre una imagen.
#
#   Devolvemos una convolucion de suavizado de kernel de las posiciones pares
#   de la matriz de pixeles de la imagen (es decir, las posiciones pares del
#   array bidimensional).
#
# Argumentos de Entrada:
#   -imagen: array numpy de dimension [imagen_height, imagen_width].
#
# Retorno: array numpy de dimension [imagen_height/2, imagen_width/2].
#
# NOTA: si imagen_height/2 o imagen_width/2 no son numeros enteros, redondear
#   sus resultados. Por ejemplo: entrada imagen 5x7, salida imagen 3x4.
#
#####################################
def reduce(imagen):
    # iniciamos la variable de salida (numpy array)
    return sp_sgl.convolve2d(imagen, generar_kernel_suavizado(a=0.4), "same")[::2, ::2]


#####################################
#
# Nombre: expand
#
# Descripcion: Esta funcion implementa la operacion "expand" sobre una imagen.
#
#   1- Obtenemos las dimensiones de imagen (alto y ancho).
#   2- Inicializamos la imagen expandida como un array bidimensional de 0, que es
#      2 veces mas grande que la anterior.
#   3- Rellenamos las posiciones de pares de la matriz de la imagen expandida por
#      los valores de la matriz de la imagen original.
#   4- Aplicamos la convolucion de suavizado de kernel a la imagen extendida.
#   5- Multiplicamos por 4 los valores de la matriz de la imagen extendida para
#      ajustar correctamente la media del filtrado.
#
# Argumentos de Entrada:
#   -imagen: array numpy de dimension [imagen_height, imagen_width].
#
# Retorno:
#   -imagen_expandida: array numpy de dimension [imagen_height*2, imagen_width*2].
#
#####################################
def expand(imagen):
    # 1
    imagen_height, imagen_width = imagen.shape
    # 2
    imagen_expandida = np.zeros((imagen_height*2, imagen_width*2))
    # 3
    imagen_expandida[::2, ::2] = imagen

    # 4
    imagen_expandida = sp_sgl.convolve2d(imagen_expandida, generar_kernel_suavizado(a=0.4), "same")
    # 5
    imagen_expandida *= 4

    return imagen_expandida


#####################################
# MAIN
#####################################
if __name__ == "__main__":
    print("Practica 1 - Tarea 1 - Test autoevaluación\n")
    print(f"Tests completados = {test_p1_tarea1()}")

    sys.exit(0)

# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
