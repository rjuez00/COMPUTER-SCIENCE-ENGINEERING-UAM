from abc import ABCMeta, abstractmethod
from Clasificador import Clasificador
from typing_extensions import final
import pandas as pd
import numpy as np
import scipy.stats


class ClasificadorNaiveBayes(Clasificador):

    def __init__(self, aplicar_laplace):
        self.tablas_nominales = {} 
        self.tablas_continuas = {}
        self.probs_hipotesis = {}
        self.class_possible_values = None
        
        self.aplicar_laplace = aplicar_laplace

    
    def nombre(self):
        return "Naive Bayes"

    def entrenamiento(self, datostrain, nominalAtributos, diccionario):
        if nominalAtributos[-1] == True:
            self.class_possible_values = [possible_value for _, possible_value in diccionario["Class"].items()]
        else:
            self.class_possible_values = set(datostrain["Class"])
            pass

        i = 0
        for atributo in datostrain:
            if atributo == "Class":
                continue
            if nominalAtributos[i] == True:   
                self.__generar_nominal(atributo, datostrain, diccionario)
            else:
                self.__generar_continua(atributo, datostrain, diccionario)
            i += 1

        for hipotesis in self.class_possible_values:
            self.probs_hipotesis[hipotesis] = len(datostrain["Class"][datostrain["Class"] == hipotesis]) / len(datostrain["Class"])

    def __generar_nominal(self, atributo, datostrain, diccionario):
        tempdict = {}
        for class_posible_value in self.class_possible_values:
            tempdict[class_posible_value] = {}
            for _, value in diccionario[atributo].items():
                tempdict[class_posible_value][value] = len([i for i in datostrain["Class"][datostrain[atributo] == value] == class_posible_value if i == True])

        tmp = pd.DataFrame(tempdict)
        if self.aplicar_laplace == True:
            tmp[:] += 1
        self.tablas_nominales[atributo] = tmp

    def __generar_continua(self, atributo, datostrain, diccionario):
        # esta mal, hay que hacer la std y mean para cada hipotesis, no para una general
        tempdict = {}
        for class_possible_value in self.class_possible_values:
            target = datostrain["Class"] == class_possible_value
            tempdict[class_possible_value] = {"std":datostrain[atributo][target].std(), "mean":datostrain[atributo][target].mean()}
        
        self.tablas_continuas[atributo] = pd.DataFrame(tempdict)

    def clasifica(self, datostest, atributosDiscretos, diccionario):
        predicciones = []

        for index, row in datostest.iterrows():
            # print("Row {}:".format(index))
            # por cada row hay que hacer una prediccion
            probabilidad_hipotesis = {}
            for hipotesis in self.class_possible_values:
                tempmultiplicacion = self.probs_hipotesis[hipotesis]
                for idx, (nombreatributo, dato_de_atributo) in enumerate(row.items()):
                    if nombreatributo == "Class":
                        continue
                
                    if atributosDiscretos[idx] == True:
                        # print("\tCalculando P({}|{})".format(dato_de_atributo, hipotesis))
                        tempmultiplicacion *= self.__calcular_probabilidad_nominal(self.tablas_nominales[nombreatributo], dato_de_atributo, hipotesis)
                
                    else:
                        tempmultiplicacion *= self.__calcular_probabilidad_continua(self.tablas_continuas[nombreatributo], dato_de_atributo, hipotesis)
                
                probabilidad_hipotesis[hipotesis] = tempmultiplicacion


            maxhipo, maxprob = list(probabilidad_hipotesis.items())[0]
            for hipotesis, probabilidad in probabilidad_hipotesis.items():
                if probabilidad > maxprob:
                    maxprob = probabilidad
                    maxhipo = hipotesis

            predicciones.append(maxhipo)
        
        return predicciones
        # P(A|H)*P(B|H)* ... * P(H)

    def __calcular_probabilidad_nominal(self, tabla, dato, hipotesis):
        """
        tablaatributo
                hipo hipo2
        valor1    2
        valor2    3
        """
        return tabla.loc[dato, hipotesis] / tabla[hipotesis].sum()

    def __calcular_probabilidad_continua(self, tabla, dato, hipotesis):
 
        return scipy.stats.norm.pdf(dato, loc = tabla[hipotesis]["mean"], scale = tabla[hipotesis]["std"])