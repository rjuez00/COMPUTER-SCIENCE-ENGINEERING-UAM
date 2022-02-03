import numpy as np
import matplotlib.pyplot as plt
x = np.arange(0, 3 * np.pi, 0.1)
animals = ["cat", "dog", "monkey"]
y_sin = np.sin (x)

"""
−Establezca un punto de parada (breakpoint) en la línea 5.
−Obtenga el valor de la propiedad “dtype.name” de la variable x
> x: array([0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. , 1.1, 1.2,
       1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2. , 2.1, 2.2, 2.3, 2.4, 2.5,
       2.6, 2.7, 2.8, 2.9, 3. , 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8,
       3.9, 4. , 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5. , 5.1,
       5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6. , 6.1, 6.2, 6.3, 6.4,
       6.5, 6.6, 6.7, 6.8, 6.9, 7. , 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7,
       7.8, 7.9, 8. , 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9. ,
       9.1, 9.2, 9.3, 9.4])
       
       > special variables
       > ..
       > ..
       > dtype
            > special variables
            > ..
            > ..
            > name: 'float64'


SOLUCIÓN:
Como se  puede observar en la columna izquierda el "dtype.name" de la variable x es "float64"


−Obtenga el valor de la propiedad “len()” de la variable animals
En la columna izquierda podemos observar los siguientes datos formateados de la siguiente manera:
> animals: ['cat', 'dog', 'monkey']
    > special variables
    > function variables
      0: 'cat'
      1: 'dog'
      2: 'monkey'
      len(): 3

SOLUCIÓN:
El valor len() es 3
"""