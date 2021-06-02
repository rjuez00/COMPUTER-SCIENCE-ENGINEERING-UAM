#!/bin/bash
#
#$ -S /bin/bash
#$ -cwd
#$ -j y

# Anadir valgrind y gnuplot al path
export PATH=$PATH:/share/apps/tools/valgrind/bin:/share/apps/tools/gnuplot/bin
# Indicar ruta librerías valgrind
export VALGRIND_LIB=/share/apps/tools/valgrind/lib/valgrind
# Pasamos el nombre del script como parámetro


#!/bin/bash
cat /proc/cpuinfo
#this script is to obtain the information from the AMD cluster we've been using
echo "________________"
dmidecode

echo "_______________ "

getconf -a | grep -i cache

