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

    nameMSG DB "Input filename: $"
	freqMSG DB "Input frequency (assumed Hz): $"
    errorMSG DB "ERROR IN WAV GENERATION $"
    quit DB "quit"

    filenameREAD db 12, ?, 14 dup('$')
    freqREAD db 5, ?, 5 dup(?)

    wavDATA db 8000 dup(?)
    

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
        
    megaloop:
        ;new line
        mov ah, 02h
        mov dl, 13
        int 21h
        mov dl, 10
        int 21h

        ;MSG TO USER for NAME
        MOV AH,09H
        mov DX, OFFSET nameMSG
        INT 21H
        ;read from keyboard
        MOV AH, 0AH
        MOV DX, OFFSET filenameREAD
        INT 21h
        
        MOV DI, OFFSET filenameREAD[2]
        call KILL_IF_QUIT

        ;eliminates the CR from the end and changes it to 0
        MOV DI, OFFSET filenameREAD[2]
        MOV BH, BYTE PTR 0
        MOV BL, filenameREAD[1]
        MOV [DI][BX], BYTE PTR 00h

        ;new line
        mov ah, 02h
        mov dl, 13
        int 21h
        mov dl, 10
        int 21h

        ;MSG TO USER for freq
        MOV AH,09H
        mov DX, OFFSET freqMSG
        INT 21H
        ;read from keyboard
        MOV AH, 0AH
        MOV DX, OFFSET freqREAD
        INT 21h


        MOV DI, OFFSET freqREAD[2]
        CALL ASCII_to_DEC

        ;AX = frec










        ;calculate the number of turns of the freq
        MOV DX, 0
        MOV AX, 8000
        DIV BX
        MOV CX, AX ;store final result temporately in cx
        MOV AX, BX ;divide frequency between modulus to round up
        MOV BX, DX
        MOV DX, 0
        DIV BX
        CMP AX, 1
        MOV AX, CX
        JE addone ;to round up
        JMP notaddone;not round up

        addone:
            INC AX
        notaddone:
            MOV DX, 0
            MOV CX,2
            DIV CX ;would be better to shift but we need remainder
            CMP DX, 1
            JE addonetofinalburst
            jmp notaddonetofinalburst
        
        addonetofinalburst:
            MOV BL, 1
            jmp startfill
        notaddonetofinalburst:
            MOV BL, 0
        ;access to the memory was minimized as much as possible 
        ;that's why i use as much registers and no stack
        
        ;AX the length of the the burst of bytes
        ;BH flag for storing 50(00h) & -50(11h)
        ;BL add a 0 or not (1)yes
        ;CX counter from 0 to 8000
        ;DI counter from length of burst to 0
        ;SI DATA
        startfill:
            MOV SI, OFFSET wavDATA
            MOV BH, 0
            MOV CX, 0
            MOV DI, AX
        loopfill:
            CMP CX, 8000
            JE initwave
            ;writing to memory
            TEST BH, BH; IF 0 JUMP, IS FASTER THAN CMP WHICH USES SUM
            JZ fifty
                MOV [SI], BYTE PTR -50
                JMP continue
            fifty:
                MOV [SI], BYTE PTR 50
            continue:    
            ;end writing to memory

            INC cx
            INC si
            DEC di
            JE switchflag
            JMP loopfill
            switchflag:
                MOV DI, AX
                NOT BH ; SWITCHES FLAG
                TEST BH, BH
                JZ addzero
                jmp loopfill


            addzero: ;this was added to achieve the frecuency desired, if not we were left with one byte less overall and comparing it to the new material uploaded with corrected arithmetics it achieves the same
                TEST BL, BL
                JZ loopfill
                MOV [SI],BYTE PTR -50
                INC SI
                INC CX
                JMP loopfill


            







        ;init wave file
        initwave:    
        MOV DX, 8000
        MOV CX, DX
        call Init_WAV_Header
        

        ; fopen call
        MOV DI, OFFSET filenameREAD[2]
        MOV DX, DI
        call fopen
        jc error_end_fopen
        MOV BX, AX

        ;write to file
        MOV DI, OFFSET wavDATA
        call Write_WAV
        jc error_end_write_wav

        ;fclose call
        call fclose
        jc error_end_fclose

        jmp megaloop













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
    



    ;INPUT:
    ;   -DS:DI REAL MEMORY WHERE IS STORED THE ASCII
    ;OUTPUT: 
    ;   -BX: NUMBER IN DEC/BIN 
    ASCII_to_DEC proc NEAR
        PUSH AX
        PUSH CX
        PUSH DX 
        PUSH SI; i change the 4 registers and i need to leave them as they were when I return thats why i push them to stack
                ; I dont push BX because the user expects the return from it so it expects that its going to change

        ;get the length of the string 
        MOV CX, 0
        MOV DH, 13; last letter is CR (13)

        BUCLE:
            CMP BYTE PTR[DI], DH
            
            JE TRANSFORMATION
            INC DI
            INC CX
            JMP BUCLE

        TRANSFORMATION:
        MOV SI, 99
        PUSH SI

        DEC DI
        MOV SI, 1  ;in charge of multiplying the units which wont be larger than 256
        MOV BX, 10 ;used for multiplying
                ;AX will store temporal values for multiplying so don't use
        
        BUCLE2:
            MOV AH, 0
            MOV AL, [DI]
            SUB AL, 30h

            MUL SI
            PUSH AX; i use the stack because i dont have registers left to store the result

            MOV AX, SI
            MUL BX
            MOV SI, AX 


            DEC DI
            DEC CX
            JZ ADDING ;if we've reached CX = 0 that means that the word has ended
            JMP BUCLE2
        
        ADDING:

        MOV BX, 0
        ADDINGLOOP:
            POP AX
            CMP AX, 99
            JE ENDOFFUNCTION
            ADD BX, AX
            jmp ADDINGLOOP

        ENDOFFUNCTION:
        INC DI ; to leave it as we received it
        POP SI
        POP DX
        POP CX
        POP AX
        
        ret
    ASCII_to_DEC endp

    

    ;INPUT:
    ;   -DS:DI REAL MEMORY WHERE IS STORED THE ASCII
    ;   -DS variable called quit with "quit" inside
    ;OUTPUT:
    ;   -ZF: 1 if equals/0 not equals
    KILL_IF_QUIT proc NEAR
        PUSH BX
        PUSH AX
        MOV SI, OFFSET quit
        MOV BX, 4

        ifquit:
            MOV AH, BYTE PTR [DI][BX]-1
            CMP AH, BYTE PTR [SI][BX]-1
            je continueloop
            jmp notquit
            
            continueloop:
            dec bx
            je killifquit
            jmp ifquit


        killifquit:
        MOV AX, 4C00H
        INT 21H
        notquit:
        POP AX
        POP BX
        ret
    KILL_IF_QUIT endp


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

       
END INICIO 

