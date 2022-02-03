from Clasificador import Clasificador
from collections import Counter
import random
from Datos import Datos
import numpy as np


class ClasificadorKNN(Clasificador):

    def __init__(self, k_neighbors, normalize=True):
        self.k_neighbors = k_neighbors
        self.trained = False
        self.normalize = normalize

    
    def nombre(self):
        return "KNN"


    def entrenamiento(self, datostrain, nominalAtributos, diccionario):
        self.trained = True
        self.normalized_data = datostrain


    def clasifica(self, datostest, atributosDiscretos, diccionario):
        if self.trained == False:
            raise Exception("No se ha entrenado el clasificador antes de clasificar")            
        return [self.__clasificaPunto(row) for index, row in datostest.loc[:, datostest.columns != "Class"].iterrows()]
        

    def __clasificaPunto(self, punto):
        indexing_not_class = self.normalized_data.columns != "Class"
        
        vecinos_sorted = sorted([(vecino["Class"], np.linalg.norm(punto - vecino[indexing_not_class])) for _, vecino in self.normalized_data.iterrows()], key = lambda x: x[1])
        
        vecinos_sorted = [i[0] for i in vecinos_sorted[:self.k_neighbors]]
        random.shuffle(vecinos_sorted)
        return Counter(vecinos_sorted).most_common(1)[0][0]

    
    def validacion(self, particionado, dataset, clasificador, seed=None):
        if self.normalize:
            normalized_dataframe = dataset.normalizarDatos(dataset.datos, dataset.nominalAtributos)
            normalized_datos = Datos(normalized_dataframe, loadCSV=False)
            return super().validacion(particionado, normalized_datos, clasificador, seed=seed)
        else:
            return super().validacion(particionado, dataset, clasificador, seed=seed)
