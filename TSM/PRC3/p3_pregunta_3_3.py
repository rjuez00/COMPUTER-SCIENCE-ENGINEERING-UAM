'''################################################################
#
# @file: p3_pregunta_3_3.py
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
from sklearn.svm import SVC, SVR
folder_resultados = "resultados"

def ejercicio_3_3(tamaños = range(10, 201, 10), kernel = "linear", max_iter = 10, ratio_train_test = 0.2, max_per_category = 200, tamano_hog = 100):
    tamaños = [i for i in tamaños]
    varia_bow(tamaños,  SVC(kernel = kernel, random_state = 0), tamano_hog, max_iter, ratio_train_test, max_per_category, f"resultados", f"3_3_{tamaños[0]}_{tamaños[-1]}.png", "svm.SVC (kernel = 'linear')")


# hemos hecho esta funcion para toca ajustes y ver si podemos llegar al 70%
def ejercicio_3_3_alternate(tamaños = range(30, 191, 10), kernel = "rbf", max_iter = 10, ratio_train_test = 0.2, max_per_category = 1000, tamano_hog = 100,  C = 10, gamma = "scale", degree = 3):
    tamaños = [i for i in tamaños]
    varia_bow(tamaños,  SVC(C = C, kernel = kernel, gamma = gamma, degree = degree, random_state = 0), tamano_hog, max_iter, ratio_train_test, max_per_category, f"resultados", f"best_svm_{tamaños[0]}_{kernel}_C_{C}_gamma_{gamma}_iter_{max_iter}_degree{degree}.png", f"svm.SVC (kernel = {kernel}, C = {C}, gamma = {gamma}, degree = {degree}), iter = {max_iter}")



if __name__ == "__main__":
    ejercicio_3_3(tamaños = range(10, 200, 10))
    #ejercicio_3_3(tamaños = range(39, 42, 1))
    #ejercicio_3_3(tamaños = range(175, 185, 1))
    #ejercicio_3_3_alternate(tamaños = [139, 141, 159, 161], C = 10)