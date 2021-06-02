#!/bin/bash
#
#$ -S /bin/bash
#$ -o falsharing.out
#$ -cwd
#$ -j y

# Anadir valgrind, gnuplot y lstopo al path
export PATH=$PATH:/share/apps/tools/valgrind/bin:/share/apps/tools/gnuplot/bin:/share/apps/tools/hwloc/bin/lstopo
# Indicar ruta librerías valgrind
export VALGRIND_LIB=/share/apps/tools/valgrind/lib/valgrind
# Pasamos el nombre del script como parámetro


#!/bin/bash
iterations=10


hola=0
for ((N = 1 ; N <= iterations ; N += 1)); do

    temp=$($1 $2| tail -n 1 | awk '{ print $2 }')
    hola=`echo "$temp + $hola" | bc -l`
done

echo `echo "$hola/$iterations" | bc -l`