"""
1. Cree una lista vacía con el nombre lista_img
2. Lea la imagen astronaut (disponible en skimage.data1) y añádala a la lista 
lista_img. Identifique si la imagen es gris o color.
3. Lea la imagen camera (disponible en skimage.data1) y añádala a la lista 
lista_img. Identifique si la imagen es gris o color.
4. Cree un array bidimensional de ceros con tamaño 10x10 y añádala a la lista 
lista_img. Identifique si el array es gris (bidimensional) o color (tridimensional)
5. Recorra la lista mediante un bucle utilizando la instrucción range
    1. Muestre por consola las dimensiones de la imagen, tipo y valor máximo
    2. Visualice la imagen en una ventana
6. Cree una nueva lista con los dos primeros elementos de la lista lista_img y 
muestra el número de elementos de esta nueva lista
• Se recomienda utilizar las funciones 
numpy.shape
numpy.range
numpy.append
skimage.data
matplotlib.pyplot.imshow
"""

from skimage.data import astronaut, camera
import numpy as np
import matplotlib.pyplot as plt
lista_img = [] # aunque pone que use numpy.append dice lista y no vector asi que asunmo que dice una lista normal de python



lista_img.append(astronaut())
print(f"La imagen del astronauta {lista_img[-1].shape} es a color, porque se puede observar que está compuesto por por 3 matrices bidimiensionales")

lista_img.append(camera())
print(f"La imagen de la camara {lista_img[-1].shape} es en blanco y negro, se puede ver porque es una única matriz bidimensional")

lista_img.append(np.zeros((10,10)))
print(f"La imagen de ceros {lista_img[-1].shape} es en blanco y negro, se puede ver porque es una única matriz bidimensional")

print("#\tdimension\ttipo\t\tmax")
for idx in range(0, len(lista_img)):
    print(f"{idx}\t{lista_img[idx].shape}\t{lista_img[idx].dtype}\t\t{lista_img[idx].max()}")
    plt.figure()
    plt.imshow(lista_img[idx]) if idx == 0 else plt.imshow(lista_img[idx], cmap = "gray") # esto lo hago porque las dos ultimas imagenes son en blanco y negro
    plt.title(str(idx))
    plt.show(block = False)


newlist = lista_img[:2]
print(f"El numero de elementos de la nueva lista es {len(newlist)}")

input("presiona cualquier enter para terminar")



