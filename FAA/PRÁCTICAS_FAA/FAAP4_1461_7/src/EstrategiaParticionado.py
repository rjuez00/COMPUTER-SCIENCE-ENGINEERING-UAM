from abc import ABCMeta, abstractmethod
import random
import numpy as np

class Particion():

    # Esta clase mantiene la lista de indices de Train y Test para cada particion del conjunto de particiones
    def __init__(self):
        self.indicesTrain = []
        self.indicesTest = []

    def __str__(self):
        return "Train: {}\n\nTest: {}".format(self.indicesTrain, self.indicesTest)

#####################################################################################################


class EstrategiaParticionado:

    # Clase abstracta
    __metaclass__ = ABCMeta

    # Atributos: deben rellenarse adecuadamente para cada estrategia concreta. Se pasan en el constructor

    @abstractmethod
    # TODO: esta funcion deben ser implementadas en cada estrategia concreta
    def creaParticiones(self, datos, seed=None):
        pass


#####################################################################################################

class ValidacionSimple(EstrategiaParticionado):

    def __init__(self, proporcionTest, numeroEjecuciones):
        self.proporcionTest = proporcionTest
        self.numeroEjecuciones = numeroEjecuciones

    # Crea particiones segun el metodo tradicional de division de los datos segun el porcentaje deseado y el numero de ejecuciones deseado
    # Devuelve una lista de particiones (clase Particion)
    # TODO: implementar
    def creaParticiones(self, datos, seed=None):

        random.seed(seed)

        #TODO: Preguntar como hacer esto bien
        indices = datos.datos.index.tolist()
        particiones = []
        for i in range(self.numeroEjecuciones):
            randompermutation = random.shuffle(indices)
            p = Particion()
            p.indicesTest = indices[:int(self.proporcionTest*len(indices))]
            p.indicesTrain = indices[int(self.proporcionTest*len(indices)):]
            particiones.append(p)

        return particiones
        


#####################################################################################################
class ValidacionCruzada(EstrategiaParticionado):

    def __init__(self, kfolds):
        self.kfolds = kfolds

    # Crea particiones segun el metodo de validacion cruzada.
    # El conjunto de entrenamiento se crea con las nfolds-1 particiones y el de test con la particion restante
    # Esta funcion devuelve una lista de particiones (clase Particion)
    # TODO: implementar
    def creaParticiones(self, datos, seed=None):

        random.seed(seed)
        
        randompermutation = datos.datos.index.tolist()
        random.shuffle(randompermutation)

        folds = [list(fold) for fold in np.array_split(randompermutation, self.kfolds)]
        particiones = []
        for foldidx in range(len(folds)):
            p = Particion()
            p.indicesTest = folds[foldidx]
            p.indicesTrain = []

            for foldidx2 in range(len(folds)):
                if foldidx2 == foldidx:
                    continue
                p.indicesTrain += folds[foldidx2]

            particiones.append(p)

        return particiones
