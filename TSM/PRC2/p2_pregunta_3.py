# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
# Practica 2: Extraccion, descripcion y correspondencia de caracteristicas locales
# Memoria: codigo de la pregunta XX

# AUTOR1: Fernández Freire, Luis
# AUTOR2: Juez Hernández, Rodrigo
# PAREJA/TURNO: 25/1461

from skimage import data
from skimage import transform
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from skimage import io

from p2_tarea1 import *
from p2_tarea2 import *
from p2_tarea3 import *

def generate_graph_comparison(folder="img", imgname="NotreDame", extension="jpg", tipoDesc="hist", tipoCorr="mindist", sigma=1.0, k=0.05, threshold_rel=0.2):
    
    def run_tests(imagen1, imagen2):
        coords_esquinas1 = detectar_puntos_interes_harris(imagen1, sigma=sigma, k=k, threshold_rel=threshold_rel)  
        if len(coords_esquinas1) == 0:
            return ([], None), ([], None), None
        descriptores_imagen1, coords_esquinas1 = descripcion_puntos_interes(imagen1, coords_esquinas1, vtam=8, nbins=16, tipoDesc=tipoDesc)

        coords_esquinas2 = detectar_puntos_interes_harris(imagen2, sigma=sigma, k=k, threshold_rel=threshold_rel)
        descriptores_imagen2, coords_esquinas2 = descripcion_puntos_interes(imagen2, coords_esquinas2, vtam=8, nbins=16, tipoDesc=tipoDesc)
        

        correspondencias = correspondencias_puntos_interes(descriptores_imagen1, descriptores_imagen2, tipoCorr=tipoCorr, max_distancia=25, max_nndr=0.75)
        return (coords_esquinas1, descriptores_imagen1), (coords_esquinas2, descriptores_imagen2), correspondencias



    img1 = io.imread(f"{folder}/{imgname}1.{extension}", as_gray=True)
    img2 = io.imread(f"{folder}/{imgname}2.{extension}", as_gray=True)

    (keypoints1, _), (keypoints2, _), matches12 = run_tests(img1, img2)

    if len(keypoints1) == 0 or len(keypoints2) == 0:
        print("ERROR NO KEYPOINTS EN UNA IMAGEN")
        return

    fig, ax = plt.subplots()
    plot_matches(ax, img1, img2, keypoints1, keypoints2, matches12)
    ax.set_title(f"{imgname}1 vs. {imgname}2")
    plt.show()




# HIST
generate_graph_comparison(folder="img", imgname="NotreDame", extension="jpg", tipoDesc="hist", tipoCorr="mindist", sigma=1.0, k=0.05, threshold_rel=0.2)
generate_graph_comparison(folder="img", imgname="EGaudi_", extension="jpg", tipoDesc="hist", tipoCorr="mindist", sigma=1.0, k=0.05, threshold_rel=0.2)
generate_graph_comparison(folder="img", imgname="Mount_Rushmore", extension="jpg", tipoDesc="hist", tipoCorr="mindist", sigma=1.0, k=0.04, threshold_rel=0.2)

# MAG-ORI
generate_graph_comparison(folder="img", imgname="NotreDame", extension="jpg", tipoDesc="mag-ori", tipoCorr="mindist", sigma=1.0, k=0.05, threshold_rel=0.2)
generate_graph_comparison(folder="img", imgname="EGaudi_", extension="jpg", tipoDesc="mag-ori", tipoCorr="mindist", sigma=1.0, k=0.05, threshold_rel=0.2)
generate_graph_comparison(folder="img", imgname="Mount_Rushmore", extension="jpg", tipoDesc="mag-ori", tipoCorr="mindist", sigma=1.0, k=0.05, threshold_rel=0.2)

generate_graph_comparison(folder="img", imgname="NotreDame", extension="jpg", tipoDesc="hist", tipoCorr="nndr", sigma=1.0, k=0.05, threshold_rel=0.2)
