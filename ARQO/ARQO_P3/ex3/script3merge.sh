iterations=2

fDATcache=ex3/results/cache.dat
fDATtime=ex3/results/time.dat
fDATfinal=ex3/results/final.dat

#paste prints all the information together and I reorder it with awk
paste $fDATcache $fDATtime | awk '{ print $1 OFS $7 OFS $2 OFS $3 OFS $8 OFS $4 OFS $5 }' > $fDATfinal

rm $fDATcache
rm $fDATtime