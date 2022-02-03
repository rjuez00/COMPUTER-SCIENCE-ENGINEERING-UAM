'''################################################################
#
# @file: tarea3.py
#
# @autor: Luis Fernandez Freire
#
# @Description:
#   1· Lea y visualice la imagen RGB “A_small_cup_of_coffe” disponible
#   en https://bit.ly/2Zjkcm7.
#   2. Muestre por consola las dimensiones, el tipo y el valor máximo
#   de la imagen.
#   3. Posteriormente cambie el tipo a float y normalice la imagen para
#   que esté en el rango [0,1]. Muestre por consola las dimensiones de
#   la imagen y el tipo.
#   4. Posteriormente transforme la imagen al espacio de color HSV.
#   5. Visualice cada canal en una sola ventana como una imagen en
#   escala de grises (e.g., una ventana con tres columnas y una fila).
#
################################################################'''
from skimage.color import rgb2hsv
from skimage.io import imread
from skimage import img_as_float32 as img_flt
import matplotlib.pyplot as plt


#####################################
#
# Nombre: main
#
# Descripcion: llama a las funciones necesarias para verificar la
# correcta ejecucion de la tarea 3 de la P0.
#
# Retorno: Nada
#
#####################################
def main():
    # 1
    imagen = imread("https://bit.ly/2Zjkcm7")
    # 2
    print(f"Imagen:\n\t-Dimension: {imagen.shape}\n\t-Tipo: {imagen.dtype}",
          f"\n\t-Valor maximo: {imagen.max()}\n")
    # 3
    imagen_float = img_flt(imagen)
    print(f"Nueva imagen:\n\t-Dimension: {imagen_float.shape}",
          f"\n\t-Tipo: {imagen_float.dtype}",
          f"\n\t-Valor maximo: {imagen_float.max()}\n")
    # 4
    imagen_rgb = rgb2hsv(imagen_float)
    # 5
    fig, axs = plt.subplots(nrows=1, ncols=3)

    for ax, i, title in zip(axs.ravel(), range(0, 3), ["1", "2", "3"]):
        ax.imshow(imagen_rgb[:, :, i], cmap="gray")
        ax.axis("off")
        ax.set_title(title)

    plt.show()

    return


if __name__ == '__main__':
    print("\n----- Inicio Test Tarea3 -----")
    main()
    print("\n----- Fin Test Tarea3 -----\n")


# END_FILE
