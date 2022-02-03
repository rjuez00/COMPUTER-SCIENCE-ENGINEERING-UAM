# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
# Practica 1: Fusion de imagenes mediante piramides
# Memoria: codigo de la pregunta 1

# AUTOR1: Fernández Freire, Luis
# AUTOR2: Juez Hernández, Rodrigo
# PAREJA/TURNO: 25/1461
'''################################################################
# Se pide:
#   1- Leer imagenes RGB y descomponer en canales
#   2- Procesar cada canal de manera independiente y realizar la fusión con piramides
#   Laplacianas.
#   3- Juntar todos los resultados de cada canal para obtener imagenes RGB resultado
#   que se mostraran por pantalla.
#
#   Nota: Se sugiere utilizar la función del paquete numpy np.stack
#
#       Para visualizar piramides, utilice las funciones vistas en la tarea 4 y
#       disponibles en el fichero p1_utils.py
#           −	visualizar_lapl_piramide(lapl_pyr)
#           −	visualizar_gaus_piramide(gauss_pyr)
#
################################################################'''
import p1_tarea4
import p1_utils
import numpy as np
import matplotlib.pyplot as plt
from skimage import color


#####################################
#
# Nombre: fun_show_laplance
#
# Descripcion: Muestra en una ventana nueva, las imagenes laplacianas.
#
# Argumentos de Entrada:
#   -window_title: string con el titulo de la ventana emergente.
#   -imagenes_laplace: lista de imagenes de la piramide laplaciana.
#
# Retorno: Nada.
#
#####################################
def fun_show_laplance(window_title, imagenes_laplace, niveles):

    # Establecemos matriz 1x4 a representar
    fig, axs = plt.subplots(1, 4)
    # Establecemos el titulo de la ventana
    fig.canvas.set_window_title(window_title + f" -  {niveles} niveles")
    # Bucle para asignar las imagenes y sus cabeceras
    for ax, imgidx, colorname in zip(axs.ravel(), range(0, 3), ["Rojo", "Verde", "Azul"]):
        ax.imshow(imagenes_laplace[imgidx], cmap="gray")
        ax.set_title(colorname)

    axs.ravel()[-1].imshow(np.stack(imagenes_laplace, axis=2))
    axs.ravel()[-1].set_title("Pirámides\n LaPlace\n Combinadas")
    fig.suptitle(window_title + f" -  {niveles} niveles")
    plt.show(block=False)

    return


#####################################
#
# Nombre: fun_show_gauss
#
# Descripcion: Muestra en una ventana nueva, las imagenes gaussianas
# sin combinar.
#
# Argumentos de Entrada:
#   -window_title: string con el titulo de la ventana emergente.
#   -imagenes_gausA: lista de imagenes de A con filtro gaussiano a combinar.
#   -imagenes_gausB: lista de imagenes de B con filtro gaussiano a combinar.
#
# Retorno: Nada.
#
#####################################
def fun_show_gauss(window_title, imagenes_gausA, imagenes_gausB, niveles):

    # Establecemos matriz 2x3 a representar
    fig, axs = plt.subplots(1, 3)
    # Establecemos el titulo de la ventana
    fig.canvas.set_window_title(window_title + " A" + f" -  {niveles} niveles")
    # Bucle para asignar las imagenes y sus cabeceras
    for imgidx, colorname in zip(range(0, 3, 1), ["Rojo", "Verde", "Azul"]):
        # primera fila
        axidx = imgidx
        axs.ravel()[axidx].imshow(imagenes_gausA[imgidx], cmap="gray")
        axs.ravel()[axidx].set_title(f"piramideA\n{colorname}")
        # segunda fila
        axidx += 3
    
    # Finalizacion del disenio de la ventana
    fig.suptitle(window_title + " A", y=0.98)
    fig.tight_layout()
    plt.show(block=False)


    fig, axs = plt.subplots(1, 3)
    # Establecemos el titulo de la ventana
    fig.canvas.set_window_title(window_title + " B")
    for imgidx, colorname in zip(range(0, 3, 1), ["Rojo", "Verde", "Azul"]):
        # primera fila
        axidx = imgidx
        axs.ravel()[axidx].imshow(imagenes_gausB[imgidx], cmap="gray")
        axs.ravel()[axidx].set_title(f"piramideB\n{colorname}")
        # segunda fila
        axidx += 3


    fig.suptitle(window_title + " B", y=0.98)
    fig.tight_layout()
    plt.show(block=False)

    return








