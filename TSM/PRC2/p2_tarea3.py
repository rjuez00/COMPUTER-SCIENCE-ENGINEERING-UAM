'''################################################################
# 
# @file: p2_tarea3.py
# 
# @description: Practica 2: Extraccion, descripcion y correspondencia de caracteristicas locales
#                   -Tarea 3: Similitud y correspondencia de puntos de interes.
#
# @author1: Fernandez Freire, Luis
# @author2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
# Librerias y paquetes por defecto
import numpy as np
from p2_tests import test_p2_tarea3

# Nuestros imports
# Ninguno

""" #####################################
    # Esta funcion determina la correspondencias entre dos conjuntos de descriptores mediante
    # el calculo de la similitud entre los descriptores.
    #
    # El parametro 'tipoCorr' determina el criterio de similitud aplicado 
    # para establecer correspondencias entre pares de descriptores:
    #   - Criterio 'mindist': minima distancia euclidea entre descriptores 
    #                         menor que el umbral 'max_distancia'
    #   - Criterio 'nndr': minima distancia euclidea entre descriptores 
    #                      menor que el umbral 'max_distancia'
    #                      y con ratio nndr menor que el umbral 'nndr'. La segunda distancia mínima no debe              
    #  
    # Argumentos de entrada:
    #   - descriptores1: numpy array con dimensiones [numero_descriptores, longitud_descriptor] 
    #                    con los descriptores de los puntos de interes de la imagen 1.        
    #   - descriptores2: numpy array con dimensiones [numero_descriptores, longitud_descriptor] 
    #                    con los descriptores de los puntos de interes de la imagen 2.        
    #   - tipoCorr: cadena de caracteres que indica el tipo de criterio para establecer correspondencias
    #   - max_distancia: valor de tipo double o float utilizado por el criterio 'mindist' y 'nndr', 
    #                    que determina si se aceptan correspondencias entre descriptores 
    #                    con distancia minima menor que 'max_distancia' 
    #   - max_nndr: valor de tipo double o float utilizado por el criterio 'nndr', que determina 
    #                    si se aceptan correspondencias entre descriptores con ratio nndr menor que 'max_nndr' 
    #
    # Argumentos de salida
    #   - correspondencias: numpy array con dimensiones [numero_correspondencias, 2] de tipo int64 
    #                       que determina correspondencias entre descriptores de imagen 1 e imagen 2.
    #                       Por ejemplo: 
    #                       correspondencias[0,:]=[5,22] significa que el descriptor 5 de la imagen 1 
    #                                                  corresponde con el descriptor 22 de la imagen 2. 
    #                       correspondencias[1,:]=[6,23] significa que el descriptor 6 de la imagen 1 
    #                                                  corresponde con el descriptor 23 de la imagen 2.
    #
    # NOTA: no modificar los valores por defecto de las variables de entrada tipoCorr y max_distancia, 
    #       pues se utilizan para verificar el correcto funciomaniento de esta funcion
    #
    # CONSIDERACIONES: 
    # 1) La funcion no debe permitir correspondencias de uno a varios descriptores. Es decir, 
    #   un descriptor de la imagen 1 no puede asignarse a multiples descriptores de la imagen 2 
    # 2) En el caso de que existan varios descriptores de la imagen 2 con la misma distancia minima 
    #    con algún descriptor de la imagen 1, seleccione el descriptor de la imagen 2 con 
    #    indice/posicion menor. Por ejemplo, si las correspondencias [5,22] y [5,23] tienen la misma
    #    distancia minima, seleccione [5,22] al ser el indice 22 menor que 23
    #####################################"""
def correspondencias_puntos_interes(descriptores_imagen1, descriptores_imagen2, tipoCorr='mindist',max_distancia=25, max_nndr=0.75):
    
    descriptores_imagen2 = [(idx, descriptor) for idx, descriptor in enumerate(descriptores_imagen2)]

    correspondencias = []
    if "mindist" == tipoCorr or "minDist" == tipoCorr:
        for idx1, descriptor1 in enumerate(descriptores_imagen1):
            distancias2 = [(idx, np.linalg.norm(descriptor2-descriptor1)) for idx, descriptor2 in descriptores_imagen2 if idx != -1]
            distancias2 = sorted(
                                    [(idx2, distancia2) for idx2, distancia2 in distancias2 if distancia2<max_distancia],
                                    key = lambda x: x[1]
                                )
            if len(distancias2) != 0:
                distancia_minima = distancias2[0][0]
                correspondencias.append((idx1, distancia_minima)) 
                descriptores_imagen2[distancia_minima] = (-1, None)
            



    elif tipoCorr == "nndr":
        for idx1, descriptor1 in enumerate(descriptores_imagen1):
            distancias2 = [(idx, np.linalg.norm(descriptor2-descriptor1)) for idx, descriptor2 in descriptores_imagen2 if idx != -1]
            distancias2 = sorted(
                                    [(idx2, distancia2) for idx2, distancia2 in distancias2 if distancia2<max_distancia],
                                    key = lambda x: x[1]
                                )
            if len(distancias2) != 0:
                if len(distancias2) == 1:
                    distancia_minima = distancias2[0][0]
                    correspondencias.append((idx1, distancia_minima)) 
                    descriptores_imagen2[distancia_minima] = (-1, None)
                else:
                    distancia1, distancia2 = distancias2[:2]
                    if distancia1[1]/distancia2[1] < max_nndr:
                        distancia_minima = distancia1[0]
                        correspondencias.append((idx1, distancia_minima)) 
                        descriptores_imagen2[distancia_minima] = (-1, None)






    return np.array(correspondencias, dtype = "int64")

if __name__ == "__main__":
    print("Practica 2 - Tarea 3 - Test autoevaluación\n")                

    ## tests correspondencias tipo 'minDist' (tarea 3a)
    print("Tests completados = " + str(test_p2_tarea3(disptime=-1,stop_at_error=True,debug=True,tipoDesc='hist',tipoCorr='minDist'))) #analizar todas las imagenes con descriptor 'hist' y ver errores
    #print("Tests completados = " + str(test_p2_tarea3(disptime=-1,stop_at_error=False,debug=False,tipoDesc='hist',tipoCorr='minDist'))) #analizar todas las imagenes con descriptor 'hist'
    #print("Tests completados = " + str(test_p2_tarea3(disptime=1,stop_at_error=False,debug=False,tipoDesc='mag-ori',tipoCorr='minDist'))) #analizar todas las imagenes con descriptor 'mag-ori'