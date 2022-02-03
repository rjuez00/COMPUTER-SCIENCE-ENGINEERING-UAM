'''################################################################
#
# @file: tarea5.py
#
# @autor: Luis Fernandez Freire
#
# @Description:
#   1· Cree una lista vacía con el nombre lista_img
#   2· Lea la imagen "astronaut" (disponible en skimage.data1) y añádala
#   a la lista lista_img. Identifique si la imagen es gris o color.
#   3· Lea la imagen "camera" (disponible en skimage.data1) y añádala a
#   la lista lista_img. Identifique si la imagen es gris o color.
#   4· Cree un array bidimensional de ceros con tamaño 10x10 y añádala a
#   la lista lista_img. Identifique si el array es gris (bidimensional)
#   o color (tridimensional).
#   5· Recorra la lista mediante un bucle utilizando la instrucción range.
#   6· Cree una nueva lista con los dos primeros elementos de la lista
#   lista_img y muestra el número de elementos de esta nueva lista.
#
################################################################'''
import numpy as np
import matplotlib.pyplot as plt
from skimage.data import astronaut, camera


#####################################
#
# Nombre: main
#
# Descripcion: llama a las funciones necesarias para verificar la
# correcta ejecucion de la tarea 5 de la P0.
#
# Retorno: Nada
#
#####################################
def main():
    img_astro = "Astronaut"
    img_cam = "Camera"
    img_mz = "Matriz de zeros"
    block = False
    # 1
    lista_img = []
    # 2
    lista_img.append(astronaut())
    print(f"Imagen de '{img_astro}':\n\t-Dimension: {lista_img[-1].shape}\n")
    esAColor(lista_img[-1].shape)
    # 3
    lista_img.append(camera())
    print(f"Imagen de '{img_cam}':\n\t-Dimension: {lista_img[-1].shape}\n")
    printInfoColor(lista_img[-1].shape)
    # 4
    lista_img.append(np.zeros((10, 10)))
    print(f"Imagen de '{img_mz}':\n\t-Dimension: {lista_img[-1].shape}\n")
    printInfoColor(lista_img[-1].shape)
    # 5
    for i in range(0, len(lista_img)):
        print(f"Imagen {i}:\n\t-Dimension: {lista_img[i].shape}",
              f"\n\t-Tipo: {lista_img[i].dtype}",
              f"\n\t-Valor maximo: {lista_img[i].max()}\n")
        plt.figure()
        
        # Mostrar imagen
        if esAColor(lista_img[i].shape) is True:
            plt.imshow(lista_img[i])
        else:
            plt.imshow(lista_img[i], cmap="gray")
        
        # Poner titulo a la imagen
        if i == 0:
            plt.title(img_astro)
        elif i == 1:
            plt.title(img_cam)
        else:
            plt.title(img_mz)
            block = True
        
        plt.show(block=block)
    
    # 6
    list_img_new = lista_img[:2]
    print(f"El numero de elementos de la lista nueva es {len(list_img_new)}")
    return


#####################################
#
# Nombre: esAColor
#
# Descripcion: Comprueba si la imagen, en funcion de su shape, es
# a color o en blanco y negro (gris).
#
# Una imagen es a color si es tridimensional, y en blanco y negro
# es bidimensional.
#
# Retorno:
#   True, si es a color.
#   False, si es en blanco y negro.
#
#####################################
def esAColor(imagen_shape):

    if len(imagen_shape) > 2 and imagen_shape[-1] == 3:
        return True
    else:
        return False


#####################################
#
# Nombre: printInfoColor
#
# Descripcion: Indica por la terminal si la imagen, en funcion
# del "shape", si es una imagen a color o en blanco y negro.
#
# Retorno: Nada.
#
#####################################
def printInfoColor(imagen_shape):

    if esAColor(imagen_shape) is True:
        print("\tEs a color (tridimensional).\n")
    else:
        print("\tEs a gris, es decir, en blanco y negro (bidimensional).\n")

    return


if __name__ == '__main__':
    print("\n----- Inicio Test Tarea5 -----")
    main()
    print("\n----- Fin Test Tarea5 -----\n")


# END_FILE
