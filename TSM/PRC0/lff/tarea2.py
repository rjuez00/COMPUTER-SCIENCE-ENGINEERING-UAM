'''################################################################
#
# @file: tarea2.py
#
# @autor: Luis Fernandez Freire
#
#   @Description:
#   -Establezca un punto de parada (breakpoint) en la linea 5 (en
#   este caso la linea 27).
#
#   -Obtenga el valor de la propiedad “dtype.name” de la variable "x".
#
#   -Obtenga el valor de la propiedad “len()” de la variable "animals".
#
#   -Incluir los valores observados de las variables como comentarios.
#
#       * Valor de la propiedad “dtype.name” de la variable "x": float64
#       * Valor de la propiedad “len()” de la variable "animals": 3
#
################################################################'''
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 3 * np.pi, 0.1)
animals = ['cat ', 'dog ', 'monkey']

y_sin = np.sin(x)

# END_FILE
