# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash

cache_associativity_inicio=1
cache_associativity_final=64

Ninicio=4560
Npaso=64
Nfinal=5072


fDAT_og=ex4/results/
fPNG_cache=ex4/results/plot_cache.png

# Remove the DAT and the PNG files.
rm -Rf ex4/results
mkdir ex4/results
mkdir ex4/results/plots

# Generate an empty DAT file.
touch $fDAT


echo "cache:"
# Basically the same as iterations but with cache_associativity.
for ((cache_associativity = cache_associativity_inicio ; cache_associativity <= cache_associativity_final ; cache_associativity = cache_associativity * 4)); do
	echo "current cache associativity: $cache_associativity"
	fDAT=$fDAT_og/$cache_associativity\_associ.dat
	
	# We iterate through matrix sizes.
	for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
		echo "		N: $N / $Nfinal..."
		
		# We call the slow.c program.
		valgrind --LL=8388608,$cache_associativity,64 --I1=8192,$cache_associativity,64 --D1=8192,$cache_associativity,64 --tool=cachegrind --cachegrind-out-file=cache.dat ./fast $N &> /dev/null
		D1mr_fast=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
		D1mw_fast=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')
		
		# We call the fast.c program.
		valgrind --LL=8388608,$cache_associativity,64 --I1=8192,$cache_associativity,64 --D1=8192,$cache_associativity,64 --tool=cachegrind --cachegrind-out-file=cache.dat ./slow $N &> /dev/null
		D1mr_slow=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $5}')
		D1mw_slow=$(cg_annotate cache.dat | head -n 19 | grep 'PROGRAM TOTALS' | awk '{print $8}')

		echo "		Fast:"
		echo "		 D1mr_fast: $D1mr_fast D1mw_fast: $D1mw_fast"
		echo "		Slow:"
		echo "		 D1mr_slow: $D1mr_slow D1mw_slow: $D1mw_slow"
		echo ""
		
		# We write the data into the file.
		echo "$N $D1mr_slow $D1mw_slow $D1mr_fast $D1mw_fast" | tr -d , >> $fDAT

	done

done

rm cache.dat

# We get the location where the plots will be.
fPNG_og=ex4/results/plots/plot
fPNGw=$fPNG_og\_write.png
fPNGr=$fPNG_og\_read.png


echo "Generating plots..."
# llamar a gnuplot para generar el gráfico y pasarle directamente por la entrada
# estándar el script que está entre "<< END_GNUPLOT" y "END_GNUPLOT"
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top

set title "Cache Misses when Reading (variable Associativity)"
set ylabel "Read Cache Misses" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNGr"
set key samplen 2 spacing 1.0 font ", 20"
files=system('ls -1B ex4/results/*.dat')

plot for [file in files] file using 1:2 with lines lw 2 title file." slow",\
	 for [file in files] file using 1:4 with lines lw 2 title file." fast"
		
						
replot
quit
END_GNUPLOT



# llamar a gnuplot para generar el gráfico y pasarle directamente por la entrada
# estándar el script que está entre "<< END_GNUPLOT" y "END_GNUPLOT"
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top

set title "Cache Misses when Writing (variable Associativity)"
set ylabel "Write Cache Misses" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNGw"
set key samplen 2 spacing 1.0 font ", 20"
files=system('ls -1B ex4/results/*.dat')

plot for [file in files] file using 1:3 with lines lw 2 title file." slow",\
	 for [file in files] file using 1:5 with lines lw 2 title file." fast"
		
						
replot
quit
END_GNUPLOT