#####################################
#
# Nombre: fun_show_gauss_comb
#
# Descripcion: Muestra en una ventana nueva, las imagenes gaussianas
# combinadas.
#
# Argumentos de Entrada:
#   -window_title: string con el titulo de la ventana emergente.
#   -imagenes_gausA: lista de imagenes de A con filtro gaussiano a combinar.
#   -imagenes_gausB: lista de imagenes de B con filtro gaussiano a combinar.
#
# Retorno: Nada.
#
#####################################
def fun_show_gauss_comb(window_title, imagenes_gausA, imagenes_gausB, niveles):

    gaus_combinado_A = []
    gaus_combinado_B = []
    for imgidx, colorname in zip(range(0, 3), ["Rojo", "Verde", "Azul"]):
        gaus_combinado_A.append(imagenes_gausA[imgidx])
        gaus_combinado_B.append(imagenes_gausB[imgidx])
    gaus_combinado_A = np.stack(gaus_combinado_A, axis=2)
    gaus_combinado_B = np.stack(gaus_combinado_B, axis=2)

    list_headers = ["piramide\ngauss A\ncombinada", "piramide\ngauss B\ncombinada"]
    # Establecemos matriz 1x2 a representar
    fig, axs = plt.subplots(1, 2)
    # Establecemos el titulo de la ventana
    fig.canvas.set_window_title(window_title + f" -  {niveles} niveles")
    # Bucle para asignar las imagenes y sus cabeceras
    for imgidx, header, picture in zip(range(0, 2), list_headers, [gaus_combinado_A, gaus_combinado_B]):
        axs.ravel()[imgidx].imshow(picture)
        axs.ravel()[imgidx].set_title(header)

    # Finalizacion del disenio de la ventana
    fig.suptitle(window_title)
    fig.tight_layout()
    plt.show(block=False)

    return


#####################################
#
# Nombre: fun_show_org_and_res
#
# Descripcion: Muestra en una ventana nueva, las imagenes originales, la
# mascara utilizada y la imagen fusionada de estas.
#
# Argumentos de Entrada:
#   -window_title: string con el titulo de la ventana emergente.
#   -list_headers: lista de string con las cabecereas de cada imagen
#                  de la ventana.
#   -list_pictures: lista que contiene las 2 imagenes originales, la
#                   mascara utilizada y la imagen resultante de la fusion.
#
# Retorno: Nada.
#
#####################################
def fun_show_org_and_res(window_title, list_headers, list_pictures, niveles):

    # Establecemos matriz 2x2 a representar
    fig, axs = plt.subplots(2, 2)
    # Establecemos el titulo de la ventana
    fig.canvas.set_window_title(window_title)
    # Bucle para asignar las imagenes y sus cabeceras
    for imgidx, header, picture in zip(range(0, 4), list_headers, list_pictures):
        if imgidx == 0 or imgidx == 1:
            axs.ravel()[imgidx].imshow(picture)
        elif imgidx == 2:
            axs.ravel()[2].imshow(picture, cmap="gray")
        else:
            axs.ravel()[3].imshow(np.stack(picture, axis=2))

        axs.ravel()[imgidx].set_title(header)

    # Finalizacion del disenio de la ventana
    fig.suptitle(f"Overview - {niveles} niveles")
    plt.show(block=False)

    return




#####################################
#
# Nombre: fun_show_gpyr_mask
#
# Descripcion: Muestra en una ventana nueva, las imagenes originales, la
# mascara utilizada y la imagen fusionada de estas.
#
# Argumentos de Entrada:
#   -window_title: string con el titulo de la ventana emergente.
#   -gpyr_mask: mascara a mostrar
#   
# Retorno: Nada.
#
#####################################
def fun_show_gpyr_mask(window_title, gpyr_mask, niveles):
    plt.figure()
    plt.imshow(gpyr_mask, cmap = "gray")
    plt.show(block = False)


    



