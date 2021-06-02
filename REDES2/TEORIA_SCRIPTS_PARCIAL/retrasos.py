print("PROPIEDAD DE: RODRIGO JUEZ HERNÁNDEZ")
print("DISEÑADO PARA EL 3er PARCIAL DE REDES2")

"""
ids = [1,2,3,4,5,6,8,9,10,12,11,14]
tr = [60.2, 75.5, 81.8, 102.4, 121.7, 173.1, 213.1, 235.3, 251.4, 265.3, 276.8, 318.7]
ts = [20,40,60,80,100,132,172,192,212,252,232,300]

ids = [1,2,3,4,5,6,7,8,9,10,11,12]
ts = [20, 42.64, 62.64,82.64,102.64,122.64,142.64,173.87,209.18,229.18,249.18,269.18]
tr = [145.6,170.81,151.25,183.21,238.74,234.48,226.74,318.02,329.51,348.75,356.03,376.48]
"""
print("RECUERDA COMPROBAR start_id y RETRASO FIJO!!!!!")
"""
ids = [1,2,3,5,4,8,6,7,13,11,10,12,15,16,21,20,17,19,22,23]
ts = [20, 40,60,112,80,172,132,152,288,242,222,268,328,350,480,435,370,415,500,520]
tr = [60.2,75.5,91.8,140.4,141.7,230.1,232.8,234.1,380.1,382.5,389.1,395.6,441.4,442.3,501.2,502.1,505.2,526.2,538.5,549.3]
"""
ids = [1,2,3,4,5,6,7,8,9,10,11,12]
ts = [20,40,63.73, 83.73, 116.01, 141.6, 161.6, 181.6, 201.6, 221.6, 255.27, 292.08]
tr = [169.96,171.31,172.83,205.98,246.74,274.04,302.71,294.56,344.52,341.31,378.72,402.7]

retraso_fijo = 122.85
start_id = 1
"EJERCICIO A"
paquetes_perdidos = [i for i in range(1, max(ids)+1)  if i not in ids]
print(f"paquetes que faltan {paquetes_perdidos}")



"EJERCICIO B"
"tp es tiempo reproduccion"
dataset = sorted(zip(ids, ts, tr), key=lambda tup: tup[0])
tp = [dataset[0][2] + retraso_fijo]

for i in range(1, len(dataset)):
    tp.append(dataset[i][1]-dataset[i-1][1] + tp[-1])

no_reproducidos = [dataset[i][0] for i in range(0, len(dataset)) if dataset[i][2] > tp[i]]
print(f"estos paquetes no se han reproducido {no_reproducidos}")

"EJERCICIO C"
paquetes_silencio = [dataset[i-1][0] for i in range(1, len(dataset)) if ((round((dataset[i][1]-dataset[i-1][1]), 5) % 20) != 0)]
print(f"tras estos paquetes hay un silencio {paquetes_silencio}")



"EJERCICIO D"
tretraso = [tp[i] - dataset[i][2] for i in range(0, len(dataset))]
print(f"el minimo retardo necesario es {round(retraso_fijo-min(tretraso), 2)}")

print("====================================")
print("#\tTS\tTR\tpi\t\tretraso")
for i in range(0, len(dataset)):
    print(f"{dataset[i][0]}\t{dataset[i][1]}\t{dataset[i][2]}\t{round(tp[i], 2)}\t\t{round(tretraso[i], 2)}")


