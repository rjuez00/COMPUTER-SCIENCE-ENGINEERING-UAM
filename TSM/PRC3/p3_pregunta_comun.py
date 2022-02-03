'''################################################################
#
# @file: p3_pregunta_A.py
#
# @description: Practica 3: Reconocimiento de escenas con modelos BOW/BOF
#                   -Memoria - Pregunta A
#
# @autor1: Fernandez Freire, Luis
# @autor2: Juez Hernandez, Rodrigo
# @group: 1461
# @pair: 25
#
################################################################'''
#TODO LEERSE LOS PAPERS PARA PODER RESPONDER BIEN LAS PREGUNTAS
from p3_utils import load_image_dataset, create_results_webpage
from p3_tarea1 import *
from p3_tarea2 import *
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import time
import os


#####################################
# 
# Nombre: load_dataset
#
# Descripcion: Carga el dataset y retorna los datos de entrenamiento (X_train e y_train) y
#   los datos de test (X_test e y_test)
#
# Argumentos de entrada:
#   - max_per_category, ratio_train_test
#
# Argumentos de salida:
#   - (X_train, X_test, y_train, y_test), categories
#####################################
def load_dataset(max_per_category, ratio_train_test):
    dataset = load_image_dataset(container_path="./dataset/scenes15", max_per_category=max_per_category)
    return train_test_split(dataset["filenames"], dataset["target"], test_size=ratio_train_test, random_state=0), dataset["target_names"]


#####################################
# 
# Nombre: clean_dataset
#
# Descripcion: Primero calcula cuanto tarda en realizar las siguientes funciones:
#   - obtener_features_hog
#   - construir_vocabulario
#   - obtener_bags_of_words
#
#   Tras calcular el tiempo, devuelve el BOW
#
# Argumentos de entrada:
#   - filenames, tamano_hog, max_iter
#
# Argumentos de salida:
#   - BOW
#####################################
def clean_dataset(filenames, tamano_hog, max_iter, vocab_size=None, vocab=None):
    # Obtener puntos de interes
    start = time.time()
    fh = obtener_features_hog(filenames, tamano=tamano_hog)
    end = time.time()
    print(f"\tobtener_features_hog():\t{start-end}")
    
    
    # Calcular centroides para esos puntos de interes
    if vocab_size != None:
        # como para el test hay que usar el vocabulario calculado durante el train,
        # hemos puesto un booleano que no calcula el vocabulario asi podemos pasarle uno ya calculado durante el test
        start = time.time()
        vocab = construir_vocabulario(fh, vocab_size = vocab_size, max_iter=max_iter)
        end = time.time()
        print(f"\tconstruir_vocabulario():\t{start-end}")
    
    
    # Calcular histogramas describiendo la imagen
    start = time.time()
    X = obtener_bags_of_words(fh, vocab)
    end = time.time()
    print(f"\tobtener_bags_of_words():\t{start-end}")

    if vocab_size != None:
        return X, vocab
    else:
        return X


#####################################
# 
# Nombre: score_classify
#
# Descripcion: Calcula cuanto tarda en obtener el score del clasificador, contando tambien
#   el tiempo que le lleva realizar el entrenamiento y devuelve el score.
#
#   Tras calcular el tiempo, devuelve el BOW
#
# Argumentos de entrada:
#   - classifier, X_train, X_test, y_train, y_test
#
# Argumentos de salida:
#   - BOW
#####################################
def score_classify(classifier, X_train, X_test, y_train, y_test):
    start = time.time()
    print(classifier)
    
    score = classifier.fit(X_train, y_train).score(X_test, y_test)
    
    end = time.time()
    print(f"\tclassifier:\t{start-end}")
    return score


