'''################################################################
#
# @file: tarea4.py
#
# @autor: Luis Fernandez Freire
#
# @Description:
#   1· Lea y visualice la imagen en escala de grises “brick”
#   disponible en el paquete skimage.data (consulte
#   https://scikit-image.org/docs/dev/api/skimage.data.html#skimage.data.brick).
#       Nota: Se entiende por visualizar como ver la imagen brick de la url, no
#       mostrarla cuando se ejecute el codigo.
#   2· Muestre por consola las dimensiones de la imagen y el tipo.
#   3· Aplique las siguientes operaciones a la imagen leida:
#       3·1· Filtrado de Sobel horizontal.
#       3·2· Filtrado Gaussiano con sigma=10.
#   4· Visualice la imagen original y cada resultado en ventanas distintas.
#
################################################################'''
import matplotlib.pyplot as plt
import scipy.ndimage as nd
from skimage.data import brick


#####################################
#
# Nombre: main
#
# Descripcion: llama a las funciones necesarias para verificar la
# correcta ejecucion de la tarea 4 de la P0.
#
# Retorno: Nada
#
#####################################
def main():
    # 1
    imagen = brick()
    block = False
    # 2
    print(f"Imagen:\n\t-Dimension: {imagen.shape}\n\t-Tipo: {imagen.dtype}\n")
    # 3
    imagen_sx = nd.sobel(imagen, axis=0, mode="constant")
    imagen_gaussian = nd.gaussian_filter(imagen, sigma=10)
    # 4
    pictures = [imagen, imagen_sx, imagen_gaussian]
    titles = ["Original", "Sobel Horizontal", "Gaussiano sigma 10"]
    for i, picture, title in zip(range(1, 4), pictures, titles):
        plt.figure()
        plt.imshow(picture, cmap="gray")
        plt.title(title)
        if i != 3:
            block = False
        else:
            block = True

        plt.show(block=block)

    return


if __name__ == '__main__':
    print("\n----- Inicio Test Tarea4 -----")
    main()
    print("\n----- Fin Test Tarea4 -----\n")


# END_FILE
