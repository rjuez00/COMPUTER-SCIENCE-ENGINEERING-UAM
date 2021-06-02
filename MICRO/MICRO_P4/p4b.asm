;@author Rodrigo Juez Hernández
;@author S. Xiao Fernández Marín



DATOS SEGMENT
    directiveREAD db 2, ?, 2 dup('$')
    directiveMSG db "DEC_2_HEX(1) or HEX_2_DEC(other): ", "$"
    select db "Write a number: $"

    origenHEX db 5, ?, 5 dup('$')
    origenDEC db 6, ?, 6 dup('$')
    dest db 6 dup(?)

DATOS ENDS


PILA SEGMENT STACK "STACK"
	DB 40H DUP (0) ; initialization example, 64 bytes set to 0
PILA ENDS



CODE SEGMENT
	ASSUME CS: CODE, DS: DATOS, SS: PILA

   	; BEGINNING OF THE MAIN PROCEDURE
	INICIO PROC
        MOV AX, 0
        MOV ES, AX
        CMP WORD PTR ES:[55h*4 +2], 0
        JZ reallyend

    	;INIT OF SEGMENTS
		MOV AX, DATOS
		MOV DS, AX

		MOV AH,09H
		mov DX, OFFSET directiveMSG 
		INT 21H

		MOV AH, 0AH
		MOV DX, OFFSET directiveREAD ;read which conversion to do
		INT 21h
        
        
      
        ; NEWLINE
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h

        CMP BYTE PTR directiveREAD[2], 31h ;check which conversion user typed
        JZ DEC_2_HEX
        
        MOV AH, 0AH
		MOV DX, OFFSET origenHEX ;conversion hex_dec 
		INT 21h ;ask for input
        MOV BL, BYTE PTR origenHEX[1]
        MOV BH, 0
        MOV origenHEX[2][BX], "$" ;setting a $ at the end
        MOV AH, 11h
        MOV CX, OFFSET origenHEX[2] 
        MOV DX, OFFSET dest ;setting the destination and origin for the interruption
        INT 55h
        jmp endfunc


        
    DEC_2_HEX:


        MOV AH, 0AH
		MOV DX, OFFSET origenDEC
		INT 21h ;ask for input
        MOV BL, BYTE PTR origenDEC[1]
        MOV BH, 0
        MOV origenDEC[2][BX], "$" ;setting a $ at the end
        MOV AH, 10h
        MOV CX, OFFSET origenDEC[2]
        MOV DX, OFFSET dest ;setting destination and origin for function
        INT 55h


    endfunc:
    ; NEWLINE
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
        MOV AH,09H
		mov DX, OFFSET dest ;printing result
		INT 21H
    reallyend:

    	MOV AX, 4C00H
		INT 21H
		
	INICIO ENDP


	CODE ENDS
END INICIO 