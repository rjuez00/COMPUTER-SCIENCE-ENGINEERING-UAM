# calculate speedup

#!/bin/bash
cat $1 | awk -v total=$(cat $1 | head -n 1 | wc -w) '{ printf $1; for (i=3;i<=total;i++) {printf " " $2/$i} print " "} ' > ej2/results/speedup.dat