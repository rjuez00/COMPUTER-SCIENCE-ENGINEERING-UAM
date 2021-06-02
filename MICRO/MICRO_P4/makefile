all: p4a.com p4b.exe p4c.exe

p4a.com: p4a.obj
	tlink /t p4a
p4a.obj: p4a.asm
	tasm /zi p4a.asm

p4b.exe: p4b.obj
	tlink /v p4b
p4b.obj: p4b.asm
	tasm /zi p4b.asm

p4c.exe: p4c.obj
	tlink /v p4c
p4c.obj: p4c.asm
	tasm /zi p4c.asm


clean:
	del *.obj
	del *.com
	del *.MAP
	del *.exe 
