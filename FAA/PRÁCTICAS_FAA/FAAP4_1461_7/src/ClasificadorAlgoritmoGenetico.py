from Clasificador import Clasificador
import math
import random
import numpy as np


class ClasificadorAlgoritmoGenetico(Clasificador):
    # cruce : ["inter", "intra"]
    # mutacion : ["all", "individual", "completa"]

    def __init__(self, tamPoblacion, nGeneraciones, maxReglas, pCruce, pMut, pElite = 0.05, cruce="intra", mutacion = "individual", saveEntrenamiento = False):
        self.pCruce = pCruce
        self.pMut = pMut
        self.pElite = pElite
        self.maxReglas = maxReglas
        self.tamPoblacion = tamPoblacion
        self.nGeneraciones = nGeneraciones
        self.func_cruce = self.__cruce_inter_regla if cruce == "inter" else self.__cruce_intra_regla
        self.func_mutacion = self.__mutacion_estandar_todas_reglas if mutacion == "all" else (self.__mutacion_estandar_una_regla if mutacion == "individual" else self.__mutacion_borra_o_añade_regla)

        self.saveEntrenamiento = saveEntrenamiento

    def nombre(self):
        return "Algoritmo Genético"


    def entrenamiento(self, datostrain, nominalAtributos, diccionario):
        if self.saveEntrenamiento == True:
            self.maxFitnessList = []
            self.meanFitnessList = []
            self.stdFitnessList = []
            self.generacionesList = []


        # guardamos el diccionario del dataset que usamos para clasificar porque se usa
        # al llamar a la funcion de representar el mejor individuo
        self.diccionario = diccionario
        self.nominalAtributos = nominalAtributos
        self.nombresAtributos = datostrain.columns


        self.atrLens = [len(values) for atributo, values in diccionario.items() if atributo != "Class"]
        self.longRegla = sum(self.atrLens) + 1
        
        poblacion = [[random.randint(0, 1) for i in range(self.longRegla*random.randint(3, max(3, self.maxReglas)))] for i in range(0, self.tamPoblacion)]
        fitness = [0 for i in range(self.tamPoblacion)]

        clase = datostrain["Class"]
        datostrain = datostrain.loc[:, datostrain.columns != "Class"]

        # Convertimos a numpy arrays porque van alrededor de 50x mas rapido que iterrows sobre el dataframe
        clase_nparray = clase.values
        datostrain_nparray = datostrain.values

        self.mostLikelyClass = round(sum(clase)/len(clase))

        # Maximo numero de individuos de la elite
        self.lenElites = round(self.tamPoblacion * self.pElite)


        for generacion in range(self.nGeneraciones):
            siguienteGeneracion = []

            # Elitismo
            elites = sorted(list(set([(tuple(cromosoma), fit) for cromosoma, fit in zip(poblacion, fitness)])), key = lambda x: x[1], reverse = True)[:self.lenElites]
            elites = [list(cromosoma) for cromosoma, fitness in elites]

            
            # Resto de la poblacion
            remainingIndivs = self.tamPoblacion - len(elites)
            while remainingIndivs > 0:


                # Metodo ruleta (random choice con weighted prob con respecto al fitness)
                if sum(fitness) == 0:
                    cromosoma1, cromosoma2 = random.choices(population=poblacion, k=2)
                else:
                    cromosoma1, cromosoma2 = random.choices(population=poblacion, weights=fitness, k=2)


                # Se hacen copias de los individuos para no trabajar con referencias del individuo en la poblacion y modificar el original
                cromosoma1 = cromosoma1.copy()
                cromosoma2 = cromosoma2.copy()


                # Cruce
                if random.random() < self.pCruce:
                    newCromosoma1, newCromosoma2 = self.func_cruce(cromosoma1, cromosoma2)
                else:
                    newCromosoma1, newCromosoma2 = cromosoma1, cromosoma2


                #Mutación
                newCromosoma1 = self.func_mutacion(newCromosoma1)
                newCromosoma2 = self.func_mutacion(newCromosoma2)


                # Si el nuevo cromosoma son todo 1s o 0s (menos la clase predicha que puede ser cualquiera), no se incluye en la poblacion nueva
                cromosoma1Pasa = True
                reglas = [newCromosoma1[i:i+self.longRegla] for i in range(0, len(newCromosoma1), self.longRegla)]
                for regla in reglas:
                    sumBits = sum(regla[:-1])
                    if sumBits == 0 or sumBits == len(regla) - 1:
                        cromosoma1Pasa = False
                        break

                cromosoma2Pasa = True
                reglas = [newCromosoma2[i:i+self.longRegla] for i in range(0, len(newCromosoma2), self.longRegla)]
                for regla in reglas:
                    sumBits = sum(regla[:-1])
                    if sumBits == 0 or sumBits == len(regla) - 1:
                        cromosoma2Pasa = False
                        break

                # Si las reglas son diferentes de todo 0s o todo 1s, pasan
                if cromosoma1Pasa: 
                    siguienteGeneracion.append(newCromosoma1)
                    remainingIndivs -= 1
                if remainingIndivs > 0:
                    if cromosoma2Pasa: 
                        siguienteGeneracion.append(newCromosoma2)
                        remainingIndivs -= 1


            # Juntamos a la elite con los hijos
            poblacion = (elites + siguienteGeneracion)

            # Calc fitness
            fitness = self.__calculate_fitness(datostrain_nparray, clase_nparray, poblacion)

            print(f"Iter: {generacion} - Max: {max(fitness)} - Mean: {np.mean(fitness)} - Stdv: {np.std(fitness)} - Pop size: {len(poblacion)}")

            if self.saveEntrenamiento == True:
                self.maxFitnessList.append(max(fitness))
                self.meanFitnessList.append(np.mean(fitness))
                self.stdFitnessList.append(np.std(fitness))
                self.generacionesList.append(generacion)

        
        self.mejorCromosoma = sorted([(cromosoma, fit) for cromosoma, fit in zip(poblacion, fitness)], key = lambda x: x[1], reverse = True)[0][0]
        print(f"Fin Ejecución: Max: {max(fitness)} - Mean: {np.mean(fitness)} - Stdv: {np.std(fitness)}")


    def __calculate_fitness(self, datostrain, clases, poblacion):
        fitness = []

        for cromosoma in poblacion:
            nAciertos = 0
            reglas = [cromosoma[i:i+self.longRegla] for i in range(0, len(cromosoma), self.longRegla)]
            for datapoint, clase in zip(datostrain, clases):

                votos = [0, 0]
                for regla in reglas:

                    voto = self.__clasificar_con_regla(datapoint, regla)
                    if voto is not None:
                        votos[voto] += 1

                if votos[0] == 0 and votos[1] == 0:
                    continue
                elif votos[0] == votos[1]:
                    pred = self.mostLikelyClass
                if votos[0] > votos[1]:
                    pred = 0
                else:
                    pred = 1
                if pred == clase:
                    nAciertos += 1

            fitness.append(nAciertos / len(datostrain))
                    
        return fitness


    def __clasificar_con_regla(self, datapoint, regla):

        atr = 0
        atrStart = None
        atrEnd = 0
        for x in datapoint:

            atrStart = atrEnd
            atrEnd = atrStart + self.atrLens[atr]

            if not regla[atrStart:atrEnd][x] == 1:
                return None

            atr += 1

        return regla[-1]


    def __cruce_inter_regla(self, cromosoma1, cromosoma2):
        puntoCorte = random.randint(1, min(len(cromosoma1), len(cromosoma2)))

        temp = cromosoma1[puntoCorte:]
        temp1 = cromosoma2[:puntoCorte] + cromosoma1[puntoCorte:]
        temp2 = cromosoma1[:puntoCorte] + cromosoma2[puntoCorte:]

        return temp1, temp2


    def __cruce_intra_regla(self, cromosoma1, cromosoma2):
        regla_a_cruzar1 = random.randint(0, (len(cromosoma1)/self.longRegla) - 1)
        regla_a_cruzar2 = random.randint(0, (len(cromosoma2)/self.longRegla) - 1)
        punto_de_corte = random.randint(0, self.longRegla-1)

        temp1 = cromosoma1[:(regla_a_cruzar1*self.longRegla + punto_de_corte)] + cromosoma2[(regla_a_cruzar2*self.longRegla + punto_de_corte) : ((regla_a_cruzar2+1)*self.longRegla)] + cromosoma1[((regla_a_cruzar1+1)*self.longRegla):]
        temp2 = cromosoma2[:(regla_a_cruzar2*self.longRegla + punto_de_corte)] + cromosoma1[(regla_a_cruzar1*self.longRegla + punto_de_corte) : ((regla_a_cruzar1+1)*self.longRegla)] + cromosoma2[((regla_a_cruzar2+1)*self.longRegla):]

        return temp1, temp2


    def __mutacion_estandar_todas_reglas(self, cromosoma):

        for idx in range(len(cromosoma)):
            if random.random() <= self.pMut:
                cromosoma[idx] ^= 1
        return cromosoma


    def __mutacion_estandar_una_regla(self, cromosoma):

        regla_a_mutar = random.randint(0, (len(cromosoma)/self.longRegla) - 1)
        for idx in range(regla_a_mutar*self.longRegla, (regla_a_mutar+1)*self.longRegla):
            if random.random() <= self.pMut:
                cromosoma[idx] ^= 1

        return cromosoma


    def __mutacion_borra_o_añade_regla(self, cromosoma):

        def añadir_regla_cromosoma(cromosoma):
            return cromosoma + [random.randint(0, 1) for i in range(self.longRegla)]

        def eliminar_regla_cromosoma(cromosoma):
            index_regla = random.randint(0, len(cromosoma)/self.longRegla - 1)
            return cromosoma[ : (self.longRegla * index_regla)] + cromosoma[( self.longRegla * (index_regla+1) ) : ]

        if random.random() <= self.pMut:
            reglasCromosoma = len(cromosoma)/self.longRegla
            if reglasCromosoma == 1:
                return añadir_regla_cromosoma(cromosoma)
            elif reglasCromosoma == self.maxReglas:
                return eliminar_regla_cromosoma(cromosoma)
            else:
                if random.random() < 0.5:
                    return añadir_regla_cromosoma(cromosoma)
                else:
                    return eliminar_regla_cromosoma(cromosoma)

        return cromosoma


    def clasifica(self, datostest, atributosDiscretos, diccionario):

        predicciones = []
        clase = datostest["Class"]
        datostest = datostest.loc[:, datostest.columns != "Class"]

        # Convertimos a numpy arrays porque van alrededor de 50x mas rapido que iterrows sobre el dataframe
        clase_nparray = clase.values
        datostest_nparray = datostest.values

        reglas = [self.mejorCromosoma[i:i+self.longRegla] for i in range(0, len(self.mejorCromosoma), self.longRegla)]

        for datapoint in datostest_nparray:
            votos = [0, 0]
            for regla in reglas:

                voto = self.__clasificar_con_regla(datapoint, regla)
                if voto is not None:
                    votos[voto] += 1

            if votos[0] == votos[1]:
                predicciones.append(self.mostLikelyClass)
            elif votos[0] > votos[1]:
                predicciones.append(0)
            else:
                predicciones.append(1)


        return predicciones

  
    def representarMejorCromosoma(self):
        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'


        returnstring = ""

        reglas = [self.mejorCromosoma[i:i+self.longRegla] for i in range(0, len(self.mejorCromosoma), self.longRegla)]
        lst = []
        for key, val in self.diccionario.items():
            lst.append({v: k for k, v in val.items()})

        
        for idx_regla, regla in enumerate(reglas):

            returnstring += f"\n{bcolors.BOLD}IF{bcolors.ENDC}  "
            
            comienzoAtr = 0
            firstAtr = True

            for numAtr, atrLength in enumerate(self.atrLens):
                x = []
                finAtr = comienzoAtr + atrLength
                
                for idx_bit, bit in enumerate(regla[comienzoAtr:finAtr]):
                    if bit == 1:
                        x.append(f"( {bcolors.UNDERLINE}{self.nombresAtributos[numAtr]}{bcolors.ENDC} == {bcolors.FAIL}{lst[numAtr][idx_bit]}{bcolors.ENDC} )")
                
                if len(x) > 0:
                    if firstAtr:

                        returnstring += "  "

                        firstAtr = False
                    else:
                        returnstring += f"  {bcolors.OKGREEN}AND{bcolors.ENDC} "

                    returnstring += f" {bcolors.OKBLUE}OR{bcolors.ENDC} ".join(x)
                    returnstring += "\n"

                comienzoAtr = finAtr

            returnstring += f"{bcolors.BOLD}THEN{bcolors.ENDC} {regla[-1]}\n"
        
        return returnstring
