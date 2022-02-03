'''################################################################
#
# @file: p3_pregunta_3_5.py
#
# @description: Practica 3: Reconocimiento de escenas con modelos BOW/BOF
#                   -Memoria - Pregunta 3.5
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
from p3_pregunta_comun import load_dataset, clean_dataset, score_classify, plot_accuracies, truncate_scores, genera_webpage
from p3_pregunta_comun import varia_bow
from sklearn.ensemble import RandomForestClassifier as RF
folder_resultados = "resultados"
# TODO tareas
"""
- parametros interesantes random forest ::::::::::::::: el mejor es el n_estimators, ya que el max_depth es mejor dejarlo que lo pille automaticamente
    n_estimators ( number of trees ) default 100
    max_depth default None (until all leaves are pure)
"""


#####################################
# 
# Nombre: ejercicio_3_5
#
# Descripcion: Realiza la funcionalidad exigida en el apartado 3.5 de la memoria.
#
#####################################
def ejercicio_3_5(n_estimators=range(200, 2001, 200), vocab_size=150, tamano_hog=100, max_iter=10, ratio_train_test=0.2, max_per_category=200):
    
    # Obtener datasets
    (X_train, X_test, y_train, y_test), _ = load_dataset(max_per_category, ratio_train_test)
    print("train:")
    X_train, vocab = clean_dataset(X_train, tamano_hog, max_iter, vocab_size = vocab_size)
    print("test:")
    X_test = clean_dataset(X_test, tamano_hog, max_iter, vocab_size=None, vocab=vocab)

    # Obtener rendimientos en funcion del numero de estimaciones y del dataset
    scores = [score_classify(RF(n_estimators=i, random_state=0), X_train, X_test, y_train, y_test) for i in n_estimators]
    # Representar los resultados obtenidos  
    plot_accuracies(n_estimators, truncate_scores(scores, 3), title=f"Random Forest (tamaño BOW: {vocab_size})", xlabel="Number Estimators", ylabel="Accuracy", base_folder="resultados", filename=f"3_5_tam_{str(vocab_size)}.png")

#####################################
# 
# Nombre: ejercicio_3_5_webpage
#
# Descripcion: Realiza la representacion del webpage en el apartado 3.5 de la memoria.
#
#####################################
def ejercicio_3_5_webpage(rf=5, vocab_size=150, tamano_hog=100, max_iter=10, ratio_train_test=0.2, max_per_category=200):
    genera_webpage(RF(n_estimators=rf, random_state=0), vocab_size, tamano_hog, max_iter, ratio_train_test, max_per_category,  f"3_5_RF_{rf}_tam_{vocab_size}")


if __name__ == "__main__":
    ejercicio_3_5(vocab_size=169) # TODO hay que poner el mejor tamaño utilizado en el 3.2
    #ejercicio_3_5_webpage(rf=1400, vocab_size=169) # TODO hay que poner el mejor rfs y el mejor tamaño utilizado en el 3.2