from Clasificador import Clasificador
import math
import random
import numpy as np


class ClasificadorRegresionLogistica(Clasificador):

    def __init__(self, learn_rate=1, n_epocas=1):
        self.learn_rate = learn_rate
        self.n_epocas = n_epocas
    

    def nombre(self):
        return "Regresion Logistica"


    def entrenamiento(self, datostrain, nominalAtributos, diccionario):

        self.w = np.array([random.uniform(-0.5, 0.5) for _ in range(len(nominalAtributos))])

        # Balancear el dataset de train
        a = datostrain.sort_values(by=['Class'])
        size = a.shape[0]
        for i in range(size//2):
            b, c = a.iloc[2*i], a.iloc[size-i-1]
            temp = a.iloc[2*i].copy()
            a.iloc[2*i] = c
            a.iloc[size-i-1] = temp
        datostrain = a

        for epoca in range(self.n_epocas):
            for index, point in datostrain.loc[:, datostrain.columns != "Class"].iterrows():

                x = [1]
                x.extend(point.array)
                x = np.array(x)

                sigma_j = ClasificadorRegresionLogistica.__sigmoidal(np.dot(self.w, x))

                self.w = self.w - (self.learn_rate * (sigma_j - datostrain["Class"][index])) * x

    def clasifica(self, datostest, atributosDiscretos, diccionario):

        predicciones = []
        
        for index, point in datostest.loc[:, datostest.columns != "Class"].iterrows():

            x = [1]
            x.extend(point.array)
            x = np.array(x)

            prob = ClasificadorRegresionLogistica.__sigmoidal(np.dot(self.w, x))

            predicciones.append(1 if prob >= 0.5 else 0) #TODO mayor o mayor o igual que 0.5
        
        return predicciones

    
    def confidence(self, datostest):

        scores = []
        
        for index, point in datostest.loc[:, datostest.columns != "Class"].iterrows():

            x = [1]
            x.extend(point.array)
            x = np.array(x)

            prob = ClasificadorRegresionLogistica.__sigmoidal(np.dot(self.w, x))

            scores.append(prob)
        
        return scores
    

    def __sigmoidal(x):
        if x >= 0:
            z = math.exp(-x)
            return 1 / (1 + z)
        else:
            z = math.exp(x)
            return z / (1 + z)
