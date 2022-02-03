# Genere un script tarea1.py que importe el paquete numpy con el 
# nombre np y muestre la versión de este paquete.
import numpy as np
print(f"la version de numpy es {np.__version__}")

# 1. Cree un vector de tamaño 10x1 con valores aleatorios 
# y muéstrelo por pantalla. Utilice numpy.random.random
print("Ejercicio 1:\n", np.random.random ((10, 1)))
#print(np.random.random (10))

# 2. Posteriormente cree un array bidimensional de ceros 
# con tamaño 10x10. Utilice numpy.zeros
bidimensional =  np.zeros((10, 10))
print("\nEjercicio 2:\n", bidimensional)


# 3. Haga que las posiciones de los extremos del array bidimensional 
# (i.e. bordes del array) tengan el valor 1. Utilice indexación de matrices
bidimensional[0, :] = 1
bidimensional[:, 0] = 1
bidimensional[-1, :] = 1
bidimensional[:, -1] = 1

print("\nEjercicio 3: \n", bidimensional, bidimensional.shape)



#  4. Genere un nuevo array bidimensional con los elementos en posiciones con 
# índices impares (filas y columnas) del array obtenido en el punto 3. Utilice 
# numpy.array con el argumento copy=True e indexación de matrices1
print("Ejercicio 4:")


# el indice inicial es 0 y los impares son 1,3,5,7,9
# entonces para los impares hay que empezar en el 1, no ponemos final y el paso es de +2 por lo tanto inicio:final:step
impar = np.array(bidimensional[1::2, 1::2], copy=True)

print(impar, impar.shape)


# 5. Genere un nuevo array bidimensional con los elementos en posiciones con 
# índices pares (filas y columnas) del array obtenido en el punto 3. Utilice 
# numpy.array con el argumento copy=True e indexación de matrices1
print("Ejercicio 5:")


# el indice inicial es 0 y los impares son 0,2,4,6,8
# entonces para los impares hay que empezar en el 0 por lo tanto no hace falta poner inicio, no ponemos final y el paso es de +2 por lo tanto inicio:final:step
par = np.array(bidimensional[::2, ::2], copy=True)

print(par, par.shape)


# 6. Partiendo del array obtenido en 3), cambie al valor 3 la posición definida 
# por la columna tercera y fila segunda. Muestre por pantalla la segunda fila.
print("Ejercicio 6:")
bidimensional[1, 2] = 3
print(bidimensional[1, :])