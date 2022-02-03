import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from numpy.lib.function_base import append

##################################################
# VARIABLES
##################################################

# Rendimiento, Desviacion
res_nb = [[0.565277], [0.002953]]
res_lr = [[0.678291], [0.001224]]
res_knn = [[0.9863, 0.9739, 0.9601, 0.9542, 0.9313], [0.000628, 0.000723, 0.000957, 0.000892]]
# limites redimiento y desviacion
ylim_rend = [0, 1]
ylim_desv = [0, 0.01]

##################################################
# FUNCIONES
##################################################

def plot(x_datos, y_datos, color="b", title="Rendimiento", xlabel="Clasificadores", ylabel="Precision", ylims=[0, 1]):
    
    x_points = np.array(x_datos)
    y_points = np.array(y_datos)

    fig, ax = plt.subplots(figsize=(12,6))

    ax.bar(x_points, y_points, color=color, width=0.5)
    
    ax.grid(color="gray", linestyle="--", linewidth=0.5)

    ax.set_ylim(ylims[0], ylims[1])
    #plt.set_yticks([0, 0.1, 0.2])

    # Informacion de la grafica
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.show()

    return


##################################################
# MAIN
##################################################

if __name__ == "__main__":
    titulo_grafica_rend = "Rendimiento de los Modelos usados"
    titulo_grafica_desv = "Desviacion de los Modelos usados"
    label_eje_x = "Clasificadores"
    label_eje_y_rend = "Precisión"
    label_eje_y_desv = "+/-"
    datos_eje_x = ["Naive Bayes", "K-Nearest Neighbors\nK=3", "Logistic Regression", "Neuronal Network\nC=2; N=40", "Random Forest\nN=110"]
    datos_eje_y_rend = [0.565277, 0.9863, 0.678291, 0.979955, 0.996233]
    datos_eje_y_desv = [0.002953, 0.001224, 0.000628, 0.001634, 0.000522]
    colores = ["b", "r"]
    
    #plot_rend(["Naive Bayes Gaussiano"], res_nb[0])
    # Rendimiento
    plot(datos_eje_x, datos_eje_y_rend, color=colores[0], title=titulo_grafica_rend)
    plot(datos_eje_x, datos_eje_y_desv, color=colores[1], title=titulo_grafica_desv, ylabel=label_eje_y_desv, ylims=ylim_desv)
    # Desviacion tipica