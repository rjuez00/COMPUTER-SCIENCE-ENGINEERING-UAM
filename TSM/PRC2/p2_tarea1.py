'''################################################################
# 
# @file: p2_tarea1.py
# 
# @description: Practica 2: Extraccion, descripcion y correspondencia de caracteristicas locales
#                   -Tarea 1: Deteccion de puntos de interes con Harris corner detector.
#
# @author1: Fernandez Freire, Luis
# @author2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
# librerias y paquetes por defecto
import numpy as np
from p2_tests import test_p2_tarea1

# Nuestros imports
from scipy.signal import convolve2d
import scipy.ndimage as nd
from skimage.feature import corner_peaks
from skimage.feature import peak_local_max

#####################################
# 
# Nombre: detectar_puntos_interes_harris
# 
# Descripcion: Esta funcion detecta puntos de interes en una imagen con el algoritmo de Harris.
#
#   1· Convertir la imagen al formato float en el rango [0,1].
#   2· Obtener las dos imagenes correspondientes a la derivada parcial horizontal y vertical
#      de la imagen dada (dimg/dx, dimg/dy).
#   3· Obtener las tres imagenes producto de derivadas parciales (dimg/dx)·(dimg/dx), 
#      (dimg/dy)·(dimg/dy), (dimg/dx)·(dimg/dy) mediante productos elemento a elemento de 
#      las imágenes correspondientes.
#   4· Aplicar filtrado Gaussiano a las tres imagenes producto anteriores.
#   5· Determinar la matriz  Mxy para cada pixel de la imagen
#   6· Calcular la funcion de respuesta R de cada píxel utilizando Mxy
#   7· Deteccion inicial de esquinas umbralizando funcion R
#   8· Deteccion final de esquinas mediante la supresion de maximos en el vecindario de cada
#      deteccion inicial
#
# Argumentos de Entrada:
#   - imagen: numpy array con dimensiones [imagen_height, imagen_width].  
#   - sigma: valor de tipo double o float que determina el factor de suavizado aplicado
#   - k: valor de tipo double o float que determina la respuesta R de Harris
#   - threshold_rel: valor de tipo double o float que define el umbral relativo aplicado sobre el valor maximo de R
# 
# Argumentos de Salida:
#   - coords_esquinas: numpy array con dimensiones [num_puntos_interes, 2] con las coordenadas 
#                      de los puntos de interes detectados en la imagen. Cada punto de interes 
#                      se encuentra en el formato [fila, columna] de tipo int64
#
# NOTA: no modificar los valores por defecto de las variables de entrada sigma y k, 
#       pues se utilizan para verificar el correcto funciomaniento de esta funcion
#####################################
def detectar_puntos_interes_harris(imagen, sigma=1.0, k=0.05, threshold_rel=0.2):
   
    # 1
    imagen = imagen.astype("float")/255 if imagen.max() > 1 else imagen.astype("float")
    # 2
    sx = nd.sobel(imagen, axis=0) # bordes horizontal
    sy = nd.sobel(imagen, axis=1) # bordes vertical

    # 3 y 4
    sx2, sxy, sy2 = [nd.gaussian_filter(img_producto, sigma=sigma, mode="constant") for img_producto in [sx*sx, sx*sy, sy*sy]]

    # 5
    det = (sx2*sy2) - (sxy**2)
    tr = sx2 + sy2
    r = det - k*(tr**2) # Obtenemos la matriz R
    # 7 y 8
    return corner_peaks(r, min_distance=5, threshold_rel=threshold_rel)


if __name__ == "__main__":    
    print("Practica 2 - Tarea 1 - Test autoevaluación\n")                
    
    print("Tests completados = " + str(test_p2_tarea1(disptime=-1,stop_at_error=False,debug=False))) #analizar todos los casos sin pararse en errores
    # print("Tests completados = " + str(test_p2_tarea1(disptime=1,stop_at_error=False,debug=False))) #analizar y visualizar todos los casos sin pararse en errores
    # print("Tests completados = " + str(test_p2_tarea1(disptime=-1,stop_at_error=True,debug=False))) #analizar todos los casos y pararse en errores 
    # print("Tests completados = " + str(test_p2_tarea1(disptime=-1,stop_at_error=True,debug=True))) #analizar todos los casos, pararse en errores y mostrar informacion

# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
