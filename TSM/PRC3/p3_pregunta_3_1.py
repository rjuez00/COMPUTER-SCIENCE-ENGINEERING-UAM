'''################################################################
#
# @file: p3_pregunta_3_1.py
#
# @description: Practica 3: Reconocimiento de escenas con modelos BOW/BOF
#                   -Memoria - Pregunta 3.3
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
from p3_pregunta_comun import varia_bow
from sklearn.neighbors import KNeighborsClassifier as KNN
folder_resultados = "resultados"


#####################################
# 
# Nombre: ejercicio_3_1
#
# Descripcion: Realiza la funcionalidad exigida en el apartado 3.1 de la memoria.
#
#####################################
def ejercicio_3_1(tamano=range(50, 201, 10), n_neighbors=5, max_iter=10, ratio_train_test=0.2, max_per_category=200, tamano_hog = 100):
    tamano = [i for i in tamano]
    varia_bow(tamano, KNN(n_neighbors=5), tamano_hog, max_iter, ratio_train_test, max_per_category, folder_resultados, f"3_1_{tamano[0]}_{tamano[-1]}.png", f"KNN (N: {n_neighbors})")



if __name__ == "__main__":
    ejercicio_3_1(tamano=range(10, 201, 10))
    #ejercicio_3_1(tamano=range(168,172,1))
    #ejercicio_3_1(tamano=range(116,125,1))
    #ejercicio_3_1(tamano=range(186,195,1))