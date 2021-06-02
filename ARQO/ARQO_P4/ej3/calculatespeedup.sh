# calculate speedup

#!/bin/bash
cat $1 | awk  '{ print $1 " " $2/$3 }'  > ej3/resultados/speedup.dat