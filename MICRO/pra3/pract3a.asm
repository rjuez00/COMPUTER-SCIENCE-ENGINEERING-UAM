;**************************************************************************
;* BASIC ASSEMBLY PROGRAM STRUCTURE EXAMPLE to use with C code link
;* SBM / MBS 2020
;*
;**************************************************************************


; CODE SEGMENT DEFINITION
_TEXT SEGMENT BYTE PUBLIC 'CODE'
ASSUME CS: _TEXT, 


PUBLIC _calculaMediana  ; example for the first function
_calculaMediana PROC FAR 

PUSH BP
MOV BP, SP
; Push the registered used 
; Recover the data from stack , BP+6, etc (integers, pointers, etc)
; fill in with the required instructions
; return the result in AX if needed.
; pop the used registers
PUSH DX
PUSH CX
PUSH BX

MOV AX, [bp + 6]
MOV BX, [bp + 8]
MOV CX, [bp + 10]
MOV DX, [bp + 12]

ordenamayor:
CMP AX, BX  
JS axmayor
jmp comparabxcx
axmayor:
xchg ax, bx

comparabxcx:
CMP BX, CX
JS bxmayor
jmp comparacxdx
bxmayor:
xchg bx, cx

comparacxdx:
CMP cx, dx
JS cxmayor
jmp ordenamenor
cxmayor:
xchg cx, dx

ordenamenor:
CMP BX, CX  
JS bxmayor2
jmp comparaaxbx2
bxmayor2:
xchg bx, cx

comparaaxbx2:
CMP AX, BX  
JS axmayor2
jmp termina
axmayor2:
xchg ax, bx
jmp termina


termina:
MOV AX, CX
ADD AX, BX

MOV BX, 2 ;divide by 2
MOV DX, 0 ;compare to 0
CMP AX, DX
JS negativo

DIV BX
jmp terminarfuncion

negativo:
MOV DX, -1
IDIV BX


MOV AX, DX
terminarfuncion:
POP BX
POP CX
POP DX
POP BP	;BP restored

RET

_calculaMediana ENDP





PUBLIC _calculaLetraDNI  ; example for the first function
_calculaLetraDNI PROC FAR 


RET
_calculaLetraDNI ENDP

PUBLIC _enteroACadenaHexa  ; example for the first function
_enteroACadenaHexa PROC FAR 

PUSH BP
MOV BP, SP

;PUSH REGISTERS!!!!!!!
PUSH AX
PUSH DS
PUSH DI
PUSH BX
PUSH CX
PUSH DX

MOV AX, [bp + 6] ;number to convert
LDS DI, [bp + 8] ;string
MOV CL, 4
MOV DX, 9

MOV BX, AX
AND BX, 0F000h
SHR BH, CL

CMP DL, BH
JS transformletter
ADD BH, 30h
JMP continue
transformletter:
ADD BH, 55
continue:

MOV BYTE PTR [DI], BH
INC DI

MOV BX, AX
AND BX, 0F00h

CMP DL, BH
JS transformletter2
ADD BH, 30h
JMP continue2
transformletter2:
ADD BH, 55
continue2:

MOV BYTE PTR [DI], BH
INC DI

MOV BX, AX
AND BX, 00F0h
SHR BL, CL

CMP DL, BL
JS transformletter3
ADD BL, 30h
JMP continue3
transformletter3:
ADD BL, 55
continue3:

MOV BYTE PTR [DI], BL
INC DI


MOV BX, AX
AND BX, 000Fh

CMP DL, BL
JS transformletter4
ADD BL, 30h
JMP continue4
transformletter4:
ADD BL, 55
continue4:

MOV BYTE PTR [DI], BL
INC DI

MOV BYTE PTR [DI], 0

POP DX
POP CX
POP BX
POP DI
POP DS
POP AX
POP BP
RET 
_enteroACadenaHexa ENDP

_TEXT ENDS

END
