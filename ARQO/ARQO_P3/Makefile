LIBS = 
LIB_DIR =  
FLAGS = -O3 -Wall -D_GNU_SOURCE

.PHONY: clean all ex1 ex2 ex3 ex4

all: fast slow multi

fast: source/fast.c source/arqo3.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

slow: source/slow.c source/arqo3.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)

multi: source/multi.c source/arqo3.c
	gcc $(FLAGS) $(LIB_DIR) -o $@ $^ $(LIBS)



clean:
	rm -f *.o *~ fast slow multi allfiles.zip

clean_results:
	rm -R ex1/results ex2/results ex3/results

pack_and_send: zip send

zip:
	(cd .. ; zip -r ARQO_P3/allfiles.zip ARQO_P3 -x '*.git*' )
	clear

send:
	@echo GzpnbjZ
	scp allfiles.zip arqo47@150.244.56.153:

connect:
	@echo GzpnbjZ
	ssh -X arqo47@150.244.56.153

ex1:
	bash ex1/script1.sh

ex2:
	bash ex2/script2.sh

ex3cache:
	bash ex3/script3cache.sh

ex3time:
	bash ex3/script3time.sh

ex3merge:
	bash ex3/script3merge.sh

ex3plot:
	bash ex3/script3plot.sh

ex3:
	bash ex3/script3og.sh

ex44:
	bash ex4/script4.sh

ex45:
	bash ex4/script5.sh

ex46:
	bash ex4/script6.sh