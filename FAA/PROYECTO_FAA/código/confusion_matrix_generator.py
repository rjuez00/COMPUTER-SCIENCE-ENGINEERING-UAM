import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline
import sklearn.metrics
import matplotlib.pyplot as plt


def load_dataset(filename = "dataset_final.csv", sample = None):
    df = pd.read_csv(filename)
    if sample != None:
        df = df.sample(sample)
    X = df.loc[:, df.columns != "Class"].to_numpy()
    y = df["Class"].to_numpy()
    return train_test_split(X, y)
   
def normalize(X_train, X_test):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test

def KNN(X_train, y_train):
    return KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)

def NN(X_train, y_train):
    return MLPClassifier(hidden_layer_sizes=(40, 40), max_iter=2000).fit(X_train, y_train)

def RandomForest(X_train, y_train):
    return RandomForestClassifier(n_estimators=110).fit(X_train, y_train)

def confusion_matrix(classifier_fitted, X_test, y_test, title, axes):
    
    disp = ConfusionMatrixDisplay(
        sklearn.metrics.confusion_matrix(y_test, classifier_fitted.predict(X_test)), 
        display_labels = classifier_fitted.classes_).plot(ax = axes)
    disp.ax_.set_title(title)

    return disp


X_train, X_test, y_train, y_test = load_dataset(sample = 21700)
X_train_norm, X_test_norm = normalize(X_train, X_test)
knn = KNN(X_train_norm, y_train)
nn = NN(X_train_norm, y_train)
rf = RandomForest(X_train, y_train)

f, axes = plt.subplots(1, 3, figsize=(20, 5))
confusion_matrix(knn, X_test_norm, y_test, "KNN (N = 3)", axes[0])
confusion_matrix(nn, X_test_norm, y_test, "Neural Network (Capas = 2; Neuronas/Capa = 40)", axes[1])
confusion_matrix(rf, X_test, y_test, "Random Forest (N Estimators = 110)", axes[2])
plt.tight_layout()
plt.show()


