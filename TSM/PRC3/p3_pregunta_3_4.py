'''################################################################
#
# @file: p3_pregunta_3_4.py
#
# @description: Practica 3: Reconocimiento de escenas con modelos BOW/BOF
#                   -Memoria - Pregunta 3.4
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
from p3_pregunta_comun import load_dataset, clean_dataset, score_classify, plot_accuracies, truncate_scores, genera_webpage
from sklearn.svm import SVC
folder_resultados = "resultados"


def ejercicio_3_4_ks(kernels = ["linear", "poly", "rbf", "sigmoid"], vocab_size = 150, tamaño_hog = 100, max_iter = 10, ratio_train_test = 0.2, max_per_category = 200):
    (X_train, X_test, y_train, y_test), _ = load_dataset(max_per_category, ratio_train_test)
    print("train:")
    X_train, vocab = clean_dataset(X_train, tamaño_hog, max_iter, vocab_size = vocab_size)
    print("test:")
    X_test = clean_dataset(X_test, tamaño_hog, max_iter, vocab_size=None, vocab=vocab)
    
    scores = [score_classify(SVC(C = 1, kernel=i, gamma = "scale", degree = 3, random_state = 0), X_train, X_test, y_train, y_test) for i in kernels]   
    plot_accuracies(kernels, truncate_scores(scores, 3), title = f"SVM (C = 1, gamma = 'scale', degree = 3) (tamaño BOW: {vocab_size})", xlabel = "Kernels", ylabel = "Accuracy", base_folder = "resultados", filename = f"3_4_tam_{str(vocab_size)}.png")

#####################################
# 
# Nombre: ejercicio_3_4_webpage
#
# Descripcion: Realiza la representacio en el apartado 3.4 de la memoria.
#
#####################################
def ejercicio_3_4_webpage(kernel = "rbf", vocab_size = 39, tamaño_hog = 100, max_iter = 10, ratio_train_test = 0.2, max_per_category = 200, C = 1):
    genera_webpage(SVC(kernel = kernel, C = C, random_state = 0), vocab_size, tamaño_hog, max_iter, ratio_train_test, max_per_category, f"3_4_kernel_{kernel}_{vocab_size}_C_{C}")











if __name__ == "__main__":
    ejercicio_3_4_ks(vocab_size = 39)
    #ejercicio_3_4_webpage(kernel = "rbf", vocab_size = 39)
