'''################################################################
#
# @file: p3_pregunta_3_2.py
#
# @description: Practica 3: Reconocimiento de escenas con modelos BOW/BOF
#                   -Memoria - Pregunta 3.2
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
from p3_pregunta_comun import load_dataset, clean_dataset, score_classify, plot_accuracies, truncate_scores, genera_webpage
from sklearn.neighbors import KNeighborsClassifier as KNN
folder_resultados = "resultados"


#####################################
# 
# Nombre: ejercicio_3_2
#
# Descripcion: Realiza la funcionalidad exigida en el apartado 3.2 de la memoria.
#
#####################################
def ejercicio_3_2_ks(knns=range(5, 22, 2), vocab_size = 150, tamano_hog=100, max_iter=10, ratio_train_test=0.2, max_per_category=200):
    (X_train, X_test, y_train, y_test), _ = load_dataset(max_per_category, ratio_train_test)
    print("train:")
    X_train, vocab = clean_dataset(X_train, tamano_hog, max_iter, vocab_size = vocab_size)
    print("test:")
    X_test = clean_dataset(X_test, tamano_hog, max_iter, vocab_size=None, vocab=vocab)




    scores = [score_classify(KNN(n_neighbors=i), X_train, X_test, y_train, y_test) for i in knns]   
    plot_accuracies(knns, truncate_scores(scores, 3), title=f"KNN (tamaño BOW: {vocab_size})", xlabel="Neighbours", ylabel="Accuracy", base_folder="resultados", filename=f"3_2_tam_{str(tamano_hog)}.png")


#####################################
# 
# Nombre: ejercicio_3_2_webpage
#
# Descripcion: Realiza la representacio en el apartado 3.2 de la memoria.
#
#####################################
def ejercicio_3_2_webpage(knn=5, vocab_size = 150, tamano_hog=100, max_iter=10, ratio_train_test=0.2, max_per_category=200):
    genera_webpage(KNN(n_neighbors=knn), vocab_size, tamano_hog, max_iter, ratio_train_test, max_per_category,  f"3_2_knn_{knn}_tam_{vocab_size}")


if __name__ == "__main__":
    ejercicio_3_2_ks(knns =  range(5, 22, 2), vocab_size=169) 
    #ejercicio_3_2_webpage(knn=15, vocab_size=169)
    #ejercicio_3_2_webpage(knn=21, vocab_size=150) # TODO hay que poner el mejor knn y el mejor tamaño


