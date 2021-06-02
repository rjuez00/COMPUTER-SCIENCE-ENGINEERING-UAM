# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash

# inicializar variables (Ex. 3)
#N1   : 1536
#N2   : 1792
#step : 32

Ninicio=1536
Npaso=32
Nfinal=1792
iterations=6


fDAT=ex4/results6/$iterations\_iteratfions.dat
fPNG_time=ex4/results6/$iterations\_plot_time.png
fPNG_cache=ex4/results6/plot_cache.png

# Remove the DAT and the PNG files.
rm -R ex4/results6
mkdir ex4/results6

# Generate an empty DAT file.
touch $fDAT

echo "Running slow and fast..."

for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	timeNormal[$N]=0
	timeTrans[$N]=0
done

echo "time:"
for ((I = 0 ; I < iterations ; I += 1)); do
	echo "	iteracion: $I"
	#date
	for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
		echo "		N: $N / $Nfinal..."
		timeNormal[$N]=`echo "${timeNormal[$N]} + $(valgrind --LL=8388608,1,64 --I1=8192,1,64 --D1=8192,1,64 --tool=cachegrind --cachegrind-out-file=cache.dat ./slow $N 2> /dev/null | grep "time" | awk '{print $3}')" | bc -l`
		timeTrans[$N]=`echo "${timeTrans[$N]} + $(valgrind --LL=8388608,1,32 --I1=8192,1,32 --D1=8192,1,32 --tool=cachegrind --cachegrind-out-file=cache.dat ./slow $N 2> /dev/null | grep "time" | awk '{print $3}')" | bc -l`
	done
done

for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	timeNormal[$N]=`echo "${timeNormal[$N]} / $iterations" | bc -l`
	timeTrans[$N]=`echo "${timeTrans[$N]} / $iterations" | bc -l`
done

echo "cache:"
# We iterate through matrix sizes.
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	echo "		N: $N / $Nfinal..."
	
	# We call the slow.c program.
	valgrind --LL=8388608,1,64 --I1=8192,1,64 --D1=8192,1,64 --tool=cachegrind --cachegrind-out-file=cache.dat ./slow $N &> /dev/null
	D1mr_normal=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
	D1mw_normal=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')
	
	# We call the fast.c program.
	valgrind --LL=8388608,1,64 --I1=8192,1,32 --D1=8192,1,32 --tool=cachegrind --cachegrind-out-file=cache.dat ./slow $N &> /dev/null
	D1mr_trans=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
	D1mw_trans=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')
	
	# We write the data into the file.
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

set title "Slow Cache Misses"
set ylabel "Misses (s)" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNG_cache"
plot "$fDAT" using 1:3 with lines lw 2 title "Read Line Size 64", \
     "$fDAT" using 1:4 with lines lw 2 title "Write Line Size 64", \
	 "$fDAT" using 1:6 with lines lw 2 linecolor "cyan" title "Read Line Size 32", \
	 "$fDAT" using 1:7 with lines lw 2 title "Write Line Size 32"
replot
quit
END_GNUPLOT




echo "Generating plot time..."
# llamar a gnuplot para generar el gráfico y pasarle directamente por la entrada
# estándar el script que está entre "<< END_GNUPLOT" y "END_GNUPLOT"
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top

set title "Slow Execution Time"
set ylabel "Execution time (s)"
set xlabel "Matrix Size"
set key right bottom
set grid
set term png
set output "$fPNG_time"
plot "$fDAT" using 1:2 with lines lw 2 title "Line Size 64", \
     "$fDAT" using 1:5 with lines lw 2 title "Line Size 32"
replot
quit
END_GNUPLOT
