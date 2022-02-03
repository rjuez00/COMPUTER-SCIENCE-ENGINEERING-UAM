'''################################################################
#
# @file: p1_tarea3.py
#
# @description: Practica 1: Fusion de imagenes mediante piramides
#                   -Tarea 3: fusion de piramides y reconstruccion
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
import sys
import numpy as np
from p1_tests import test_p1_tarea3
from p1_tarea1 import expand


#####################################
#
# Nombre: fusionar_lapl_pyr
#
# Descripcion: Esta funcion realiza la fusion entre dos piramides laplacianas de distintas imagenes.
# La fusion esta determinada por una mascara de la cual se utiliza su correspondiente piramide
# Gaussiana para combinar las dos piramides laplacianas.
#
# Argumentos de Entrada:
#   -lapl_pyr_imgA: lista de arrays numpy obtenida con la funcion 'lapl_piramide' sobre una imagen img2
#   -lapl_pyr_imgB: lista de arrays numpy obtenida con la funcion 'lapl_piramide' sobre otra imagen img1
#   -gaus_pyr_mask: lista de arrays numpy obtenida con la funcion 'gaus_piramide' sobre una mascara
#   para combinar ambas imagenes.
#   Esta mascara y la piramide tiene valores en el rango [0,1].
#   Para los pixeles donde gaus_pyr_mask==1, se coge la piramide de img1.
#   Para los pixeles donde gaus_pyr_mask==0, se coge la piramide de img2.
#
# Retorno:
#   -fusion_pyr: piramide fusionada, lista de arrays numpy con variable tamaño con "niveles+1" elementos.
#   fusion_pyr[i] es el nivel i de la piramide que contiene bordes.
#   fusion_pyr[niveles] es una imagen (RGB o escala de grises)
#
# NOTA: si imagen_height/2 o imagen_width/2 no son numeros enteros, redondear
#   sus resultados. Por ejemplo: entrada imagen 5x7, salida imagen 3x4.
#
#####################################
def fusionar_lapl_pyr(lapl_pyr_imgA, lapl_pyr_imgB, gaus_pyr_mask):
    # C.d.E
    if len(lapl_pyr_imgA) != len(lapl_pyr_imgB):
        return -1
    fusion_pyr = []
    for i in range(len(lapl_pyr_imgA)):
        # formula de fusión para cada nivel
        fusion_pyr.append(lapl_pyr_imgA[i]*gaus_pyr_mask[i] + lapl_pyr_imgB[i]*(1-gaus_pyr_mask[i]))

    return fusion_pyr


#####################################
#
# Nombre: reconstruir_lapl_pyr
#
# Descripcion: Esta funcion reconstruye la imagen dada una piramide laplaciana.
#
# Argumentos de Entrada:
#   -lapl_pyr: lista de arrays numpy obtenida con la funcion 'lapl_piramide'
#              sobre una imagen img.
#
# Retorno:
#   -output: array numpy con dimensiones iguales al primer nivel de la piramide
#            lapl_pyr[0].
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
def reconstruir_lapl_pyr(lapl_pyr):
    # iniciamos la variable de salida (numpy array)
    output = lapl_pyr[-1]

    for k in reversed(range(len(lapl_pyr)-1)):
        output = expand(output)[:lapl_pyr[k].shape[0], :lapl_pyr[k].shape[1]] + lapl_pyr[k]

    return output


#####################################
# MAIN
#####################################
if __name__ == "__main__":
    print("Practica 1 - Tarea 3 - Test autoevaluación\n")
    print(f"Tests completados = {test_p1_tarea3(precision=2)}")

    sys.exit(0)

# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