#####################################
# 
# Nombre: process_and_score
#
# Descripcion: Procesa los datos del entrenamiento y el test para despues aplicarlos en
#   clasificador.
# 
#   Tras los calculos devuelve el rendimiento obtendido del clasificador.
#
# Argumentos de entrada:
#   - classifier, X_train, X_test, y_train, y_test, tamano_hog, max_iter
#
# Argumentos de salida:
#   - score
#####################################
def process_and_score(classifier, vocab_size, X_train, X_test, y_train, y_test, tamano_hog, max_iter):
    X_train, vocab = clean_dataset(X_train, tamano_hog, max_iter, vocab_size = vocab_size)
    X_test = clean_dataset(X_test, tamano_hog, max_iter, vocab_size=None, vocab=vocab)
    score = score_classify(classifier, X_train, X_test, y_train, y_test)
    print(f"\t\tscore vocab_size: {vocab_size}, max_iter: {max_iter}: {score}")
    return score


#####################################
# 
# Nombre: plot_accuracies
#
# Descripcion: Genera la grafica del rendimiento.
#
# Argumentos de entrada:
#   - x, y, title, xlabel, ylabel, base_folder, filename
#
# Argumentos de salida:
#   - Ninguno
#####################################
def plot_accuracies(x, y, title, xlabel, ylabel, base_folder=None, filename=None):
    font = {'weight' : 'light',
            'size'   : 5}
    isnumber = True if type(x[0]) == int else False

    if len(x) > 2 and isnumber == True:
        width = (x[1] - x[0])/2
    else:
        width = 4
    plt.bar(x, y, width=width, tick_label=x) if isnumber else plt.bar(x, y)
    plt.ylim((0,1))

    [plt.text(i, v, " "+str(v), color='blue', ha='center', va="bottom", fontdict=font) for i, v in zip(x, y)]
    
    # Informacion de la grafica
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if filename == None:
        plt.show()
    else:
        if base_folder == None:
            plt.savefig(filename)
        else:
            if not os.path.exists(base_folder):
                os.makedirs(base_folder)
            plt.savefig(f"{base_folder}/{filename}")



def truncate_scores(scores, n_decimals):
    rule = "{0:." + str(n_decimals) + "f}"
    return [float(rule.format(i)) for i in scores]


#####################################
# 
# Nombre: varia_bow
#
# Descripcion: Genera la grafica del rendimiento en funcion del tamano del BOW.
#
# Argumentos de entrada:
#   - tamano, classifier, max_iter, ratio_train_test, max_per_category, base_folder, filename, plt_title
#
# Argumentos de salida:
#   - Ninguno
#####################################
def varia_bow(vocab_size, classifier, tamano_hog , max_iter, ratio_train_test, max_per_category, base_folder, filename, plt_title):
    print("tiempos")
    scores = [process_and_score(classifier, i, *load_dataset(max_per_category, ratio_train_test)[0], tamano_hog=tamano_hog, max_iter=max_iter) for i in vocab_size]
    print("las scores obtenidas son: ", scores)
    plot_accuracies(vocab_size, truncate_scores(scores, 3), title=plt_title, xlabel="Tamaño del BOW", ylabel="Accuracy", base_folder=base_folder, filename=filename)


#####################################
# 
# Nombre: genera_webpage
#
# Descripcion: Genera la pagina web del clasificador.
#
# Argumentos de entrada:
#   - classifier, tamano_hog, max_iter, ratio_train_test, max_per_category, filename
#
# Argumentos de salida:
#   - BOW
#####################################
def genera_webpage(classifier, vocab_size, tamano_hog, max_iter, ratio_train_test, max_per_category, filename):
    (filenames_train, filenames_test, y_train, y_test), categories = load_dataset(max_per_category, ratio_train_test)
    abbr_categories = [i[:3] for i in categories]

    X_train, vocab = clean_dataset(filenames_train, tamano_hog, max_iter, vocab_size = vocab_size)
    X_test = clean_dataset(filenames_test, tamano_hog, max_iter, vocab_size=None, vocab=vocab)
    y_predict = classifier.fit(X_train, y_train).predict(X_test)

    y_train = [categories[prediction] for prediction in y_train]
    y_test = [categories[prediction] for prediction in y_test]
    y_predict = [categories[prediction] for prediction in y_predict]

    create_results_webpage(filenames_train, filenames_test, y_train, y_test,categories, abbr_categories, y_predict, filename)


