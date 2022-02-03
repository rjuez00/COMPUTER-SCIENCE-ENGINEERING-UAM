# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
# Practica 2: Extraccion, descripcion y correspondencia de caracteristicas locales
# Memoria: codigo de la pregunta XX

# AUTOR1: Fernández Freire, Luis
# AUTOR2: Juez Hernández, Rodrigo
# PAREJA/TURNO: 25/1461

from skimage.data import camera
import matplotlib.pyplot as plt
from p2_tarea1 import *
from p2_tarea2 import *
from p2_tarea3 import *
from p2_tests import test_p2_tarea2

def calc_bins(nbins):
    bins = [int(i) for i in np.linspace(0, 255, nbins + 1)]
    return [ f"[{bins[i]},{bins[i+1]})" for i in range(len(bins)) if i + 1 < len(bins)]

def generar_comparacion(coordinatestitle, histogram1, histogram2, histogram3, histogram4, title1, title2, title3, title4, bins12, bins34, rotation = 90):
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1)
    

    
    
    plt.suptitle(str(coordinatestitle))
    
    
    ax1.bar(bins12, histogram1)
    ax1.title.set_text(title1)
    plt.setp(ax1.get_xticklabels(), rotation=rotation, ha="center")


    ax2.bar(bins12, histogram2)
    ax2.title.set_text(title2)
    plt.setp(ax2.get_xticklabels(), rotation=rotation, ha="right",  rotation_mode="anchor")
    
    

    ax3.bar(bins34, histogram3)
    ax3.title.set_text(title3)
    plt.setp(ax3.get_xticklabels(), rotation=rotation, ha="right",  rotation_mode="anchor")


    ax4.bar(bins34, histogram4)
    ax4.title.set_text(title4)
    plt.setp(ax4.get_xticklabels(), rotation=rotation, ha="right",  rotation_mode="anchor")
    
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.7)

    fig.show()
    #plt.savefig(f"hist_{coordinatestitle}.jpg")

def show_comparison_for_indices(lista_indices):
    imagen = camera()
    coords_esquinas = detectar_puntos_interes_harris(imagen, sigma=1.0, k=0.05, threshold_rel=0.2)
    histograms1632, coordinates = descripcion_puntos_interes(imagen, coords_esquinas, vtam=16, nbins=32, tipoDesc='hist')
    histograms832, coordinates2 = descripcion_puntos_interes(imagen, coords_esquinas, vtam=8, nbins=32, tipoDesc='hist')

    if len(coordinates) != len(coordinates2):
        print("NO PUEDO CONTINUAR LOS INDICES SON DISTINTOS")

    histograms1616, coordinates = descripcion_puntos_interes(imagen, coords_esquinas, vtam=16, nbins=16, tipoDesc='hist')
    histograms816, coordinates2 = descripcion_puntos_interes(imagen, coords_esquinas, vtam=8, nbins=16, tipoDesc='hist')

    for i in lista_indices:
        generar_comparacion(coordinates[i], histograms1632[i], histograms832[i], histograms1616[i], histograms816[i], "nbins = 32, vtam = 16", "nbins = 32, vtam = 8", "nbins = 16, vtam = 16", "nbins = 16, vtam = 8", calc_bins(32), calc_bins(16))
    input()









show_comparison_for_indices([0,10,15,40])
