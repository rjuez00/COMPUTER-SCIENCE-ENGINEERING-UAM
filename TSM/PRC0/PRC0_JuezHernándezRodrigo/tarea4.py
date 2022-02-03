"""
1. Lea y visualice la imagen RGB “brick” disponible en el paquete 
skimage.data (consulte https://scikit-image.org/docs/dev/api/skimage.data.html  skimage.data.brick) 
2. Muestre por consola las dimensiones de la imagen y el tipo
3. Aplique las siguientes operaciones a la imagen leida: 
    1. Filtrado de Sobel horizontal 
    2. Filtrado Gaussiano con sigma=10. 
4. Visualice la imagen original y cada resultado en ventanas distintas
• Se recomienda utilizar las funciones 
numpy.shape
skimage.data
scipy.ndimage.sobel
scipy.ndimage.gaussian_filter
matplotlib.pyplot.imshow"""



from skimage.data import brick
import matplotlib.pyplot as plt
from scipy.ndimage import sobel, gaussian_filter



img = brick() # en la descripcion de la tarea pone que es "RGB" pero claramente viendo las dimensiones (.shape) es en blanco y negro
# y no he encontrado otro "brick()" que sea en RGB ni se puede cambiar el output con un argumento


print(f"La imagen tiene las dimensiones {img.shape} y el tipo {img.dtype}")
sx = sobel(img, axis = 0, mode = "constant") # bordes horizontal

gau = gaussian_filter(img, sigma =10)

for idx, current, currentitle in zip(range(1, 4), [img, sx, gau], ["original", "sobel horizontal", "gausiano (sigma 10)"]):
    plt.figure()
    plt.imshow(current, cmap = "gray"); #aunque en el pdf pone que es RGB no la imagen es claramente en blanco y negro
    plt.title(currentitle)
    block = False if idx != 3 else True
    plt.show(block = block)

