import numpy as np
import pandas as pd
import random
import collections


class KMeans:

    def __init__(self, dataset, k_clusters):
        self.datos = dataset.datos
        self.k_clusters = k_clusters
        self.clusters = [[] for _ in range(k_clusters)]
    

    def clusterea(self):

        random_starting_seeds = self.datos.sample(self.k_clusters).index.tolist()
        centroids = [self.datos.iloc[x, self.datos.columns != "Class"] for x in random_starting_seeds]

        flag = False

        n_iters = 0
        while True:

            n_iters += 1
            last_clusters = self.clusters.copy()
            self.clusters = [[] for _ in range(self.k_clusters)]

            for index, point in self.datos.loc[:, self.datos.columns != "Class"].iterrows():

                minDist = np.inf
                closestCentroid = None

                for idx, centroid in enumerate(centroids):

                    dist = np.linalg.norm(point - centroid)
                    if dist < minDist:
                        minDist = dist
                        closestCentroid = idx

                self.clusters[closestCentroid].append(index)

            if self.clusters == last_clusters and flag:
                print("Se han necesitado {} iteraciones para formar los clusters.".format(n_iters))
                break
            elif self.clusters == last_clusters:
                flag = True
            else:
                flag = False      
            
            for i in range(self.k_clusters):
                centroids[i] = self.datos.iloc[self.clusters[i], self.datos.columns != "Class"].mean(axis=0)

            

    @classmethod
    def matriz_confusion(cls, dataset, clusters):
        clases = list(dataset.diccionario["Class"].keys())
        datos = dataset.datos

        cuentaclusters = {}
        for idx, cluster in enumerate(clusters):
            tempdict = {}
            for clase in clases:              
                tempdict[str(clase)] = len([indice for indice in cluster if datos.iloc[indice]["Class"] == float(clase)])
           
            cuentaclusters[f"c{idx}_{max(tempdict, key=tempdict.get)}"] = tempdict


        return pd.DataFrame(collections.OrderedDict(sorted(cuentaclusters.items(), key = lambda x: x[0][-1])))
