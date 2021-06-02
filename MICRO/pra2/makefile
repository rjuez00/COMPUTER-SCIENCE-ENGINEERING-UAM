all: clean ls2a.exe ls2b.exe ls2c.exe

ls2a.exe: ls2a.obj
	tlink /v ls2a wav

ls2a.obj: ls2a.asm
	tasm /zi ls2a.asm

ls2b.exe: ls2b.obj
	tlink /v ls2b wav

ls2b.obj: ls2c.asm
	tasm /zi ls2b.asm

ls2c.exe: ls2c.obj
	tlink /v ls2c wav

ls2c.obj: ls2c.asm
	tasm /zi ls2c.asm





clean:
	del *.MAP
	del LS2A.OBJ
	del LS2A.EXE
	del LS2B.OBJ
	del LS2B.EXE
	del LS2C.OBJ
	del LS2C.EXE
