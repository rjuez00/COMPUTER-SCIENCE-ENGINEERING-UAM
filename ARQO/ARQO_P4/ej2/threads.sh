# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash

# inicializar variables (Ex. 2)
#N1 : 4560
#N2 : 5072

Ninicio=100 #524286
Npaso=2
Nfinal=1000 #168435455
niterations=2

mincores=4
maxcores=8 #24

fDAT=ej2/results/resultados$maxcores.dat

rm -rf $fDAT
touch $fDAT



for ((N = Ninicio; N <= Nfinal ; N *= Npaso)); do
    echo "$N/$Nfinal"
    for ((core = mincores; core <= maxcores ; core += 4)); do
        fast[$core]=0
    done


    #try different matrix sizes
    for ((iterations = 1 ; iterations <= niterations ; iterations = iterations +1)); do
        echo "      $iterations/$niterations"
        slow=$(./pescalar_serie_forscript $N | grep Tiempo | awk '{ print $2 }')
        for ((core = mincores; core <= maxcores ; core += 4)); do
            fast[$core]=`echo "${fast[$core]}+$(./pescalar_par3_forscript $N $core | grep Tiempo | awk '{ print $2 }')" | bc -l`
        done
    done

    final="$N "
    final+=$(echo "`echo "$slow/${niterations}" | bc -l` ")
    for ((core = mincores; core <= maxcores ; core +=4)); do
        final+=$(echo "$(echo "${fast[$core]}/${niterations}" | bc -l)")" "
    done

    echo $final >> $fDAT
    unset final
done

unset slow
unset fast

: '
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
END_GNUPLOT'
