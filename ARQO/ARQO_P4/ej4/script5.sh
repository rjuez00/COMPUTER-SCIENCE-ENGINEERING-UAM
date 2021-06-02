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
iterations=3
sizes=(1 2 4 6 7 8 9 10 12)


for i in "${sizes[@]}"; do   
    results[$i]=0
done

hola=0
for ((N = 1 ; N <= iterations ; N += 1)); do
    for i in "${sizes[@]}"; do   
        temp=$(./pi_par3 $i| tail -n 1 | awk '{ print $2 }')
        results[$i]=`echo "${results[$i]} + $temp" | bc -l`
    done
done



for i in "${sizes[@]}"; do   
    echo "$i `echo "${results[$i]}/$iterations" | bc -l`"
done

