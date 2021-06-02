# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash


Ninicio=514
Npaso=64
Nfinal=1538
niterations=5


fDAT=ej3/resultados/resultados_plotting_$Nfinal.dat

rm -rf $fDAT
touch $fDAT

for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
    multi0[$N]=0
    multi3[$N]=0
done


for ((iterations = 1 ; iterations <= niterations ; iterations = iterations +1)); do
    echo "$iterations/$niterations"
	for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
        echo "  $N/$Nfinal"
   		multi0[$N]=`echo "${multi0[$N]}+$(./multi0 $N t | grep Tiempo | awk '{ print $2 }')" | bc -l`
		multi3[$N]=`echo "${multi3[$N]}+$(./multi3 $N 12 t | grep Tiempo | awk '{ print $2 }')" | bc -l`

	done
done


echo ""
echo "Wrapping up"
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
    echo "     $N/$maxcores"
    final="$N "
    final+=$(echo "`echo "${multi0[$N]}/${niterations}" | bc -l` ")
    final+=$(echo "`echo "${multi3[$N]}/${niterations}" | bc -l` ")


    echo $final >> $fDAT
    unset final
done



: '
fPNG_og=ej3/plot
fDAT=resultados_plotting_100.dat
fPNGt=$fPNG_o\_time.png
fPNGs=$fPNG_og\_speedup.png

echo "Generating plots..."
#system('ls -1B') obtains all the files we want to plot
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top
set title "Time needdd for matrix multiplication"
set ylabel "Seconds" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNGr"
set key samplen 2 spacing 1.0 font ", 20"
plot "$fDAT" using 1:2 with lines lw 2 title "serie",\
	 "$fDAT" using 1:3 with lines lw 2 title "parallel"
						
replot
quit
END_GNUPLOT'