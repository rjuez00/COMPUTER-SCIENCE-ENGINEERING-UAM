from unicodedata import decimal
import pandas as pd
import numpy as np


def print_all_id(id_a_comprobar):
    slice_de_id = dataset.loc[dataset["id"] == id_a_comprobar]
    pd.set_option('display.max_rows', len(slice_de_id))
    print(slice_de_id)


def load_dataset(base_folder = "dataset"):
    dataset = pd.read_csv(f'{base_folder}/HT_Sensor_dataset.dat', delim_whitespace=True)
    metadataset = pd.read_csv(f'{base_folder}/HT_Sensor_metadata.dat', delim_whitespace=True).set_index("id", drop = True)
    
    return dataset, metadataset


def limpiar_combinar_dataset(dataset, metadataset):

    temp_df = pd.merge(dataset, metadataset[["class", "dt"]], left_on="id", right_index=True, how="left")
    dataset["Class"] = "background"
    dataset.loc[(temp_df["time"] >= 0) & (dataset["time"] <= temp_df["dt"]), "Class"] = temp_df["class"]


def sliding_window(x, y, window):
    """
    Usamos una sliding window de tamapño window para optimizar el calculo de nuevas columnas
    Si no tardaría demasiado el programa (horas), en vez de los 10-20 min que tarda este en
    generar 50 columnas nuevas para el dataset con 1MM de filas
    """

    stds = np.empty(len(x))
    slps = np.empty(len(x))
    stds[:] = np.nan
    slps[:] = np.nan

    Sy = 0
    Sx = 0
    Sxx = 0
    Sxy = 0

    windowStartIdx = 0
    windowEndIdx = 0
    for val in x[1:]:

        windowEndIdx += 1
        Sy += y[windowEndIdx-1]
        Sx += x[windowEndIdx-1]
        Sxx += x[windowEndIdx-1] * x[windowEndIdx-1]
        Sxy += x[windowEndIdx-1] * y[windowEndIdx-1]
        while x[windowStartIdx] + 0.00001 < val - window:
            Sy -= y[windowStartIdx]
            Sx -= x[windowStartIdx]
            Sxx -= x[windowStartIdx] * x[windowStartIdx]
            Sxy -= x[windowStartIdx] * y[windowStartIdx]
            windowStartIdx += 1

        # There has to be at least 3 measurements in the window
        if windowStartIdx >= windowEndIdx - 3:
            pass
        elif val - window >= -1:
            n = windowEndIdx - windowStartIdx
            stds[windowEndIdx] = np.std(y[windowStartIdx:windowEndIdx])
            slps[windowEndIdx] = (n * Sxy - Sx * Sy) / (n * Sxx - Sx * Sx) # Fast approximation of the slope

    return stds, slps


def new_columns(dataset, window):

    subdatasets = { id: dataset[(dataset["id"]==id)] for id in dataset['id'].unique() }

    for id, subdataset in subdatasets.items():
        if id == 0:
            continue
        columnas = { col: subdataset[col].to_numpy() for col in subdataset.columns }
        for string in ["R2", "R6", "R8", "Temp.", "Humidity"]:
            stds, slps = sliding_window(columnas["time"], columnas[string], window)
            dataset.loc[dataset["id"] == id,string+"Std"] = np.around(stds, decimals=5)
            dataset.loc[dataset["id"] == id,string+"Slope"] = np.around(slps, decimals=5)


# Load and clean dataset
dataset, metadataset = load_dataset()
limpiar_combinar_dataset(dataset, metadataset)

print(metadataset['class'].value_counts())

print("Finished loading dataset")
new_columns(dataset, 3 * 0.0166666) # Ventana de 3 minutos

# Elimina las filas con NaN que pueden aparecer despues de crear las nuevas columnas
# (Por ejemplo si no cabe la ventana entera o no hay al menos 2-3 datos en ella se pone el valor a NaN)
dataset = dataset.dropna()

# Balanceo del dataset. Mira que clase tiene menos datapoints y los coge todos.
# De las otras clases hace un random sample de la misma cantidad. De esta forma estan perfectamente balanceadas
df = (dataset.groupby('Class', as_index=False)
        .apply(lambda x: x.sample(n=dataset.groupby('Class').size().min()))
        .reset_index(drop=True))

# Mueve la columna de la clase al final
cols = df.columns.to_list()
cols.remove('Class')
cols.append('Class')
df = df.reindex(columns=cols)

df = df.drop(columns=['id', 'time', 'R5', 'R1', 'R3', 'R4', 'R7'])

df.to_csv('dataset_final.csv', index=False) 

print(df)
