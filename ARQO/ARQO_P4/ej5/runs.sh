iterations=1
fDAT=ej5/results.dat
touch $fDAT

files=("SD.jpg" "HD.jpg" "FHD.jpg" "4k.jpg" "8k.jpg")

for ((N = 0 ; N < ${#files[@]} ; N += 1)); do
    fast[$N]=0
    slow[$N]=0
done


for ((N = 1; N <= iterations ; N += 1)); do
    for ((uwu = 0 ; uwu < ${#files[@]} ; uwu += 1)); do
        fast[$uwu]=`echo "${fast[$uwu]} + $(./edgeDetector resources/${files[$uwu]} | grep Tiempo | awk '{ print $2 }')" | bc -l`
        slow[$uwu]=`echo "${fast[$uwu]} + $(./edgeDetector_backup_og resources/${files[$uwu]} | grep Tiempo | awk '{ print $2 }')" | bc -l`
    done
done

for ((N = 0 ; N < ${#files[@]} ; N += 1)); do
    temp1=`echo "${slow[$N]}/$iterations" | bc -l `
    temp2=`echo "${fast[$N]}/$iterations" | bc -l `

    echo ${files[$N]}": " $temp1 $temp2 >> $fDAT
done