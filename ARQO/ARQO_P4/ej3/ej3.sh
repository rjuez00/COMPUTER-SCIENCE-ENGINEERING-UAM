# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash




niterations=1

mincores=1
maxcores=4

fDAT=ej3/resultados/resultados$maxcores\_$1.dat

rm -rf $fDAT
touch $fDAT

for ((core = mincores; core <= maxcores ; core += 1)); do
    multi0[$core]=0
    multi1[$core]=0
    multi2[$core]=0
    multi3[$core]=0
done


for ((iterations = 1 ; iterations <= niterations ; iterations = iterations +1)); do
    echo "$iterations/$niterations"
    for ((core = mincores; core <= maxcores ; core += 1)); do
        echo "  $core/$maxcores"
   		multi0[$core]=`echo "${multi0[$core]}+$(./multi0 $1 t | grep Tiempo | awk '{ print $2 }')" | bc -l`
		multi1[$core]=`echo "${multi1[$core]}+$(./multi1 $1 $core t | grep Tiempo | awk '{ print $2 }')" | bc -l`
		multi2[$core]=`echo "${multi2[$core]}+$(./multi2 $1 $core t | grep Tiempo | awk '{ print $2 }')" | bc -l`
		multi3[$core]=`echo "${multi3[$core]}+$(./multi3 $1 $core t | grep Tiempo | awk '{ print $2 }')" | bc -l`

	done
done


echo ""
echo "Wrapping up"
for ((core = mincores; core <= maxcores ; core += 1)); do
    echo "     $core/$maxcores"
    final="$core "
    final+=$(echo "`echo "${multi0[$core]}/${niterations}" | bc -l` ")
    final+=$(echo "`echo "${multi1[$core]}/${niterations}" | bc -l` ")
    final+=$(echo "`echo "${multi2[$core]}/${niterations}" | bc -l` ")
    final+=$(echo "`echo "${multi3[$core]}/${niterations}" | bc -l` ")


    echo $final >> $fDAT
    unset final
done



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