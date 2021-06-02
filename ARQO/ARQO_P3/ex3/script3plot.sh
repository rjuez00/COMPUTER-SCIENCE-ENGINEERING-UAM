
fPNG_time=ex3/results/plot_time.png
fPNG_cache=ex3/results/plot_cache.png
fDAT=ex3/results/final.dat


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

