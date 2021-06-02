mincores=4
maxcores=24

fPNG_og_time=ej2/plots/plot_time.png
fPNG_og_speedup=ej2/plots/plot_speedup.png

fDAT_time=ej2/results/resultados24.dat
fDAT_speedup=ej2/results/speedup.dat

echo "Generating time plots..."
#system('ls -1B') obtains all the files we want to plot
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top
set title "Scalar Product Time"
set ylabel "Seconds" font ", 25"
set xlabel "Vector Size" font ", 25"
set grid
set term png
set output "$fPNG_og_time"
set key samplen 2 spacing 1.0 font ", 20"
plot "$fDAT_time" using 1:2 with lines lw 2 linecolor rgb "black" title "Serie",\
     for [i=3:8] "$fDAT_time" using 1:i with lines lw 2 title "Threads: ".((i-2)*4)
						
replot
quit
END_GNUPLOT

# for [i=2:12] 'data'.i.'.txt' using 1:2 title 'Flow '.i

echo "Generating speedup plots..."
#system('ls -1B') obtains all the files we want to plot
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top
set title "Scalar Product Speedup depending on threads"
set ylabel "Times faster than serie" font ", 25"
set xlabel "Vector Size" font ", 25"
set grid
set term png
set output "$fPNG_og_speedup"
set key samplen 2 spacing 1.0 font ", 20"
plot for [i=2:7] "$fDAT_speedup" using 1:i with lines lw 2 title "Threads: ".((i-1)*4)
						
replot
quit
END_GNUPLOT

# for [i=2:12] 'data'.i.'.txt' using 1:2 title 'Flow '.i