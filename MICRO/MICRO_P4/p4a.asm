;@author Rodrigo Juez Hernández
;@author S. Xiao Fernández Marín



CODE SEGMENT
	ASSUME CS: CODE
    ORG 256
    ;start
    init: jmp INICIO
    oldsegment dw ?
    oldoffset dw ?
    
    localcounter db 0
    secondcounter db 0
    firstimeflag db 0

    ;GLOBAL VARIABLES
    argumenterror db "Use /I or /U or none for printing status", "$"
    groupnumber db "Group Number: 2292", "$"
    programmers db "Programmers: Sofia Xiaofan Fernandez Marin & Rodrigo Juez Hernandez", "$"
    statusinstalled db "Driver Status: Installed", "$"
  	statusuninstalled db "Driver Status: Uninstalled", "$"
    
    



    ;INPUT:
        ;AX=integer tu convert
        ;DS:DI destination
    INT_to_ASCII_HEX PROC FAR 
        PUSH AX
        PUSH DS
        PUSH DI
        PUSH BX
        PUSH CX
        PUSH DX

        MOV CL, 4
        MOV DX, 9

        MOV BX, AX
        AND BX, 0F000h ;filter the first 4 bits
        SHR BH, CL ;shift them to the bottom of the BH register and we can operate with it
        
        CMP DL, BH ;check if they're bigger than 9 to change to A-F
        JS transformletter
        ADD BH, 30h ;its lower so add ascii code to 0
        JMP continue
        transformletter:
        ADD BH, 55 ;higher so add ascii code to 'A'-10
        continue:

        MOV BYTE PTR [DI], BH ;save the result
        INC DI

        MOV BX, AX
        AND BX, 0F00h ;filter the next 4 bits

        CMP DL, BH ;is it lower than 9?
        JS transformletter2
        ADD BH, 30h ;its lower so add ascii code to 0
        JMP continue2
        transformletter2:
        ADD BH, 55 ;higher so add ascii code to 'A'-10
        continue2:

        MOV BYTE PTR [DI], BH ;save the result
        INC DI

        MOV BX, AX
        AND BX, 00F0h ; filter the next 4 bits
        SHR BL, CL ; shift it so its in the bottom of BL and we can operate with it

        CMP DL, BL ; is it lower than 9?
        JS transformletter3
        ADD BL, 30h ;its lower so add ascii code to 0
        JMP continue3
        transformletter3:
        ADD BL, 55 ;higher so add ascii code to 'A'-10
        continue3:

        MOV BYTE PTR [DI], BL ;save the result
        INC DI


        MOV BX, AX
        AND BX, 000Fh ;last 4 bits

        CMP DL, BL ;is it lower than 9?
        JS transformletter4
        ADD BL, 30h ;its lower so add ascii code to 0
        JMP continue4
        transformletter4:
        ADD BL, 55 ;higher so add ascii code to 'A'-10
        continue4:

        MOV BYTE PTR [DI], BL
        INC DI

        MOV BYTE PTR [DI], 24h ;NULL signaling end of string

        POP DX
        POP CX
        POP BX
        POP DI
        POP DS
        POP AX
        
        RET 
    INT_to_ASCII_HEX ENDP

    ;INPUT
    ;   DS:DI where we have the hexadecimal number in ascii characters
    ;   AX: RETURN
    ASCII_HEX_to_INT PROC FAR
        PUSH BX
        PUSH CX
        PUSH DX 
        PUSH SI; i change the 4 registers and i need to leave them as they were when I return thats why i push them to stack
                ; I dont push BX because the user expects the return from it so it expects that its going to change

        ;get the length of the string 
        MOV CX, 0
        MOV DH, 24h ;last letter is $

        BUCLEASC:
            CMP BYTE PTR[DI], DH
            
            JE TRANSFORMATIONASC
            INC DI
            INC CX
            JMP BUCLEASC

        TRANSFORMATIONASC:
        MOV SI, 99
        PUSH SI

        DEC DI
        MOV SI, 1  ;in charge of multiplying the units which wont be larger than 256
        MOV BX, 16 ;used for multiplying
                ;AX will store temporal values for multiplying so don't use
        
        BUCLE2:
            MOV AH, 0
            MOV AL, [DI]
            CMP AL, 41h
            JB isnumber
            SUB AL, 37h
            JMP go_on

        isnumber:
            SUB AL, 30h

        go_on:
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
        MOV AX, BX
        POP SI
        POP DX
        POP CX
        POP BX
        
        ret
    ASCII_HEX_to_INT ENDP

    ;INPUT:
    ;   -DS:DI REAL MEMORY WHERE IS STORED THE ASCII
    ;OUTPUT: 
    ;   -AX: NUMBER IN DEC 
    ASCII_to_DEC proc FAR 
        PUSH BX
        PUSH CX
        PUSH DX 
        PUSH SI; i change the 4 registers and i need to leave them as they were when I return thats why i push them to stack
                ; I dont push BX because the user expects the return from it so it expects that its going to change

        ;get the length of the string 
        MOV CX, 0
        MOV DH, 24h; last letter is $

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
        
        BUCLE2ASC:
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
            JZ ADDINGASC ;if we've reached CX = 0 that means that the word has ended
            JMP BUCLE2ASC
        
        ADDINGASC:

        MOV BX, 0
        ADDINGLOOPASC:
            POP AX
            CMP AX, 99
            JE ENDOFFUNCTIONASC
            ADD BX, AX
            jmp ADDINGLOOPASC

        ENDOFFUNCTIONASC:
        INC DI ; to leave it as we received it
        MOV AX, BX

        POP SI
        POP DX
        POP CX
        POP BX
        
        ret
    ASCII_to_DEC endp

    ;INPUT 
	;	-AX: NUMBER TO CONVERT
	;	-DS:DI ADRESS TO STORE ASCII
	;OUTPUT:
	;	-DS:DI ADRESS WHERE ASCII IS STORED
    DEC_to_ASCII proc FAR
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
				PUSH DX ;divides and pushes the module for inverting it through the stack
				TEST AX, AX
				JE tomemory
				jmp tyrell
			tomemory:
			wallace:
				POP DX
				ADD DX, 30h ;obtains from stack converts to ascii
				MOV BYTE PTR [DI], DL ;stores in position of destination
				INC DI ;increases index
				DEC CX
				JE finishhim
				jmp wallace
		finishhim:
            MOV BYTE PTR [DI], 24h
			POP DI
			POP DX
			POP CX
			POP BX
			POP AX
		ret
	DEC_to_ASCII endp


    digitalstamp dw 0CACAh
    ; ==========================================================
        ;			Int 55h - Convert DEC to HEX
        ; Input:
        ; 	Ah = 10h
        ; 	DS:CX = String ASCII+$ (Decimal)
        ; Output:
        ; 	DS:DX = String ASCII+$ (hexadecimal)
        ; ==========================================================
        ;			Int 55h - Convert HEX to DEC
        ; Input:
        ; 	Ah = 11h
        ; 	DS:CX = String ASCII+$ (Hexa)
        ; Output:
        ; 	DS:DX = String ASCII+$ (Decimal)
    isr PROC FAR
        PUSH DI

        CMP AH, 10h ;if is 10h goes to dec_2_hex if 11h to hex_2_dec otherwise terminates
        JZ dec_2_hex
        CMP AH, 11h
        JZ hex_2_dec
        JMP endfunc

        dec_2_hex:
            MOV DI, CX ; first calls function from previous assigment that converts to decimal number 
            call ASCII_to_DEC ;;it is safe to use because the maximum hexadecimal number will be 4 digits
            MOV DI, DX ;we set the destination to write to pass it to the next function
            call INT_to_ASCII_HEX ;with the result of the previous funcion in ax we call the int to ascii hexadecimal converter 
            jmp endfunc

        hex_2_dec:
            MOV DI, CX
            call ASCII_HEX_to_INT ;we convert the ascii hexadecimal to an integer
            
            MOV DI, DX ;receives in ax the integer and in di the destination
            call DEC_to_ASCII ;we convert that integer to ascii


        endfunc:
            POP DI
            IRET
    isr ENDP

    startflag db 00h ;if FFh it will start
    printsegment dw 0000h ;where the caller will set the segment and the offset to print
    printoffset dw 0000h 

    ; ==========================================================
        ;			Int 1Ch - Convert DEC to HEX
        ; Input:
        ; 	DX = 0CACAh
        ;   printsegment to segment of print input
        ;   printoffset to offset of print input
        ;   startflag [1Ch*4+2]:031Dh to FFh to start
        ;   when printing is finished it will be set to 00h
        ;Output:
    isr_timer PROC FAR
        PUSH BX AX DX
        CMP cs:startflag, 0FFh ;checks if flag is set to start interrupt (FF)
        JNZ no
        CMP cs:firstimeflag, 1 ;if it starts it sets the firstime printing to 1 so that it knows for future iterations
        JNZ notfirstime ;if not continues printing
        MOV cs:firstimeflag, 0 ;its the first time so it set its to 0 so that next executions know it
        MOV cs:secondcounter, 0 ;it sets the time counter (in seconds) to 0 (i use it as an indexer too)
        MOV cs:localcounter, 0 ;this variable is used to count until 18 reached to check if a second has passed
    notfirstime:
        INC cs:localcounter ;its not the first time so increment the localcounter
        CMP cs: localcounter, 18 ;if localcounter reaches 18 a second has passed 
        JA secondpassed 
        JMP no ;a second has not passed continue
    secondpassed:
        MOV BH, 0 
        mov BL, byte ptr secondcounter
        inc secondcounter ;increments the secondcounter
        
        mov ax, cs:printsegment ;obtains segment and offset to print
        mov ds, ax
        mov si, printoffset

        mov ah, 02h
		mov dl, byte ptr ds:[bx][si] ;in bx we have the second passed since start of printing we can use it as indexer and in si the offset of the variable
        CMP dl, "$" ;if $ reached end of word
        JZ killme
		int 21h ;call interruption to print the letter as we haven't reached the end

        mov localcounter, 0
    
    no:
        POP DX AX BX
        IRET
    killme:
        POP DX AX BX
        MOV firstimeflag, 1 ;we've reached the end of the word so set to 1 the firstimeflag for next printings
        MOV cs:startflag, 00h ;and communicate with caller process setting the flag to 00h again
        IRET
    
    isr_timer ENDP
    
    private_installer_55h PROC
        mov ax, 0
        mov es, ax
        mov ax, OFFSET isr
        mov bx, CS
        cli
        mov es:[55h*4], ax ;set offset and segment of new interruption
        mov es:[55h*4+2], bx
        sti
        
        mov dx, es:[1Ch*4] ;read the previous interruption and save it to restore it later
        MOV oldoffset, dx
        mov dx, es:[1Ch*4+2]
        MOV oldsegment, dx

        mov dx, OFFSET isr_timer ;take offset of timer and segment too
        mov bx, CS
        
        in al, 21h ;take PIC0
        or al, 00000001b ;manipulate first bit(timer) to enable timer masking
        out 21h, al ;writing it to PIC0 

        mov es:[1Ch*4], dx ;set directions on table
        mov es:[1Ch*4+2], bx
       
        
        in al, 21h ;reading PIC0
        and al, 11111110b ;bit manipulation to deactivate timer masking (first bit)
        out 21h, al ;writing it to PIC0



        MOV AH,09H
		mov DX, OFFSET warninginstall ;print success
		INT 21H

        mov dx, OFFSET private_installer_55h ;stay resident until start of installer as interruption's code are before the installer
        int 27h
    private_installer_55h ENDP
    


	INICIO PROC
        MOV AL, BYTE PTR CS:[0080h] ;CHECK CUANTITY OF ARGUMENTS IF NOT CORRECT PRINT STATUS AND HOW TO USE
        CMP AL, 3
        JZ letsgo
        
    noarguments:
        MOV AH,09H
        mov DX, OFFSET groupnumber ;print groupnumber
        INT 21H
        ; NEWLINE
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
			mov ah, 09h

        MOV AH,09H
        mov DX, OFFSET programmers ;print programmers
        INT 21H
        ; NEWLINE
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
			mov ah, 09h

        MOV AH,09H
        mov DX, OFFSET argumenterror ;print how to use 
        INT 21H
        ; NEWLINE
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
			mov ah, 09h
        
        MOV AX, 0
        MOV ES, AX ;uses the segment 0 to access table of interruptions 
        MOV BX, WORD PTR ES:[55h*4 +2]
        CMP BX, 0 ;check if uninstalled by checking if segment is 0
        JZ isuninstalled
        MOV ES, BX
        MOV BX, OFFSET digitalstamp ;checks the digitalstamp saved before the isr
        MOV BX, ES:[BX]
        CMP BX, 0CACAh
        JNZ isuninstalled ;if not the stamp then other interruption is installed but not ours
        MOV AH,09H
        mov DX, OFFSET statusinstalled ;if installed
        INT 21H
        JMP endinicio 

    isuninstalled:
        MOV AH,09H
        mov DX, OFFSET statusuninstalled ;if uninstalled
        INT 21H
        JMP endinicio

    endinicio:
        MOV AX, 4C00H
		INT 21H



    letsgo:
        CMP BYTE PTR CS:[81h+1], "/" ;get arguments and check correctness
        JNZ noarguments
        CMP BYTE PTR CS:[81h+2], "I"
        JZ installer
        CMP BYTE PTR CS:[81h+2], "U"
        jz uninstaller
        JMP noarguments
    
    installer:
        call private_installer_55h  
    uninstaller:
        call uninstall_55h
        jmp endinicio


	INICIO ENDP

    
    warninginstall db "Succesfully installed$"
    warninguninstall db "Succesfully uninstalled$"
    uninstall_55h proc
        push ax bx cx ds es
        mov cx, 0
        mov ds, cx
        CMP WORD PTR ds:[55h*4+2], 0
        JZ no1c
        
        mov cx, 0
        mov ds, cx

        mov dx, ds:[1Ch*4 +2]
        mov es, dx
        mov bx, OFFSET oldoffset ;retrieves old offset and segment from the resident code if not the timer wont work and it will crash
        mov dx, es:[bx]
               
        mov bx, OFFSET oldsegment
        mov bx, es:[bx]

        in al, 21h ;same as install reads PIC0 enables timer mask and writes it 
        or al, 00000001b
        out 21h, al

        mov ds:[1Ch*4], dx ;set old procedure in  table
        mov ds:[1Ch*4+2], bx
       
        in al, 21h ;same as install reads PIC0 disables timer mask and writes it 
        and al, 11111110b
        out 21h, al

        mov es, ds:[55h*4 +2] ;read isr segment
        mov bx, es:[2Ch] ;read segment of enviroment
        mov ah, 49h 
        int 21h ;release isrs
        mov es, bx
        int 21h ;release segment of enviroment variables


        cli
        mov ds:[55h*4], cx ;set to 0 entries on table
        mov ds:[55h*4 +2], cx
        sti

    no1c:
 
        pop es ds cx bx ax
        MOV AH,09H
		mov DX, OFFSET warninguninstall ;print success
		INT 21H
        ret
    uninstall_55h endp


CODE ENDS
END init 