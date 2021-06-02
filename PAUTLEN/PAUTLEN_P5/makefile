CC=gcc
CFLAGS=-Wall -g
#MINI = mini mini2 mini3 mini4 mini5 mini6 mini7 mini8 mini9 factorial condicionales vectores fibonacci funciones_vectores funciones
#ERR = err1 err2 err3 err4 err5 err6 err7 err8 err9 err10 err11 err12 err13 err14 err15 err16
EXE = alfa #$(MINI)
ALL_BIN = bin/aritmeticas1 bin/aritmeticas2 bin/comparaciones bin/funciones1 bin/funciones2 bin/funciones3 bin/funciones4 bin/if1 bin/if2 bin/if3 bin/logicas1 bin/logicas2 bin/vectores1 bin/vectores2 bin/vectores3 bin/vectores4 bin/while
all: $(EXE) generatenasm

exec_all: clean all generatebins exec_bins

generatebins: $(ALL_BIN)

alfa: alfa.c lex.yy.o y.tab.o generacion.o SymbolTable.o hash.o
	$(CC) $(CFLAGS) $^ -o $@

generacion.o: generacion.c generacion.h
	$(CC) $(CFLAGS) -c $<

SymbolTable.o: SymbolTable.c SymbolTable.h
	$(CC) $(CFLAGS) -c $<

hash.o: hash.c hash.h
	$(CC) $(CFLAGS) -c $<

lex.yy.o: lex.yy.c
	$(CC) $(CFLAGS) -c $^

y.tab.o: y.tab.c
	$(CC) $(CFLAGS) -c $<

lex.yy.c: alfa.l y.tab.h
	flex $<

y.tab.c: alfa.y
	bison -d -y -v $^

y.tab.h: alfa.y
	bison -d -y -v $^

alfa.c:
	@echo "Make does weird things." > /dev/null

.PHONY: clean
megaclean: clean cleanasm cleanbin

clean:
	rm -rf alfa lex.yy.* y.tab.* y.output *.asm
	rm -f generacion.o hash.o lex.yy.o SymbolTable.o y.tab.o

cleanasm:
	rm -r nasmoutput

cleanbin:
	rm -f bin/*

bin/%: nasmoutput/%.o
	gcc -m32 -o $@ $^ alfalib.o

nasmoutput/%.o: nasmoutput/%.asm
	nasm -felf32 $^ -o $@

generatenasm:
	bash tests.sh
