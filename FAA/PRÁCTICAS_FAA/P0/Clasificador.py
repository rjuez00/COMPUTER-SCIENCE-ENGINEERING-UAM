from abc import ABCMeta, abstractmethod


class Clasificador:

    # Clase abstracta
    __metaclass__ = ABCMeta

    # Metodos abstractos que se implementan en casa clasificador concreto
    @abstractmethod
    # TODO: esta funcion debe ser implementada en cada clasificador concreto. Crea el modelo a partir de los datos de entrenamiento
    # datosTrain: matriz numpy con los datos de entrenamiento
    # nominalAtributos: array bool con la indicatriz de los atributos nominales
    # diccionario: array de diccionarios de la estructura Datos utilizados para la codificacion de variables discretas
    def entrenamiento(self, datosTrain, nominalAtributos, diccionario):
        pass

    @abstractmethod
    # TODO: esta funcion debe ser implementada en cada clasificador concreto. Devuelve un numpy array con las predicciones
    # datosTest: matriz numpy con los datos de validaci�n
    # nominalAtributos: array bool con la indicatriz de los atributos nominales
    # diccionario: array de diccionarios de la estructura Datos utilizados para la codificacion de variables discretas
    def clasifica(self, datosTest, nominalAtributos, diccionario):
        pass

    # Obtiene el numero de aciertos y errores para calcular la tasa de fallo
    # TODO: implementar
    def error(self, datos, pred):
        
        # Aqui se compara la prediccion (pred) con las clases reales y se calcula el error
        if len(datos["Class"]) != len(pred):
            return None
        errores = len([ 1 for i in range(len(datos["Class"])) if datos["Class"].iloc[i] != pred[i]])

        
        return errores/len(datos["Class"])

    # Realiza una clasificacion utilizando una estrategia de particionado determinada
    # TODO: implementar esta funcion
    def validacion(self, particionado, dataset, clasificador, seed=None):

        # Creamos las particiones siguiendo la estrategia llamando a particionado.creaParticiones
        # - Para validacion cruzada: en el bucle hasta nv entrenamos el clasificador con la particion de train i
        # y obtenemos el error en la particion de test i
        # - Para validacion simple (hold-out): entrenamos el clasificador con la particion de train
        # y obtenemos el error en la particion test. Otra opci�n es repetir la validaci�n simple un n�mero especificado de veces, obteniendo en cada una un error. Finalmente se calcular�a la media.
        particiones = particionado.creaParticiones(dataset, seed)
        nparticiones = len(particiones)
        errores = []
        for part in particiones:

            # Estraemos los datos de train y test
            datosTrain = dataset.extraeDatos(part.indicesTrain)
            datosTest = dataset.extraeDatos(part.indicesTest)

            # TODO: No se que devuelve. Lo veremos en la siguiente practica
            clasificador.entrenamiento(datosTrain, dataset.nominalAtributos, dataset.diccionario)

            predicciones = clasificador.clasifica(datosTest, dataset.nominalAtributos, dataset.diccionario)
            errores.append( self.error(datosTest, predicciones) )
       
        return errores

##############################################################################


class ClasificadorNaiveBayes(Clasificador):

    # TODO: implementar
    def entrenamiento(self, datostrain, atributosDiscretos, diccionario):
        pass

    # TODO: implementar
    def clasifica(self, datostest, atributosDiscretos, diccionario):
        # TODO: Quitar cuando se implemente correctamente Naive Bayes
        return [0] * len(datostest)
        # pass
