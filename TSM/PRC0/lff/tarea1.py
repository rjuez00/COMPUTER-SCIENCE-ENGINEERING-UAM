'''################################################################
#
# @file: tarea1.py
#
# @autor: Luis Fernandez Freire
#
################################################################'''
import numpy as np


#####################################
#
# Nombre: main
#
# Descripcion: llama a las funciones necesarias para verificar la
# correcta ejecucion de la tarea 1 de la P0.
#
# Retorno: Nada
#
#####################################
def main():
    function_0()
    function_1()
    array_zeros = function_2()
    print("2· Matriz 10x10 de zeros:\n", array_zeros, "\n")
    function_3(array_zeros)
    function_4(array_zeros)
    function_5(array_zeros)
    function_6(array_zeros)
    return


#####################################
#
# Nombre: function_0
#
# Descripcion: muestra la version del paquete "numpy" con el nombre "np".
#
# Retorno: Nada
#
#####################################
def function_0():
    print("0· Numpy version as 'np': ", np.version.version)
    return


#####################################
#
# Nombre: function_1
#
# Descripcion: Crea un vector de tamaño 10x1 con valores aleatorios y
# lo muéstra por pantalla.
#
# Retorno: Nada
#
#####################################
def function_1():
    vector_random = np.random.random((10, 1))
    print("1· Vector de 10 filas y 1 columna con valores aleatorios:\n",
          vector_random, "\n")
    return


#####################################
#
# Nombre: function_2
#
# Descripcion: Crea un array bidimensional de zeros con tamanio 10x10 y
# lo devuelve.
#
# Retorno: array bidemensional de zeros con tamianio 10x10.
#
#####################################
def function_2():
    return np.zeros((10, 10))


#####################################
#
# Nombre: function_3
#
# Descripcion: Cambia el valor de los extremos de una array bidimensional
# de tamanio 10x10 lleno de 0 (i.e. bordes del array) por 1 utilizando
# indexacion de matrices y muestra el cambio por pantalla.
#
# Retorno: Nada.
#
#####################################
def function_3(array_zeros):
    x = 1
    array_zeros[0, :] = x
    array_zeros[:, 0] = x
    array_zeros[-1, :] = x
    array_zeros[:, -1] = x

    print("3· Array de 10 filas y 10 columnas con todo zeros excepto en ",
          "los extremos cuyo valor es 1:\n", array_zeros, "\n")
    return


#####################################
#
# Nombre: function_4
#
# Descripcion: Genere un nuevo array bidimensional con los elementos en
# posiciones con índices impares (filas y columnas) del array modificado
# en el metodo "function_3" utilizando indexacion de matrices.
#
# Retorno: Nada.
#
#####################################
def function_4(array_fun3):
    array_impares = np.array(array_fun3[1::2, 1::2], copy=True)
    print("4· Matriz de impares:\nDimension: ", array_impares.shape, "\n",
          array_impares, "\n")
    return


#####################################
#
# Nombre: function_5
#
# Descripcion: Genere un nuevo array bidimensional con los elementos en
# posiciones con índices pares (filas y columnas) del array modificado
# en el metodo "function_3" utilizando indexacion de matrices.
#
# Retorno: Nada.
#
#####################################
def function_5(array_fun3):
    array_pares = np.array(array_fun3[::2, ::2], copy=True)
    print("5· Matriz de pares:\nDimension: ", array_pares.shape, "\n",
          array_pares, "\n")
    return


#####################################
#
# Nombre: function_6
#
# Descripcion: Modifica el array obtenido despues de la ejecucion del
# metodo "function_3", cambiando por un 3 el valor definido en la segunda
# fila y tercera columna. Finalmente muestra la segundo fila del array
# modificado.
#
# Retorno: Nada.
#
#####################################
def function_6(array_fun3):
    array_fun3[1, 2] = 3
    print("6· Fila modificada del apartado 3:\n", array_fun3[1, :])
    return


if __name__ == '__main__':
    print("\n----- Inicio Test Tarea1 -----")
    main()
    print("\n----- Fin Test Tarea1 -----\n")

# END_FILE
