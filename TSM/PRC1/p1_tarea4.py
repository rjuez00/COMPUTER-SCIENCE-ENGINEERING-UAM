'''################################################################
#
# @file: p1_tarea4.py
#
# @description: Practica 1: Fusion de imagenes mediante piramides
#                   -Tarea 4: fusion de imagenes
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
import sys
import numpy as np
import math

from p1_tests import test_p1_tarea4
from p1_utils import visualizar_fusion
import p1_tarea1
import p1_tarea2
import p1_tarea3


#####################################
#
# Nombre: run_fusion
#
# Descripcion: Esta funcion implementa la fusion de dos imagenes calculando las
#              piramides Laplacianas de las imagenes de entrada y la piramide
#              Gausiana de una mascara.
#
# Argumentos de Entrada:
#   -imgA: array numpy de dimension [imagen_height, imagen_width].
#   -imgB: array numpy de dimension [imagen_height, imagen_width].
#   -mask: array numpy de dimension [imagen_height, imagen_width].
#
# Retorno:
#   -Gpyr_imgA: lista de arrays numpy con variable tamanio con "niveles+1" elementos
#               correspodientes a la piramide Gaussiana de la imagen A.
#   -Gpyr_imgB: lista de arrays numpy con variable tamanio con "niveles+1" elementos
#               correspodientes a la piramide Gaussiana de la imagen B.
#   -Gpyr_mask: lista de arrays numpy con variable tamanio con "niveles+1" elementos 
#               correspodientes a la piramide Gaussiana de la mascara.
#   -Lpyr_imgA: lista de arrays numpy con variable tamanio con "niveles+1" elementos 
#               correspodientes a la piramide Laplaciana de la imagen A.
#   -Lpyr_imgB: lista de arrays numpy con variable tamanio con "niveles+1" elementos 
#               correspodientes a la piramide Laplaciana de la imagen B.
#   -Lpyr_fus:  lista de arrays numpy con variable tamanio con "niveles+1" elementos 
#               correspodientes a la piramide Laplaciana de la fusion imagen A & B
#   -Lpyr_fus_rec:  array numpy de dimension [imagen_height, imagen_width] correspondiente
#                   a la reconstruccion de la pirámide Lpyr_fus
#
#####################################
def run_fusion(imgA, imgB, mask, niveles):
    # iniciamos las variables de salida    
    Gpyr_imgA = []      # Pirámide Gaussiana imagen A
    Gpyr_imgB = []      # Pirámide Gaussiana imagen B
    Gpyr_mask = []      # Pirámide Gaussiana máscara    
    Lpyr_imgA = []      # Pirámide Laplaciana imagen A
    Lpyr_imgB = []      # Pirámide Laplaciana imagen B
    Lpyr_fus = []       # Pirámide Laplaciana fusionada
    Lpyr_fus_rec = []   # Imagen reconstruida de la pirámide Laplaciana fusionada

    # 1. control de errores
    if len(imgA.shape) != 2 or len(imgB.shape) != 2:
        raise Exception("Imágenes no bidimensionales (blanco y negro)")

    # 2. 3. convertir a float y normalizar
    to_float = lambda img: img.astype("float")/255 if img.max() > 1 else img.astype("float")
    imgA = to_float(imgA)
    imgB = to_float(imgB)
    mask = to_float(mask)


    # 4. calcular las piramides gausianas
    Gpyr_imgA = p1_tarea2.gaus_piramide(imgA, niveles)
    Gpyr_imgB = p1_tarea2.gaus_piramide(imgB, niveles)
    Gpyr_mask = p1_tarea2.gaus_piramide(mask, niveles)


    # 5. calcular las piramides laplacianas   
    Lpyr_imgA = p1_tarea2.lapl_piramide(Gpyr_imgA)
    Lpyr_imgB = p1_tarea2.lapl_piramide(Gpyr_imgB)
    

    # 6. fusionar las pirámides laplacianas
    Lpyr_fus = p1_tarea3.fusionar_lapl_pyr(Lpyr_imgA, Lpyr_imgB, Gpyr_mask)

    
    # 7. Reconstruir la pirámide resultante para obtener una imagen con la función "reconstruir_lapl_pyr“
    Lpyr_fus_rec = p1_tarea3.reconstruir_lapl_pyr(Lpyr_fus)



    # 8. Tras la reconstrucción, algunos valores pueden estar fuera de rango (<0 o >1). En caso positivo, recortar a '0' o '1' según corresponda. 
    Lpyr_fus_rec[Lpyr_fus_rec > 1] = 1
    Lpyr_fus_rec[Lpyr_fus_rec < 0] = 0

    # 9. El tipo de imagen de salida debe ser float
    if Lpyr_fus_rec.dtype != float:
        raise Exception("dtype resultante no float")
        return
    
    return Gpyr_imgA, Gpyr_imgB, Gpyr_mask, Lpyr_imgA, Lpyr_imgB, Lpyr_fus, Lpyr_fus_rec


if __name__ == "__main__":    
    
    path_imagenes = "./img/"
    print("Practica 1 - Tarea 4 - Test autoevaluación\n")    
    result,imgAgray,imgBgray,maskgray,\
        Gpyr_imgA, Gpyr_imgB, Gpyr_mask, Lpyr_imgA, Lpyr_imgB, Lpyr_fus, Lpyr_fus_rec \
            = test_p1_tarea4(path_img=path_imagenes,precision=2)
    print("Tests completado = " + str(result)) 

    if result==True:
        #visualizar piramides de la fusion (puede consultar el codigo en el fichero p1_utils.py)
        visualizar_fusion(imgAgray,imgBgray,maskgray,Gpyr_imgA, Gpyr_imgB, Gpyr_mask, Lpyr_imgA, Lpyr_imgB, Lpyr_fus, Lpyr_fus_rec)
    
    sys.exit(0)

# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
