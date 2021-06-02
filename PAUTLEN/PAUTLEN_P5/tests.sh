EXE="alfa"
SRCFOLDER="casos_prueba_alumnos"
NASMFOLDER="nasmoutput"

mkdir -p $NASMFOLDER
sources=($(ls -d $SRCFOLDER/*.alf))

for source in "${sources[@]}"
do
    name=$(echo $source | awk '{ print substr( $0,22, length($0)-25 ) }')
    echo "Compilando $name..."
    outputfile=$NASMFOLDER/$name.asm

    ./$EXE $source $outputfile
    
    echo "-------------------"
done