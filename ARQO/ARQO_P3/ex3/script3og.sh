# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash

# inicializar variables (Ex. 3)
#N1   : 1536
#N2   : 1792
#step : 32

Ninicio=1536
Npaso=32
Nfinal=1792
iterations=2

fDAT=ex3/results/$iterations\_iterations.dat
fPNG_time=ex3/results/$iterations\_plot_time.png
fPNG_cache=ex3/results/plot_cache.png
# borrar el fichero DAT y el fichero PNG
rm -R ex3/results
mkdir ex3/results
# generar el fichero DAT vacío
touch $fDAT

echo "Running slow and fast..."
#initialize array
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	timeNormal[$N]=0
	timeTrans[$N]=0
done

echo "time:"
for ((I = 0 ; I < iterations ; I += 1)); do
	echo "	iteracion: $I"
	date #this is to check what a iteration lasts so that I can calculate what the simulation will last
	for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
		echo "		N: $N / $Nfinal..."
		timeNormal[$N]=`echo "${timeNormal[$N]} + $(./multi $N)" | bc -l`
		timeTrans[$N]=`echo "${timeTrans[$N]} + $(./multi $N t)" | bc -l`

	done
done
#calculate average but not printing
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	timeNormal[$N]=`echo "${timeNormal[$N]} / $iterations" | bc -l`
	timeTrans[$N]=`echo "${timeTrans[$N]} / $iterations" | bc -l`
done
#simulate with valgrind AND printing
echo "cache:"
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	echo "		N: $N / $Nfinal..."
	
	valgrind --tool=cachegrind --cachegrind-out-file=cache.dat ./multi $N &> /dev/null
	D1mr_normal=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
	D1mw_normal=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')
	
	valgrind --tool=cachegrind --cachegrind-out-file=cache.dat ./multi $N t &> /dev/null
	D1mr_trans=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
	D1mw_trans=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')
	#as valgrind has only one iteration i can print right away
	echo "$N ${timeNormal[$N]} $D1mr_normal $D1mw_normal ${timeTrans[$N]} $D1mr_trans $D1mw_trans" | tr -d , >> $fDAT
done

#date
unset timeNormal
unset timeTrans
rm cache.dat

echo "Generating plot caches..."
# llamar a gnuplot para generar el gráfico y pasarle directamente por la entrada
# estándar el script que está entre "<< END_GNUPLOT" y "END_GNUPLOT"
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top
set title "Multiplication Cache Misses"
set ylabel "Misses (s)" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNG_cache"
plot "$fDAT" using 1:3 with lines lw 2 title "Read Normal", \
     "$fDAT" using 1:4 with lines lw 2 title "Write Normal", \
	 "$fDAT" using 1:6 with lines lw 2 linecolor "cyan" title "Read Transposed", \
	 "$fDAT" using 1:7 with lines lw 2 title "Write Transposed"
replot
quit
END_GNUPLOT




echo "Generating plot time..."
# llamar a gnuplot para generar el gráfico y pasarle directamente por la entrada
# estándar el script que está entre "<< END_GNUPLOT" y "END_GNUPLOT"
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top
set title "Multiplication Execution Time"
set ylabel "Execution time (s)"
set xlabel "Matrix Size"
set key right bottom
set grid
set term png
set output "$fPNG_time"
plot "$fDAT" using 1:2 with lines lw 2 title "Normal", \
     "$fDAT" using 1:5 with lines lw 2 title "Transposed"
replot
quit
END_GNUPLOT