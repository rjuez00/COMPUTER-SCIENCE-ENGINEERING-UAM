import pandas as pd
import matplotlib.pyplot as plt

base_folder = "../dataset"
dataset = pd.read_csv(f'{base_folder}/HT_Sensor_dataset.dat', delim_whitespace=True)
metadataset = pd.read_csv(f'{base_folder}/HT_Sensor_metadata.dat', delim_whitespace=True).set_index("id", drop=True)

temp_df = pd.merge(dataset, metadataset[["class", "dt"]], left_on="id", right_index=True, how="left")

dataset.loc[(temp_df["time"] < 0), "Class"] = "background_before"
dataset.loc[(temp_df["time"] >= 0) & (dataset["time"] <= temp_df["dt"]), "Class"] = temp_df["class"]
dataset.loc[(temp_df["time"] >= 0) & (dataset["time"] > temp_df["dt"]), "Class"] = "background_after"

# Código para mostrar por qué quitar el sensor 5
df = dataset
groupedDf = df.drop(columns=['id', 'time']).groupby(['Class'])

for key, val in groupedDf:
    val.plot(title=key)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

# Código para mostrar por qué añadimos nuevos atributos (media, min, max)
df = dataset
groupedDf = df.drop(columns=['id', 'time']).groupby(['Class'])

sensorNames = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'Temp.', 'Humidity']

classNames = []
means = {}
stds = {}
for sensor in sensorNames:
    means[sensor] = []
    stds[sensor] = []

for key, val in groupedDf:
    classNames.append(key)

    for col in val:
        if (col == "Class"):
            break
        mean = val[col].mean()
        std = val[col].std()

        means[col].append(mean)
        stds[col].append(std)

newOrder = [2, 3, 0, 4, 1]
classNames = [classNames[idx] for idx in newOrder]

plt.figure(figsize=(8, 20))
pltIdx = 0
idxs = [1, 1, 2, 2, 3, 3, 4, 4, 5, 6]
titles = ["R1 & R2", "R1 & R2", "R3 & R4", "R3 & R4", "R5 & R6", "R5 & R6", "R7 & R8", "R7 & R8", "Temperatura",
          "Humedad"]

for key, mean in means.items():
    mean = [mean[idx] for idx in newOrder]
    stds[key] = [stds[key][idx] for idx in newOrder]
    plt.subplot(10, 1, idxs[pltIdx])
    plt.errorbar(classNames, mean, stds[key], marker='o', capsize=5)
    plt.title(titles[pltIdx], fontsize=12, loc='left', pad=2)
    plt.subplots_adjust(bottom=0, top=1.2, hspace=0.5)
    pltIdx += 1
plt.show()
