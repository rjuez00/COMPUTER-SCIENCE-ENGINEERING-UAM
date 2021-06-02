LIBS = -lm
LIB_DIR =  
FLAGS = -g -lgomp -lm -Wall -D_GNU_SOURCE -fopenmp -O3
FOLDER=source

.PHONY: clean all

all: multi0 multi1 multi2 multi3 omp1 omp2 pescalar_par1 pescalar_par2 pescalar_par3 pescalar_par3_forscript pescalar_serie pescalar_serie_forscript edgeDetector edgeDetector_backup_og edgeDetector_backup pi_par1 pi_par2 pi_par3 pi_par4 pi_par5 pi_par6 pi_par7 pi_serie

speedtest:
	./edgeDetector_backup resources/8k.jpg
	./edgeDetector resources/8k.jpg


multi0: source/multi0.c source/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

multi1: source/multi1.c source/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

multi2: source/multi2.c source/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)
	
multi3: source/multi3.c source/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

omp1: $(FOLDER)/omp1.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

omp2: $(FOLDER)/omp2.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

pescalar_serie: $(FOLDER)/pescalar_serie.c $(FOLDER)/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

pescalar_par1: $(FOLDER)/pescalar_par1.c $(FOLDER)/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

pescalar_par2: $(FOLDER)/pescalar_par2.c $(FOLDER)/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

pescalar_par3: $(FOLDER)/pescalar_par3.c $(FOLDER)/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

pescalar_par3_forscript: $(FOLDER)/pescalar_par3_forscript.c $(FOLDER)/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

pescalar_serie_forscript: $(FOLDER)/pescalar_serie_forscript.c $(FOLDER)/arqo4.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

edgeDetector: $(FOLDER)/edgeDetector.c $(FOLDER)/stb_image_write.h $(FOLDER)/stb_image.h
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/edgeDetector.c $(LIBS)

edgeDetector_backup: $(FOLDER)/edgeDetector_backup.c $(FOLDER)/stb_image_write.h $(FOLDER)/stb_image.h
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/edgeDetector_backup.c $(LIBS)

edgeDetector_backup_og: $(FOLDER)/edgeDetector_backup_og.c $(FOLDER)/stb_image_write.h $(FOLDER)/stb_image.h
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/edgeDetector_backup_og.c $(LIBS)

pi_par1: $(FOLDER)/pi_par1.c
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/pi_par1.c $(LIBS)

pi_par2: $(FOLDER)/pi_par2.c
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/pi_par2.c $(LIBS)
	
pi_par3: $(FOLDER)/pi_par3.c
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/pi_par3.c $(LIBS)

pi_par4: $(FOLDER)/pi_par4.c
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/pi_par4.c $(LIBS)
	
pi_par5: $(FOLDER)/pi_par5.c
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/pi_par5.c $(LIBS)
	
pi_par6: $(FOLDER)/pi_par6.c
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/pi_par6.c $(LIBS)
	
pi_par7: $(FOLDER)/pi_par7.c
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/pi_par7.c $(LIBS)

pi_serie: $(FOLDER)/pi_serie.c
	gcc $(FLAGS) -std=gnu99 $(LIB_DIR) -o $@ $(FOLDER)/pi_serie.c $(LIBS)



stb_image.h:
	@echo "Los ficheros de cabecera de stb se deberían descarga automáticamente"
	@echo "En caso de fallo, descargadlo de https://raw.githubusercontent.com/nothings/stb/master/stb_image.h"
	wget --no-check-certificate https://raw.githubusercontent.com/nothings/stb/master/stb_image.h

stb_image_write.h:
	@echo "Los ficheros de cabecera de stb se deberían descarga automáticamente"
	@echo "En caso de fallo, descargadlo de https://raw.githubusercontent.com/nothings/stb/master/stb_image_write.h"
	wget --no-check-certificate https://raw.githubusercontent.com/nothings/stb/master/stb_image_write.h

clean:
	rm -f *.o *~ omp1 omp2 pescalar_serie pescalar_par1 pescalar_par2 pescalar_par3 pescalar_par3_forscript pescalar_serie_forscript edgeDetector multi1 multi2 multi3 multiTest multi0 pi_par1 pi_par2 pi_par3 pi_par4 pi_par5 pi_par6 pi_par7 pi_serie edgeDetector_backup_og edgeDetector_backup
	
clean_resources:
	rm -rf resources/*_grad_denoised.jpg resources/*grad.jpg resources/*_grey.jpg

clear:
	rm -f *.o *~

ex0:
	bash ej0/ej0.sh

pack_and_send: zip send

zip:
	(cd .. ; zip -r ARQO_P4/allfiles.zip ARQO_P4 -x '*.git*' )
	clear

send:
	@echo GzpnbjZ
	scp allfiles.zip arqo47@150.244.56.153:

connect:
	@echo GzpnbjZ
	ssh -X arqo47@150.244.56.153
ej0:
	bash ej0/ej0.sh

ej2:
	bash ej2/threads.sh
	bash ej2/calculatespeedup.sh ej2/results/resultados24.dat
	bash ej2/plotting.sh



ej3tabla1:
	bash ej3/ej3.sh 1000

ej3tabla2:
	bash ej3/ej3.sh 2000

ej3plotting:
	bash ej3/computeplotting.sh

ej5run:
	bash ej5/runs.sh

