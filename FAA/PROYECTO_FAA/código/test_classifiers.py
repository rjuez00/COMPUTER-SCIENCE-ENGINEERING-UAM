import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier



def KNN(args):

    X = args[0]
    y = args[1]
    k = args[2]

    clf = KNeighborsClassifier(n_neighbors=k)
    scalar = StandardScaler()
    # Pipeline que normaliza antes de clasificar en cada fold para no normalizar
    # usando todos los datos sino solo los de train
    pipeline = Pipeline([('transformer', scalar), ('estimator', clf)])
    scores = cross_val_score(pipeline, X, y, cv=5)

    return (k, np.mean(scores), np.std(scores))


def NeuralNetwork(args):

    X = args[0]
    y = args[1]
    hiddenLayers = args[2]
    neuronsLayer = args[3]

    clf = MLPClassifier(hidden_layer_sizes=tuple([neuronsLayer for _ in range(hiddenLayers)]), max_iter=2000)
    scalar = StandardScaler()
    # Pipeline que normaliza antes de clasificar en cada fold para no normalizar
    # usando todos los datos sino solo los de train
    pipeline = Pipeline([('transformer', scalar), ('estimator', clf)])
    scores = cross_val_score(pipeline, X, y, cv=5)

    return (hiddenLayers, neuronsLayer, np.mean(scores), np.std(scores))


def RandomForest(args):

    X = args[0]
    y = args[1]
    n = args[2]

    clf = RandomForestClassifier(n_estimators=n)
    scores = cross_val_score(clf, X, y, cv=5)

    return (n, np.mean(scores), np.std(scores))

from multiprocessing import Pool
if __name__ == '__main__':

    df = pd.read_csv("dataset_final.csv")
    X = df.loc[:, df.columns != "Class"].to_numpy()
    y = df["Class"].to_numpy()

    pool = Pool(processes=4)


    print("Gaussian Naive Bayes\n")

    clf = GaussianNB()
    scores = cross_val_score(clf, X, y, cv=5)

    naiveBayesDf = pd.DataFrame(columns=('Accur.', 'Desv'))
    naiveBayesDf.loc[0] = [np.mean(scores), np.std(scores)]

    print(naiveBayesDf)


    print("\n\nK Nearest Neighbors\n")
    
    results = pool.map(KNN, [(X, y, k) for k in range(3, 39, 5)])
    results.sort(key=lambda tup: tup[0])

    knnDf = pd.DataFrame(columns=('K', 'Accur.', 'Desv'))
    for idx, res in enumerate(results):
        knnDf.loc[idx] = [res[0], res[1], res[2]]
    knnDf = knnDf.astype({'K': int})

    print(knnDf)


    print("\n\nLogistic Regression\n")

    clf = LogisticRegression(multi_class='multinomial', solver='saga')
    scalar = StandardScaler()
    # Pipeline que normaliza antes de clasificar en cada fold para no normalizar
    # usando todos los datos sino solo los de train
    pipeline = Pipeline([('transformer', scalar), ('estimator', clf)])
    scores = cross_val_score(pipeline, X, y, cv=5)

    logRegDf = pd.DataFrame(columns=('Accur.', 'Desv'))
    logRegDf.loc[0] = [np.mean(scores), np.std(scores)]

    print(logRegDf)


    print("\n\nNeural Network\n")
    
    results = pool.map(NeuralNetwork, [(X, y, i, j) for i in range(1,3) for j in [10, 20, 30, 40]])
    results.sort(key=lambda tup: tup[0])

    yIndex = [
        ("1", "10"),
        ("1", "20"),
        ("1", "30"),
        ("1", "40"),
        ("2", "10"),
        ("2", "20"),
        ("2", "30"),
        ("2", "40"),
    ]
    namesy = ["Capas", "Neuronas/Capa"]

    neuralNetDf = pd.DataFrame(index=pd.MultiIndex.from_tuples(yIndex, names = namesy), columns=('Accur.', 'Desv'), dtype=float)
    for idx, res in enumerate(results):
        neuralNetDf.loc[(str(res[0]), str(res[1]))] = [res[2], res[3]]

    print(neuralNetDf)

    
    print("\n\nRandom Forest\n")

    results = pool.map(RandomForest, [(X, y, n) for n in range(10, 171, 20)])
    results.sort(key=lambda tup: tup[0])

    randForestDf = pd.DataFrame(columns=('N Estim.', 'Accur.', 'Desv'))
    for idx, res in enumerate(results):
        randForestDf.loc[idx] = [res[0], res[1], res[2]]
    randForestDf = randForestDf.astype({'N Estim.': int})

    print(randForestDf)

    
    print("########## Codigo Latex de las Tablas de Resultados ##########")

    print("\nGaussian Naive Bayes\n")
    print(naiveBayesDf.to_latex(index=False))

    print("\n\nK Nearest Neighbors\n")
    print(knnDf.to_latex(index=False))

    print("\n\nLogistic Regression\n")
    print(logRegDf.to_latex(index=False))

    print("\n\nNeural Network\n")
    print(neuralNetDf.to_latex())

    print("\n\nRandom Forest\n")
    print(randForestDf.to_latex(index=False))

    pool.close()
