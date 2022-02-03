import pandas as pd
import matplotlib.pyplot as plt

base_folder = "../dataset"
df = pd.read_csv(f'{base_folder}/dataset_final.csv')

plt.matshow(df.corr())
plt.show()

# df = df[df.columns.drop(list(df.filter(regex=r'(R1|R3|R4|R7|Min|Max|Mean)')))]

plt.matshow(df.corr())
plt.show()
