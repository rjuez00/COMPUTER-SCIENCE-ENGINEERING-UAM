;@author Rodrigo Juez Hernández
;@author S. Xiao Fernández Marín



DATOS SEGMENT
    dest db 6 dup(?)
    flagfinished db 0
    noinstallMSG db "Please install the interruption 55h and 1Ch$"
    hexdecMSG db "use: hex/dec NUMBER$"
    directiveMSG db "hex/dec NUMBER: $"
    directiveREAD db 10, ?, 10 dup('$')

    origenHEX db 5, ?, 5 dup('$')
    origenDEC db 6, ?, 6 dup('$')
DATOS ENDS


PILA SEGMENT STACK "STACK"
	DB 40H DUP (0) ; initialization example, 64 bytes set to 0
PILA ENDS



CODE SEGMENT
	ASSUME CS: CODE, DS: DATOS, SS: PILA

   	; BEGINNING OF THE MAIN PROCEDURE
	INICIO PROC
    ;INIT OF SEGMENTS
		MOV AX, DATOS
		MOV DS, AX
        MOV AX, 0
        MOV ES, AX
        CMP WORD PTR ES:[55h*4 +2], 0 ;checks if interruptions are installed if not finishes 
        JZ noinstall ;obviously is not a full check but the user is supposed to have it installed
        JMP iniciar

    noinstall:
        MOV AH,09H
		mov DX, OFFSET noinstallMSG 
		INT 21H
        JMP reallyend

    hexdecerror:
        MOV AH, 09H
        mov DX, OFFSET hexdecMSG
        INT 21h
        ;NEWLINE
        mov ah, 02h
        mov dl, 13
        int 21h
        mov dl, 10
        int 21h
        JMP iniciar

    iniciar:
    	MOV AH,09H
		mov DX, OFFSET directiveMSG 
		INT 21H

		MOV AH, 0AH
		MOV DX, OFFSET directiveREAD ;read which conversion to do
		INT 21h
        
        MOV BX, OFFSET directiveREAD ;where the number will be stored
        CALL HEX_OR_DEC_OR_QUIT ;calls function which parses what user has typed including the number
        CMP AX, -1
        JZ hexdecerror
        CMP AX, 2 ;act accordingly
        JZ reallyend
        TEST AX, AX
        JZ hex_2_dec
        JMP dec_2_hex


    hex_2_dec:
        MOV BL, BYTE PTR directiveREAD[1] ;gets length to set $ at the end
        MOV BH, 0
        MOV directiveREAD[2][BX], "$" ;setting a $ at the end because specified in interuption
        MOV AH, 11h
        MOV CX, OFFSET directiveREAD[6] ;says where is the input
        MOV DX, OFFSET dest ;setting destination and origin for function
        INT 55h ;calls interruption
        JMP startprint




    dec_2_hex:
        MOV BL, BYTE PTR directiveREAD[1] ;gets length to set $ at the end
        MOV BH, 0
        MOV directiveREAD[2][BX], "$" ;setting a $ at the end
        MOV AH, 10h
        MOV CX, OFFSET directiveREAD[6] ;sets input
        MOV DX, OFFSET dest ;setting destination and origin for function
        INT 55h ;calls interruption
        JMP startprint



   startprint: 
    ; NEWLINE
	mov ah, 02h
	mov dl, 13
	int 21h
	mov dl, 10
	int 21h
    
   
    mov ax, 0
    mov es, ax
    mov bx, word ptr es:[1Ch*4+2] ;gets segment in which startflag and parameter inputs are stored
    mov es, bx
    mov word ptr es:[031Eh], DS ;writes segment on input
    mov word ptr es:[0320], OFFSET dest ;writes offset on input
    mov byte ptr es:[031Dh], 0FFh ;writes FF which tells interruption to start printing 
    
    print:
        CMP byte ptr es:[031Dh], 00h ;wait until the startflag is 00 which means printing has finished
        JNZ print
      
    aightimmaheadout:
        ; NEWLINE
        mov ah, 02h
        mov dl, 13
        int 21h
        mov dl, 10
        int 21h
        
        MOV flagfinished, 0 ; restarts whole process
        MOV CX, 0000h
        JMP iniciar
    
    reallyend:
        MOV AX, 4C00H ;user has typed quit or interruption is not installed
		INT 21H

		
	INICIO ENDP

    ;DS:BX READ FROM USER
    ;AX: 0(DEC) 1(HEX) -1(NONE) 2(quit)
    HEX_OR_DEC_OR_QUIT PROC
        CMP BYTE PTR 2[BX], "q"
        JZ checkquit
        CMP BYTE PTR 1[BX], 5
        JB errorend
        CMP BYTE PTR 2[BX], "h"
        JZ checkhex
        CMP BYTE PTR 2[BX], "d"
        JZ checkdec
        
    errorend:
        MOV AX, -1
        RET 
          

    checkhex:
        CMP BYTE PTR 3[BX], "e"
        JNZ errorend
        CMP BYTE PTR 4[BX], "x"
        JNZ errorend
        MOV AX,1 
        RET

    checkdec:
        CMP BYTE PTR 3[BX], "e"
        JNZ errorend
        CMP BYTE PTR 4[BX], "c"
        JNZ errorend
        MOV AX, 0
        RET
    
    checkquit:
        CMP BYTE PTR 3[BX], "u"
        JNZ errorend
        CMP BYTE PTR 4[BX], "i"
        JNZ errorend
        CMP BYTE PTR 5[BX], "t"
        JNZ errorend
        MOV AX, 2
        RET

    HEX_OR_DEC_OR_QUIT ENDP

	CODE ENDS
END INICIO 