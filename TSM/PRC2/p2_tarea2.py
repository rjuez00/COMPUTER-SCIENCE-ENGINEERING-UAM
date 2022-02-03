'''################################################################
# 
# @file: p2_tarea2.py
# 
# @description: Practica 2: Extraccion, descripcion y correspondencia de caracteristicas locales
#                   -Tarea 2: Descripcion de puntos de interes mediante histogramas.
#
# @author1: Fernandez Freire, Luis
# @author2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
# Librerias y paquetes por defecto
import numpy as np
import scipy.ndimage as nd
from p2_tests import test_p2_tarea2

# Nuestros imports
import matplotlib.pyplot as plt
# Ninguno
""" #####################################
    # Esta funcion describe puntos de interes de una imagen mediante histogramas, analizando 
    # vecindarios con dimensiones "vtam+1"x"vtam+1" centrados en las coordenadas de cada punto de interes
    #   
    # La descripcion obtenida depende del parametro 'tipoDesc'
    #   - Caso 'hist': histograma normalizado de valores de gris:
    #       Por cada uno de los puntos de interes:
    #           * Nos posicionamos en la esquina superior izquierda de la matriz de vecinos de dicho punto. 
    #           * Obtenemos el nbins, que sera una array cuyos valores es el rango [0, 1] dividido en nbins+1 partes.
    #           * Obtenemos la matriz vecindario.
    #           * Obtenemos el descriptor histograma.
    #           * Normalizamos el descriptor histograma.
    #           * Insertamos el histograma en la lista de descriptores.
    #
    #   - Caso 'mag-ori': histograma de orientaciones de gradiente
    #
    # En el caso de que existan puntos de interes en los bordes de la imagen, el descriptor no
    # se calcula y el punto de interes se elimina de la lista <new_coords_esquinas> que devuelve
    # esta funcion. Esta lista indica los puntos de interes para los cuales existe descriptor.
    #
    # Argumentos de entrada:
    #   - imagen: numpy array con dimensiones [imagen_height, imagen_width].        
    #   - coords_esquinas: numpy array con dimensiones [num_puntos_interes, 2] con las coordenadas 
    #                      de los puntos de interes detectados en la imagen. Tipo int64
    #                      Cada punto de interes se encuentra en el formato [fila, columna]
    #   - vtam: valor de tipo entero que indica el tamaño del vecindario a considerar para
    #           calcular el descriptor correspondiente.
    #   - nbins: valor de tipo entero que indica el numero de niveles que tiene el histograma 
    #           para calcular el descriptor correspondiente.
    #   - tipoDesc: cadena de caracteres que indica el tipo de descriptor calculado
    #
    # Argumentos de salida
    #   - descriptores: numpy array con dimensiones [num_puntos_interes, nbins] con los descriptores 
    #                   de cada punto de interes (i.e. histograma de niveles de gris)
    #   - new_coords_esquinas: numpy array con dimensiones [num_puntos_interes, 2], solamente con las coordenadas 
    #                      de los puntos de interes descritos. Tipo int64  <class 'numpy.ndarray'>
    #
    # NOTA: no modificar los valores por defecto de las variables de entrada vtam y nbins, 
    #       pues se utilizan para verificar el correcto funciomaniento de esta funcion
    #####################################"""
def descripcion_puntos_interes(imagen, coords_esquinas, vtam=8, nbins=16, tipoDesc='hist'):
    
    # Inicializamos las variables a devolver.
    new_coords_esquinas = []  
    descriptores = []
    # C.d.E
    if vtam %2 != 0:
        return

    # Convertir la imagen al formato float en el rango [0,1].
    imagen = imagen.astype("float")/255 if imagen.max() > 1 else imagen.astype("float")
    # Obtener el numero de filay y columnas de la imagen.
    nrows, ncols = imagen.shape
    # Obtener el radio de la matriz de vecinos.
    radio = int((vtam+1)/2)
    
    # Obtenemos los puntos de interes descartando los que esten en los bordes de la imagen.
    new_coords_esquinas = [(tempx, tempy) for tempx, tempy in coords_esquinas if not (tempx + radio >= nrows or tempx - radio < 0 or tempy + radio >= ncols or tempy - radio < 0)]
    
    # Caso de descriptor de historgram
    if tipoDesc == "hist":
        for tempx, tempy in new_coords_esquinas:

            tempx, tempy = (tempx - radio, tempy - radio)
            bins = np.linspace(0, 1, nbins + 1)
            vecindario = imagen[tempx:tempx+vtam+1, tempy:tempy+vtam+1]

            hist, _ = np.histogram(vecindario.flatten(), bins=bins)
            hist = hist/hist.sum()

            descriptores.append(hist)
        
    # Caso de descriptor categorico
    elif tipoDesc == "mag-ori":
        img_dx = nd.sobel(imagen, axis=0)
        img_dy = nd.sobel(imagen, axis=1)
        bins = np.linspace(0, 360, num=(nbins + 1))

        img_ori = (np.rad2deg(np.arctan2(img_dx, img_dy)) + 360) % 360
        img_mag = (img_dx**2 + img_dy**2)**(1/2)

        for tempx, tempy in new_coords_esquinas:          
            tempx, tempy = (tempx - radio, tempy - radio)
            
            vec_ori = img_ori[tempx:tempx+vtam+1, tempy:tempy+vtam+1]
            vec_mag = img_mag[tempx:tempx+vtam+1, tempy:tempy+vtam+1]

            histograma = np.zeros(shape=nbins)
            indices = np.digitize(vec_ori, bins) -1
            
            # print("\n***** Ori:\n", vec_ori)
            # print("\n***** Indices:\n", indices)
            # print("\n***** Mag:\n", vec_mag)
            for mag, indx_bin in zip(vec_mag.flatten(), indices.flatten()):
                histograma[indx_bin] += mag

            descriptores.append(histograma)
            

    return np.asarray(descriptores), np.asarray(new_coords_esquinas)


if __name__ == "__main__":    
    print("Practica 2 - Tarea 2 - Test autoevaluación\n")                

    ## tests descriptor tipo 'hist' (tarea 2a) 1: 1 seg, 2: 343 seg, 3: 1 seg, 4: 1 seg
    #print("Tests completados = " + str(test_p2_tarea2(disptime=-1,stop_at_error=False,debug=False,tipoDesc='hist'))) #analizar todas las imagenes y esquinas del test
    #print("Tests completados = " + str(test_p2_tarea2(disptime=1,stop_at_error=False,debug=False,tipoDesc='hist'))) #analizar todas las imagenes y esquinas del test, mostrar imagenes con resultados (1 segundo)
    #print("Tests completados = " + str(test_p2_tarea2(disptime=-1,stop_at_error=True,debug=True,tipoDesc='hist'))) #analizar todas las imagenes y esquinas del test, pararse en errores y mostrar datos
    #print("Tests completados = " + str(test_p2_tarea2(disptime=-1,stop_at_error=True,debug=True,tipoDesc='hist',imgIdx = 3, poiIdx = 7))) #analizar solamente imagen #2 y esquina #7

    ## tests descriptor tipo 'mag-ori' (tarea 2b)
    print("Tests completados = " + str(test_p2_tarea2(disptime=-1,stop_at_error=False,debug=False,tipoDesc='mag-ori'))) #analizar todas las imagenes y esquinas del test
    #print("Tests completados = " + str(test_p2_tarea2(disptime=0.1,stop_at_error=False,debug=False,tipoDesc='mag-ori'))) #analizar todas las imagenes y esquinas del test, mostrar imagenes con resultados (1 segundo)
    #print("Tests completados = " + str(test_p2_tarea2(disptime=-1,stop_at_error=True,debug=True,tipoDesc='mag-ori'))) #analizar todas las imagenes y esquinas del test, pararse en errores y mostrar datos
    #print("Tests completados = " + str(test_p2_tarea2(disptime=1,stop_at_error=True,debug=True,tipoDesc='mag-ori',imgIdx = 3,poiIdx = 7))) #analizar solamente imagen #1 y esquina #7

# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM