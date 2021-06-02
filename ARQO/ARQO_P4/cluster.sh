#!/bin/bash
#
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -pe openmp 12

# Anadir valgrind, gnuplot y lstopo al path
export PATH=$PATH:/share/apps/tools/valgrind/bin:/share/apps/tools/gnuplot/bin:/share/apps/tools/hwloc/bin/lstopo
# Indicar ruta librerías valgrind
export VALGRIND_LIB=/share/apps/tools/valgrind/lib/valgrind
# Pasamos el nombre del script como parámetro


#!/bin/bash
make $1