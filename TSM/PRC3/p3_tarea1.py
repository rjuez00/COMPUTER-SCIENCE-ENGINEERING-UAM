'''################################################################
#
# @file: p3_tarea1.py
#
# @description: Practica 3: Reconocimiento de escenas con modelos BOW/BOF
#                   -Tarea 1: modelo BOW/BOF
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
# librerias y paquetes por defecto
from p3_tests import test_p3_tarea1
import numpy as np
from sklearn.cluster import KMeans 
from scipy.spatial.distance import cdist


#####################################
# 
# Nombre: construir_vocabulario
#
# Descripcion: Esta funcion utiliza K-Means para agrupar los descriptores en "vocab_size" clusters.
#
# Argumentos de entrada:
# - list_array_desc: Lista 1xN con los descriptores de cada imagen. Cada posicion de la lista 
#                   contiene (MxD) numpy arrays que representan UNO O VARIOS DESCRIPTORES 
#                   extraidos sobre la imagen
#                   - M es el numero de vectores de caracteristicas/features de cada imagen 
#                   - D el numero de dimensiones del vector de caracteristicas/feature.    
#   - vocab_size: int, numero de palabras para el vocabulario a construir.    
#   - max_iter: int, numero maximo de iteraciones del algoritmo KMeans
#
# Argumentos de salida:
#   - vocabulario: Numpy array de tamaño [vocab_size, D], 
#                   que contiene los centros de los clusters obtenidos por K-Means
#
#
# IMPORTANTE: PARAMETRO ITER NO TIENE SENTIDO QUE VALGA 1!!
# NOTA: se sugiere utilizar la funcion sklearn.cluster.KMeans
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html     
#####################################
def construir_vocabulario(list_img_desc, vocab_size=10, max_iter=300):
    return KMeans(n_clusters=vocab_size, max_iter=max_iter, random_state=0).fit(np.concatenate(list_img_desc)).cluster_centers_
    

#####################################
#
# Nombre: obtener_bags_of_words
# 
# Descripcion: Esta funcion obtiene el Histograma Bag of Words para cada imagen
#
# Argumentos de entrada:
# - list_img_desc: Lista 1xN con los descriptores de cada imagen. Cada posicion de la lista 
#                   contiene (MxD) numpy arrays que representan UNO O VARIOS DESCRIPTORES 
#                   extraidos sobre la imagen
#                   - M es el numero de vectores de caracteristicas/features de cada imagen 
#                   - D el numero de dimensiones del vector de caracteristicas/feature.  
#   - vocab: Numpy array de tamaño [vocab_size, D], 
#                  que contiene los centros de los clusters obtenidos por K-Means.   
#
# Argumentos de salida: 
#   - list_img_bow: Array de Numpy [N x vocab_size], donde cada posicion contiene 
#                   el histograma bag-of-words construido para cada imagen.
#
#####################################
def obtener_bags_of_words(list_img_desc, vocab):
    list_img_bow = []

    for desc in list_img_desc:
        matriz_distancias = cdist(vocab, desc)       
        hist, _ = np.histogram([np.argmin(columna) for columna in matriz_distancias.transpose()], bins=[i for i in range(len(vocab) + 1)])
        list_img_bow.append(hist/hist.sum())
        
    return np.array(list_img_bow)


if __name__ == "__main__":    
    dataset_path = './dataset/scenes15/'
    print("Practica 3 - Tarea 1 - Test autoevaluación\n")                    
    #print("Tests completados = " + str(test_p3_tarea1(dataset_path,stop_at_error=False,debug=False))) #analizar todos los casos sin pararse en errores ni mostrar datos
    print("Tests completados = " + str(test_p3_tarea1(dataset_path,stop_at_error=True,debug=True))) #analizar todos los casos, pararse en errores y mostrar datos

# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
