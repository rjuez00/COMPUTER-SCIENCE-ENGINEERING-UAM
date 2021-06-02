;@author Rodrigo Juez Hernández
;@author S. Xiao Fernández Marín


;**************************************************************************
; ASSEMBLY CODE STRUCTURE EXAMPLE. MBS 2020
;**************************************************************************
; DATA SEGMENT DEFINITION
extrn Init_WAV_Header:FAR
extrn fopen:FAR
extrn fclose:FAR
extrn fread:FAR
extrn Write_WAV:FAR
extrn Read_WAV:FAR

DATOS SEGMENT

	filename DB "gen_la.wav", 0
    ; We added more bytes to fill the null ones that appeared if we use only 440
    sound db 445 dup(9 dup(50), 9 dup(-50))

	errorfopenMSG DB "Error in fopen: $"
    errorwritewavMSG DB "Error in Write_WAV: $"
   	errorfcloseMSG DB "Error in fclose: $"
    errorcodeMSG DB 2 dup('$'), '$'

DATOS ENDS


PILA SEGMENT STACK "STACK"
	DB 40H DUP (0) ; initialization example, 64 bytes set to 0
PILA ENDS



CODE SEGMENT
	ASSUME CS: CODE, DS: DATOS, SS: PILA

   	; BEGINNING OF THE MAIN PROCEDURE
	INICIO PROC
    
    ; INIT OF SEGMENTS
    MOV AX, DATOS
    MOV DS, AX
    
    ;init wave file
    MOV DX, 8000
    MOV CX, DX
    call Init_WAV_Header
    ; generation of 440hz signal
     

    ; fopen call
    MOV DX, OFFSET filename
    call fopen
    jc error_end_fopen
    MOV BX, AX

    ;write to file
    MOV DI, OFFSET sound
    call Write_WAV
    jc error_end_write_wav

    ;fclose call
    call fclose
    jc error_end_fclose


    endcall:
    	MOV AX, 4C00H
	    INT 21H
    
    
    error_end_fopen:
        MOV DI, OFFSET errorcodeMSG
        CALL DEC_to_ASCII
     ; NEWLINE
        mov ah, 02h
        mov dl, 13
        int 21h
        mov dl, 10
        int 21h
    ;MSG TO USER for NAME
        MOV AH,09H
        mov DX, OFFSET errorfopenMSG
        INT 21H
    ;MSG TO USER for NAME
        MOV AH,09H
        mov DX, OFFSET errorcodeMSG
        INT 21H
    ;kill
        jmp endcall
    


    error_end_fclose:
        MOV DI, OFFSET errorcodeMSG
        CALL DEC_to_ASCII
     ; NEWLINE
        mov ah, 02h
        mov dl, 13
        int 21h
        mov dl, 10
        int 21h
    ;MSG TO USER for NAME
        MOV AH,09H
        mov DX, OFFSET errorfcloseMSG
        INT 21H
    ;MSG TO USER for NAME
        MOV AH,09H
        mov DX, OFFSET errorcodeMSG
        INT 21H
    ;kill
        jmp endcall





    error_end_write_wav:
        call fclose
        MOV DI, OFFSET errorcodeMSG
        CALL DEC_to_ASCII
     ; NEWLINE
        mov ah, 02h
        mov dl, 13
        int 21h
        mov dl, 10
        int 21h
    ;MSG TO USER for NAME
        MOV AH,09H
        mov DX, OFFSET errorwritewavMSG
        INT 21H
    ;MSG TO USER for NAME
        MOV AH,09H
        mov DX, OFFSET errorcodeMSG
        INT 21H
    ;kill
        jmp endcall

	INICIO ENDP
	



    ;INPUT 
	;	-AX: NUMBER TO CONVERT
	;	-DS:DI ADRESS TO STORE ASCII
	;OUTPUT:
	;	-DS:DI ADRESS WHERE ASCII IS STORED
    DEC_to_ASCII proc NEAR
		PUSH AX
		PUSH BX
		PUSH CX
		PUSH DX
		PUSH DI
		;CONVERSIOn BX=10; CX=COUNTER IN MEMORY; DI=ADDRESS AX: NUMBER TO CONVERT; DX INTERMEDIATE DIGIT
			MOV BX, 10
			MOV CX, 0
			tyrell:
				MOV DX, 0
				INC CX
				DIV BX
				PUSH DX
				TEST AX, AX
				JE tomemory
				jmp tyrell
			tomemory:
			wallace:
				POP DX
				ADD DX, 30h
				MOV BYTE PTR [DI], DL
				INC DI
				DEC CX
				JE finishhim
				jmp wallace

		finishhim:
			POP DI
			POP DX
			POP CX
			POP BX
			POP AX
		ret
	DEC_to_ASCII endp
	CODE ENDS
	; END OF PROGRAM. OBS: INCLUDES THE ENTRY OR THE FIRST PROCEDURE (i.e. “INICIO”)
END INICIO 