# -*- coding: utf-8 -*-

# coding: utf-8
import pandas as pd
import numpy as np

class Datos:

    # Constructor: procesar el fichero para asignar correctamente las variables nominalAtributos, datos y diccionarios
    def __init__(self, dataset, loadCSV=True, todosNominales=False):

        if loadCSV:
            # cargamos con pandas directamente, no hace falta especificar nada porque tiene el formato de primera linea son titulos
            self.datos = pd.read_csv(dataset, dtype = {"Class": "object"})
        else:
            self.datos = dataset.copy()

        if todosNominales == False:
            # Con esta list comprehension comprobamos los tipos de los datos y rellenamos un array con Trues y Falses (None si no es string, int o float)
            self.nominalAtributos = [True if (type(i) == str) else False if (np.issubdtype(type(i), np.float)) or (np.issubdtype(type(i), np.integer)) else None for i in self.datos.iloc[0, :]]
            if None in self.nominalAtributos:
                raise ValueError
        else:
            self.nominalAtributos = [True for i in self.datos.iloc[0, :]]

        # iVamos columna por columna añadiendo al diccionario principal otro diccionario con el lookup table
        self.diccionario = {}
        for idx, nombreatributo in enumerate(self.datos.keys()):

            # Si el atributo no es nominal, introducimos un diccionario vacio para ese atributo
            if self.nominalAtributos[idx] == False:
                self.diccionario[nombreatributo] = {}
                continue
            
            # la pd.Series la convertimos en un set y luego en una lista para poder indexarla 
            valores = list(set(self.datos[nombreatributo]))
            valores.sort()
            # usamos el indice como el indice
            self.diccionario[nombreatributo] = {valores[i] : i for i in range(len(valores))}

        for isnominal, i in zip(self.nominalAtributos, self.datos):
            if isnominal == True:
                self.datos[i] = [self.diccionario[i][valor] for valor in self.datos[i]]
    
    @staticmethod
    def calcularMediasDesv(datos, nominalAtributos):
        return {columna : {"mean": datos[columna].mean(), "std": datos[columna].std()} for esnominal, columna in zip(nominalAtributos, datos) if esnominal == False}

    @staticmethod
    def normalizarDatos(datos, nominalAtributos):
        
        medias_desvs = Datos.calcularMediasDesv(datos, nominalAtributos)
        normalized_data = datos.copy()

        for nombre_columna in normalized_data.columns.values.tolist():
            if nombre_columna != "Class":
                normalized_data[nombre_columna] = (normalized_data[nombre_columna] - medias_desvs[nombre_columna]["mean"]) / medias_desvs[nombre_columna]["std"]
        
        return normalized_data


    # Devuelve el subconjunto de los datos cuyos indices se pasan como argumento
    def extraeDatos(self,idx):
        return self.datos.loc[idx]




    