#####################################
#
# Nombre: run_fusion_RGB
#
# Descripcion: A partir de las imagenes leidas, realiza las subdivisiones y fusiones
# necesarias para realizar lo exigido en la memoria.
#
# Argumentos de Entrada:
#   -imgRGBA: imagen 1 a color a ser fusionada.
#   -imgRGBB: imagen 2 a color a ser fusionada.
#   -mask: mascara para utilizar en la fusion entre ambas imagines.
#   -niveles: numero de tipo "int" con el numero profundidades en las piramides.
#   -show_laplace: booleano que indica si se debe mostrar los datos de laplance.
#   -show_gauss: boolenao que indica si se debe mostrar los datos gaussianos.
#
# Retorno: Nada.
#
#####################################
def run_fusion_RGB(imgRGBA, imgRGBB, mask, niveles, show_laplace=True, show_gauss=True):
    # Crear listas
    resultados_imagenes = []
    imagenes_laplace = []
    imagenes_gausA = []
    imagenes_gausB = []
    imagenes_LPA = []
    imagenes_LPB = []
    # Fusionar imagenes, 1 por cada color
    for icolor in range(0, 3):
        Gpyr_imgA, Gpyr_imgB, Gpyr_mask, Lpyr_imgA, Lpyr_imgB, laplace_piramide, img_fusionada = p1_tarea4.run_fusion(imgRGBA[:, :, icolor], imgRGBB[:, :, icolor], mask, niveles)
        # imagen resultante de la fusion gaussiana y laplaciana
        resultados_imagenes.append(img_fusionada)
        imagenes_laplace.append(p1_utils.visualizar_lapl_piramide(laplace_piramide))
        # imagenes gaussianas
        imagenes_gausA.append(p1_utils.visualizar_gaus_piramide(Gpyr_imgA))
        imagenes_gausB.append(p1_utils.visualizar_gaus_piramide(Gpyr_imgB))
        # imagenes laplacianas
        imagenes_LPA.append(p1_utils.visualizar_lapl_piramide(Lpyr_imgA))
        imagenes_LPB.append(p1_utils.visualizar_lapl_piramide(Lpyr_imgB))
        gauss_mascara = p1_utils.visualizar_gaus_piramide(Gpyr_mask)
    # Mostrar imagenes
    # Caso de piramide Laplaciana
    if show_laplace is True:
        fun_show_laplance("Piramides Laplace Fusionada", imagenes_laplace, niveles)

    # Caso de piramide Gaussiana
    if show_gauss is True:
        fun_show_gauss("Piramides LaPlace", imagenes_LPA, imagenes_LPB, niveles)
        fun_show_gauss("Piramides Gauss", imagenes_gausA, imagenes_gausB, niveles)
        fun_show_gauss_comb("Piramides Gauss Combinadas", imagenes_gausA, imagenes_gausB, niveles)

    # Material Original y resultado final.
    list_headers = ["imagen original A", "imagen original B", "máscara", "resultado_final"]
    list_pictures = [imgRGBA, imgRGBB, mask, resultados_imagenes]
    fun_show_gpyr_mask("Pirámide Gaussiana Máscara", gauss_mascara, niveles)
    fun_show_org_and_res("Material Original y Resultado Final", list_headers, list_pictures, niveles)

    return


#####################################
#
# Nombre: leer_imagenes
#
# Descripcion: Lee las imagenes y la mascara correspondiete segun la ruta
# especificada para encontrar dichos archivos.
#
# Argumentos de Entrada:
#   -titulo1: variable de tipo "string" con el nombre y la extension de la
#             primera imagen a leer.
#   -titulo2: variable de tipo "string" con el nombre y la extension de la
#             segunda imagen a leer.
#   -mask: variable de tipo "string" con el nombre y la extension de la
#             mascara a leer.
#
# Retorno:
#   - imgA: imagen leida a partir de los parametros "titulo1" y "path_imagenes".
#   - imgB: imagen leida a partir de los parametros "titulo2" y "path_imagenes".
#   - mask: imagen leida a partir de los parametros "mask" y "path_imagenes".
#
#####################################
def leer_imagenes(titulo_img1, titulo_img2, titulo_mask, path_imagenes="./img/"):
    imgA = plt.imread(f"{path_imagenes}{titulo_img1}")
    imgB = plt.imread(f"{path_imagenes}{titulo_img2}")
    mask = color.rgb2gray(plt.imread(f"{path_imagenes}{titulo_mask}"))

    return imgA, imgB, mask


if __name__ == "__main__":
    print("Practica 1 - Tarea MEMORIA - Test autoevaluacion\n")
    apple2, orange2, mask_apple2_orange2 = leer_imagenes(titulo_img1="apple2.jpg",
                                                         titulo_img2="orange2.jpg",
                                                         titulo_mask="mask_apple2_orange2.jpg")

    result = run_fusion_RGB(imgRGBA=apple2, imgRGBB=orange2, mask=mask_apple2_orange2, niveles = 8, show_laplace=False, show_gauss=True)
    plt.show(block = True)

# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
