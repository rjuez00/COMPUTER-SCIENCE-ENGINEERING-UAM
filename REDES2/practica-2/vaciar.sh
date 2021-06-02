MAIN=securebox.py

python3 $MAIN --list_files | grep 'fileID' | awk '{print $2}' | cut -c2-9 | while read line; do
echo "eliminando $line"
python3 $MAIN --delete_file $line
done

echo "comprobando remanente"
python3 $MAIN --list_files