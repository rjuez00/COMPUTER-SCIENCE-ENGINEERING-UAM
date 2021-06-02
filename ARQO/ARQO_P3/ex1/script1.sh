# Ejemplo script, para P3 arq 2019-2020

#!/bin/bash

# inicializar variables (Ex. 1)
#N1 : 15120
#N2 : 16144


Ninicio=15120
Npaso=64
Nfinal=16144
iterations=10

fDAT=ex1/results/$iterations\_iterations.dat
fPNG=ex1/results/$iterations\_graph.png

# borrar el fichero DAT y el fichero PNG
rm -f $fDAT fPNG
mkdir ex1/results
# generar el fichero DAT vacío
touch $fDAT

echo "Running slow and fast..."

#initialize array
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	fastTime[$N]=0
	slowTime[$N]=0
done

#fill the array using as index the matrix size
for ((I = 0 ; I < iterations ; I += 1)); do
	echo "iteracion: $I"
	date
	for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
		echo "	$N"
		fastTime[$N]=`echo "${fastTime[$N]} + $(./fast $N | grep 'time' | awk '{print $3}')" | bc -l`
		slowTime[$N]=`echo "${slowTime[$N]} + $(./slow $N | grep 'time' | awk '{print $3}')" | bc -l`
	done
done

#calculate the average for each matrix size and printing it
for ((N = Ninicio ; N <= Nfinal ; N += Npaso)); do
	slowTime[$N]=`echo "${slowTime[$N]} / $iterations" | bc -l`
	fastTime[$N]=`echo "${fastTime[$N]} / $iterations" | bc -l`
	echo "$N	${slowTime[$N]}	${fastTime[$N]}" >> $fDAT
done


date
#delete the arrays because they occupy a lot of space
unset fastTime
unset slowTime
#plot the .dat
echo "Generating plot..."
# llamar a gnuplot para generar el gráfico y pasarle directamente por la entrada
# estándar el script que está entre "<< END_GNUPLOT" y "END_GNUPLOT"
gnuplot << END_GNUPLOT
set terminal png size 1500,1000
set key left top

set title "Slow-Fast Execution Time"
set ylabel "Execution Time (s)" font ", 25"
set xlabel "Matrix Size" font ", 25"
set grid
set term png
set output "$fPNG"
plot "$fDAT" using 1:2 with lines lw 2 title "slow", \
     "$fDAT" using 1:3 with lines lw 2 title "fast"
replot
quit
END_GNUPLOT
