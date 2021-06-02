# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash

# inicializar variables (Ex. 3)
#N1   : 1536
#N2   : 1792
#step : 32

Ninicio=1536
Npaso=32
Nfinal=1792
iterations=3

fDAT=ex3/results/time.dat
# borrar el fichero DAT y el fichero PNG
rm -R $fDAT
mkdir -p ex3/results
# generar el fichero DAT vacío
touch $fDAT

#initialize arrays
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	timeNormal[$N]=0
	timeTrans[$N]=0
done

#calculate time 
echo "time:"
for ((I = 0 ; I < iterations ; I += 1)); do
	echo "	iteracion: $I"
	#date
	for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
		echo "		N: $N / $Nfinal..."
		timeNormal[$N]=`echo "${timeNormal[$N]} + $(./multi $N)" | bc -l`
		timeTrans[$N]=`echo "${timeTrans[$N]} + $(./multi $N t)" | bc -l`

	done
done
#print time to a temporal time
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	timeNormal[$N]=`echo "${timeNormal[$N]} / $iterations" | bc -l`
	timeTrans[$N]=`echo "${timeTrans[$N]} / $iterations" | bc -l`
   	echo "$N ${timeNormal[$N]} ${timeTrans[$N]}" | tr -d , >> $fDAT
done

unset timeNormal
unset timeTrans