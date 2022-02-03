"""
Lea y visualice la imagen RGB “A_small_cup_of_coffe” disponible en 
https://bit.ly/2Zjkcm7
2. Muestre por consola las dimensiones, el tipo y el valor máximo de la 
imagen
3. Posteriormente cambie el tipo a float y normalice la imagen para que 
esté en el rango [0,1]. Muestre por consola las dimensiones de la 
imagen y el tipo
4. Posteriormente transforme la imagen al espacio de color HSV 
5. Visualice cada canal en una sola ventana como una imagen en escala 
de grises (e.g., una ventana con tres columnas y una fila).


- Se recomienda utilizar las funciones 
skimage.io.imread
skimage.color.rgb2hsv
matplotlib.pyplot.subplots
matplotlib.pyplot.imshow
"""


from skimage.color import rgb2hsv
from skimage.io import imread
from skimage import img_as_float
import matplotlib.pyplot as plt

img = imread ("https://bit.ly/2Zjkcm7")
print(f"Las dimensiones son {img.shape}, el tipo {img.dtype}, y el valor máximo {img.max()}")
plt.imshow(img)
plt.show(block = False)



img = img_as_float(img)
print(f"Despues de la conversión las dimensiones son {img.shape}, el tipo {img.dtype}, y el valor máximo {img.max()}")



img = rgb2hsv(img)



fig, axs = plt.subplots (1 ,3)
for ax, imgidx, colorname in zip(axs.ravel(), range(0, 3), ["Rojo", "Verde", "Azul"]):
    ax.imshow(img[:,:,imgidx], cmap ="gray"); 
    ax.set_title(colorname)

plt.show()