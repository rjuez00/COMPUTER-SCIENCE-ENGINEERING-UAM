# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash

# inicializar variables (Ex. 2)
#N1 : 4560
#N2 : 5072

Ninicio=4560
Npaso=64
Nfinal=5072

cache_inicio=1024
cache_final=8192

fDAT_og=ex2/results/
iterations=10

#remove previous results
rm -R ex2/results

#The folders we need
mkdir ex2/results
mkdir ex2/results/plots


echo "Running slow and fast..."
#try different matrix sizes
for ((cache_size = cache_inicio ; cache_size <= cache_final ; cache_size = cache_size * 2)); do
	echo "current cache size: $cache_size"
	fDAT=$fDAT_og/$cache_size.dat
	# for N in $(seq $Ninicio $Npaso $Nfinal);
	for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
		echo "		N: $N / $Nfinal..."
		
		valgrind --LL=8388608,1,64 --I1=$cache_size,1,64 --D1=$cache_size,1,64 --tool=cachegrind --cachegrind-out-file=cache.dat ./fast $N &> /dev/null
		D1mr_fast=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
		D1mw_fast=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')
		
		valgrind --LL=8388608,1,64 --I1=$cache_size,1,64 --D1=$cache_size,1,64 --tool=cachegrind --cachegrind-out-file=cache.dat ./slow $N &> /dev/null
		D1mr_slow=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
		D1mw_slow=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')

		echo "		Fast:"
		echo "		 D1mr_fast: $D1mr_fast D1mw_fast: $D1mw_fast"
		echo "		Slow:"
		echo "		 D1mr_slow: $D1mr_slow D1mw_slow: $D1mw_slow"
		echo ""
		
		echo "$N $D1mr_slow $D1mw_slow $D1mr_fast $D1mw_fast" | tr -d , >> $fDAT

	done

done


fPNG_og=ex2/results/plots/plot
fPNGw=$fPNG_og\_write.png
fPNGr=$fPNG_og\_read.png

echo "Generating plots..."
#system('ls -1B') obtains all the files we want to plot
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top

set title "Cache Misses when Reading"
set ylabel "Read Cache Misses" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNGr"
set key samplen 2 spacing 1.0 font ", 20"
files=system('ls -1B ex2/results/*.dat')

plot for [file in files] file using 1:2 with lines lw 2 title file[13:16]." slow",\
	 for [file in files] file using 1:4 with lines lw 2 title file[13:16]." fast"
		
						
replot
quit
END_GNUPLOT


gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top

set title "Cache Misses when Writing"
set ylabel "Write Cache Misses" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNGw"
set key samplen 2 spacing 1.0 font ", 20"
files=system('ls -1B ex2/results/*.dat')

plot for [file in files] file using 1:3 with lines lw 2 title file[13:16]." slow",\
	 for [file in files] file using 1:5 with lines lw 2 title file[13:16]." fast"
		
						
replot
quit
END_GNUPLOT


rm cache.dat


