# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash

# inicializar variables (Ex. 3)
#N1   : 1536
#N2   : 1792
#step : 32

Ninicio=1536
Npaso=32
Nfinal=1792
fDAT=ex3/results/cache.dat

# borrar el fichero DAT y el fichero PNG
rm -R $fDAT
mkdir -p ex3/results
# generar el fichero DAT vacío
touch $fDAT



echo "cache:"
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	echo "		N: $N / $Nfinal..."
	date

	valgrind --tool=cachegrind --cachegrind-out-file=cache.dat ./multi $N &> /dev/null
	D1mr_normal=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
	D1mw_normal=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')
	
	valgrind --tool=cachegrind --cachegrind-out-file=cache.dat ./multi $N t &> /dev/null
	D1mr_trans=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
	D1mw_trans=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')
	#print cache to a temporal file
	echo "$N $D1mr_normal $D1mw_normal $D1mr_trans $D1mw_trans" | tr -d , >> $fDAT
done

date
rm cache.dat

