echo prueba1:
	./pruebaSintactico pruebas_2019_2020/entrada_sin_1.txt misalida_sin_1.txt
	diff -bB pruebas_2019_2020/salida_sin_1.txt misalida_sin_1.txt

echo prueba2:
	./pruebaSintactico pruebas_2019_2020/entrada_sin_2.txt misalida_sin_2.txt
	diff -bB pruebas_2019_2020/salida_sin_2.txt misalida_sin_2.txt

echo prueba3:
	./pruebaSintactico pruebas_2019_2020/entrada_sin_3.txt misalida_sin_3.txt
	diff -bB pruebas_2019_2020/salida_sin_3.txt misalida_sin_3.txt