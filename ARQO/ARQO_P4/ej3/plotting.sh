# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash


fPNG_og_time=ej3/plots/plot_time.png
fPNG_og_speedup=ej3/plots/plot_speedup.png

fDAT_time=ej3/resultados/resultados_plotting_1538.dat
fDAT_speedup=ej3/resultados/speedup.dat

echo "Generating plots..."
#system('ls -1B') obtains all the files we want to plot
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top
set title "Multiplication Time"
set ylabel "Seconds" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNG_og_time"
set key samplen 2 spacing 1.0 font ", 20"
plot "$fDAT_time" using 1:2 with lines lw 2 title "serie",\
	 "$fDAT_time" using 1:3 with lines lw 2 title "parallel 3 (12 cores)"
						
replot
quit
END_GNUPLOT


gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top
set title "Multiplication Speedup"
set ylabel "Times faster" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNG_og_speedup"
set key samplen 2 spacing 1.0 font ", 20"
plot "$fDAT_speedup" using 1:2 with lines lw 2 title "parallel 3 (12 cores)"
						
replot
quit
END_GNUPLOT