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
	askfilenameMSG DB "Input filename:     $"
    filenameREAD db 15, ?, 15 dup('$')
	filenameMSG DB        "File name:          $"
	filetypeMSG DB        "File type:          $"
	samplerateMSG DB      "Sample rate:        $" 
	nsamplesMSG DB   	  "Number of samples:  $" 
	nchannelsMSG DB       "Number of channels: $" 
	bpsMSG DB        	  "Bytes per second:   $" 
	bpsrawMSG DB		  "Bits per second:    $"
	typeofrecordingMSG DB "Type of recording:  $" 

	typeREAD DB 4 dup(?), '$'
	samplerateREAD DB 5 dup('$'), '$'
	nsamplesREAD DB 5 dup('$'), '$'
	nchannelsREAD DB 5 dup('$'), '$'
	bpsREAD DB 5 dup('$'), '$'
	typeofrecordingREAD DB 5 dup('$'), '$'
	bpsrawREAD DB 5 dup('$'), '$'

	fileCONTENT DB 44 dup(?)
	errorfopenMSG DB "Error in fopen: $"
    errorfreadMSG DB "Error in fread: $"
   	errorfcloseMSG DB "Error in fclose: $"
   	erroremptyMSG DB "Error in fread, empty file$"
   	errorincompleteMSG DB "Error in fread, incomplete file$"
   	errorheaderMSG DB "Error in header missing RIFF, WAVE, fmt or data$"

    errorcodeMSG DB 4 dup('$'), '$'


	headershouldcontain1 DB "WAVE"
	headershouldcontain2 DB "RIFF"
	headershouldcontain3 DB "data"
	headershouldcontain4 DB "fmt"

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

		system_interaction:
			;MSG TO USER for NAME
			MOV AH,09H
			mov DX, OFFSET askfilenameMSG
			INT 21H
			;read from keyboard
			MOV AH, 0AH
			MOV DX, OFFSET filenameREAD
			INT 21h
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
			
		fetching_info:		;BX = FILE HANDLE
			;opening file
			MOV DX, OFFSET filenameREAD[2]
			call fopen
			MOV SI, 2; code for error control
			jc callerror
			;reading everything except data
			MOV BX, AX
			MOV CX, 44
			MOV DX, OFFSET fileCONTENT
			call fread
			MOV SI, 0; code for error control
			jc callerror
			TEST AX, AX
			MOV SI, 1; code for error control
			je callerror
			MOV BX, 44
			SUB BX, AX
			MOV SI, 3; code for error control
			JNZ callerror

			INC AX; erase zero flag
			;close file
			call fclose
			MOV SI, 4; code for error control
			jc callerror
			
			jmp cutting
		
		callerror:
			call ERROR_CONTROL
		




		cutting:
		MOV BX, 4
		MOV SI, OFFSET headershouldcontain1
		MOV DI, OFFSET fileCONTENT[8]
		call KILL_IF_NOT_bxCHARWORD

		MOV SI, OFFSET headershouldcontain2
		MOV DI, OFFSET fileCONTENT[0]
		call KILL_IF_NOT_bxCHARWORD

		MOV SI, OFFSET headershouldcontain3
		MOV DI, OFFSET fileCONTENT[36]
		call KILL_IF_NOT_bxCHARWORD
	
		MOV BX,3
		MOV SI, OFFSET headershouldcontain4
		MOV DI, OFFSET fileCONTENT[12]
		call KILL_IF_NOT_bxCHARWORD

		






		
			;type
			MOV AX, WORD PTR fileCONTENT[8]
			MOV BX, WORD PTR fileCONTENT[10]
			MOV SI, OFFSET typeREAD
			MOV WORD PTR [SI], AX
			MOV WORD PTR [SI]+2, BX
			;sample rate
			MOV AX, WORD PTR filecontent[24]
			MOV DX, AX; we will need the sample rate later on
			MOV DI, OFFSET samplerateREAD
			CALL DEC_to_ASCII
			;nsamples
			MOV AX, WORD PTR fileCONTENT[28]
			MOV DI, OFFSET nsamplesREAD
			CALL DEC_to_ASCII
			;nchannels
			MOV AX, WORD PTR fileCONTENT[22]
			MOV DI, OFFSET nchannelsREAD
			CALL DEC_to_ASCII
			;bytes per second
			MOV AX, WORD PTR fileCONTENT[34]
			MOV DI, OFFSET bpsrawREAD
			CALL DEC_to_ASCII

			MUL DX; multiply sample rate to obtain bits per second
			MOV CL, 3
			SHR AX, CL; divide by 8 to obtain bytes per second
			MOV DI, OFFSET bpsREAD
			CALL DEC_to_ASCII
			;typerecording
			MOV AX, WORD PTR fileCONTENT[20]
			MOV DI, OFFSET typeofrecordingREAD
			CALL DEC_to_ASCII

	
			
			
		
		;PRINTING PART
		;print file name
        MOV AH,09H
        mov DX, OFFSET filenameMSG
        INT 21H
		MOV AH,09H
        mov DX, OFFSET filenameREAD[2]
        INT 21H
		;new line
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
		;print file type
		MOV AH,09H
        mov DX, OFFSET filetypeMSG
        INT 21H
		MOV AH,09H
        mov DX, OFFSET typeREAD
        INT 21H

		;new line
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
		;print sample rate
		MOV AH,09H
        mov DX, OFFSET samplerateMSG
        INT 21H
		MOV AH,09H
        mov DX, OFFSET samplerateREAD
        INT 21H

		;new line
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
		;print number of samples
		MOV AH,09H
        mov DX, OFFSET nsamplesMSG
        INT 21H
		MOV AH,09H
        mov DX, OFFSET nsamplesREAD
        INT 21H

		;new line
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
		;print number of channels
		MOV AH,09H
        mov DX, OFFSET nchannelsMSG
        INT 21H
		MOV AH,09H
        mov DX, OFFSET nchannelsREAD
        INT 21H

		;new line
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
		;print bps
		MOV AH,09H
        mov DX, OFFSET bpsMSG
        INT 21H
		MOV AH,09H
        mov DX, OFFSET bpsREAD
        INT 21H

		;new line
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
		;print bpsraw
		MOV AH,09H
        mov DX, OFFSET bpsrawMSG
        INT 21H
		MOV AH,09H
        mov DX, OFFSET bpsrawREAD
        INT 21H

		;new line
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
		;print type of recording message
		MOV AH, 09H
		mov DX, OFFSET typeofrecordingMSG
		INT 21H
		MOV AH, 09H
		MOV DX, OFFSET typeofrecordingREAD
		INT 21H
		
		
		MOV AX, 4C00H
		INT 21H
		
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

	;INPUT
	;	-SI: ERROR TO PRINT:
	;		0=error_fread, 1=error_empty, 2= error_fopen, 3= error_incomplete, 4=error_fclose, 5 = header
	;	-AX: ERROR CODE IN CASE OF ERROR
	ERROR_CONTROL proc NEAR
		
		;CHECK HERE THE CALL
		TEST SI, SI
		JZ error_end_fread
		CMP SI, 1
		JE error_end_empty
		CMP SI, 2
		JE error_end_fopen
		CMP SI, 3
		JE error_end_incomplete
		CMP SI, 4
		JE error_end_fclose
		CMP SI, 5
		JE error_end_header


		; NEWLINE
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h

		error_end_fopen:
			MOV DI, OFFSET errorcodeMSG
			CALL DEC_to_ASCII
		
		;MSG TO USER
			MOV AH,09H
			mov DX, OFFSET errorfopenMSG
			INT 21H
		;MSG TO USE
			MOV AH,09H
			mov DX, OFFSET errorcodeMSG
			INT 21H
		;kill
			jmp endcall

		error_end_empty:
			call fclose
		;MSG TO USER
			MOV AH,09H
			mov DX, OFFSET erroremptyMSG
			INT 21H
		
		;kill
			jmp endcall

		error_end_fclose:
			MOV DI, OFFSET errorcodeMSG
			CALL DEC_to_ASCII
		
		;MSG TO USE
			MOV AH,09H
			mov DX, OFFSET errorfcloseMSG
			INT 21H
		;MSG TO USER
			MOV AH,09H
			mov DX, OFFSET errorcodeMSG
			INT 21H
		;kill
			jmp endcall

		error_end_fread:
			call fclose
			MOV DI, OFFSET errorcodeMSG
			CALL DEC_to_ASCII
		
		;MSG TO USER
			MOV AH,09H
			mov DX, OFFSET errorfreadMSG
			INT 21H
		;MSG TO USER
			MOV AH,09H
			mov DX, OFFSET errorcodeMSG
			INT 21H
		;kill
			jmp endcall

		error_end_incomplete:
			call fclose
		;MSG TO USER
			MOV AH,09H
			mov DX, OFFSET errorincompleteMSG
			INT 21H
		
		;kill
			jmp endcall
		
		error_end_header:
			call fclose
			;MSG TO USER
			MOV AH,09H
			mov DX, OFFSET errorheaderMSG
			INT 21H

			jmp endcall
		

		
		endcall:
			MOV AX, 4C00H
			INT 21H

		ERROR_CONTROL endp


		
	;INPUT:
    ;   -DS:DI REAL MEMORY WHERE IS STORED THE ASCII
    ;   -DS:SI variable called quit with "quit" inside
	;	-BX: LENGTH
    ;OUTPUT:
    ;   -ZF: 1 if equals/0 not equals
	KILL_IF_NOT_bxCHARWORD proc
			PUSH BX
			PUSH AX

        ifquit:
            MOV AH, BYTE PTR [DI][BX]-1
            CMP AH, BYTE PTR [SI][BX]-1
            je continueloop
            jmp killifquit
            
            continueloop:
            dec bx
            je notquit
            jmp ifquit


        killifquit:

		; NEWLINE
			mov ah, 02h
			mov dl, 13
			int 21h
			mov dl, 10
			int 21h
			;MSG TO USER
			MOV AH,09H
			mov DX, OFFSET errorheaderMSG
			INT 21H
		

        MOV AX, 4C00H
        INT 21H
        notquit:
        POP AX
        POP BX
        ret

	KILL_IF_NOT_bxCHARWORD endp

	



	CODE ENDS
END INICIO 