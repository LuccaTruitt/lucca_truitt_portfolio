TITLE String Primitives and Macros     (Proj6_truittl.asm)

; Author: Lucca Truitt
; Last Modified: 3/11/2025
; OSU email address: truittl@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: 6                Due Date: March 16, 2025
; Description: Program that uses macros and string primitives to take a file full of delimiter seperated temperatures, then prints those values to the screen in reverse order.

INCLUDE Irvine32.inc

; ------------------------------------------------------
; Name: mGetString 
; 
; Asks the user for input
; 
; Preconditions: do not use edx, ecx, or eax as arguments
; 
; Receives: 
; displayMessageOffset = address of user instruction message
; maxReadLength = max number of bytes than should be read
; 
; returns:
; userInputOffset = address to users input
; userInputByteCount = number of bytes user entered
; ------------------------------------------------------
mGetString MACRO displayMessageOffset, userInputOffset, maxReadLength, userInputByteCount
	; Preserve Registers
	PUSH EDX
	PUSH ECX
	PUSH EAX

	; Display Instructions to User
	MOV  EDX, displayMessageOffset
	CALL WriteString

	; Take Input from User
	MOV  EDX, userInputOffset    ; point to the buffer 
	MOV  ECX, maxReadLength      ; specify max characters 
	CALL ReadString              ; read string from keyboard 
	MOV  userInputByteCount, EAX ; EAX gets number of characters 

	; Preserve Registers
	POP EAX
	POP ECX
	POP EDX
ENDM

; ------------------------------------------------------
; Name: mDisplayString 
; 
; Displays the inputted string to the terminal
; 
; Preconditions: do not use edx as argument
; 
; Receives: strAddress = address of string to print
; 
; returns: None
; ------------------------------------------------------
mDisplayString MACRO strAddress
	; Preserve Registers
	PUSH EDX

	; Print String
	MOV  EDX, strAddress
	CALL WriteString

	; Preserve Registers
	POP EDX
ENDM

; ------------------------------------------------------
; Name: mDisplayChar 
; 
; Displays the inputted ASCII character to the terminal
; 
; Preconditions: do not use eax as argument
; 
; Receives: inputChar = single char 
; 
; returns: None
; ------------------------------------------------------
mDisplayChar MACRO inputChar
	; Preserve Registers
	PUSH EAX

	; Print Char
	MOV  AL, inputChar 
	CALL WriteChar 

	; Preserve Registers
	POP EAX
ENDM

TEMPS_PER_DAY = 24
DELIMITER = ','
BUFFER_SIZE = 5000

.data

userInputMessage   BYTE "Please enter the filename of the file you wish to read from: ",0
userOutputMessage  BYTE "Here are the temperature values in the correct order: ",0
fileReadingError   BYTE "The file you entered was not found or not opened correctly",13,10,0
userInput		   BYTE 100 DUP(?)
userInputByteCount DWORD ?
fileBuffer		   BYTE BUFFER_SIZE DUP(?)
tempArray		   SDWORD TEMPS_PER_DAY DUP(?)

.code
main PROC

	; ---------------------------------------------------------------------------
	; Asks the user for filename input
	; If the file name is incorrect, an error will print and the program will end
	; If valid, the program will attempt to fufill the programs description
	; ---------------------------------------------------------------------------

	; Get User Input
	MOV EBX, SIZEOF userInput
	mGetString OFFSET userInputMessage, OFFSET userInput, EBX, userInputByteCount

	; Open User File
	MOV  EDX, OFFSET userInput 
	CALL OpenInputFile 

	; Check if file did not open correctly
	MOV EBX, 4294967295
	CMP EAX, EBX
	JE errorReadingFile

	; Read File Into fileBuffer
	PUSH EAX
	MOV  EDX, OFFSET fileBuffer
	MOV  ECX, BUFFER_SIZE
	CALL ReadFromFile
	POP EAX

	; Close File
    CALL CloseFile 

	; Parse buffer into SDWORD array
	PUSH OFFSET tempArray
	PUSH OFFSET fileBuffer
	CALL ParseTempsFromString

	; Display Message to User
	mDisplayString OFFSET userOutputMessage

	; Prints the temps to the screen in reverse order
	PUSH OFFSET tempArray
	CALL WriteTempsReverse

	; End Program, do not go through errorReadingFile label
	JMP endProgram

	; Display error opening file message to user
	errorReadingFile:
		mDisplayString OFFSET fileReadingError

	; End the Program
	endProgram:
	Invoke ExitProcess,0	; exit to operating system
main ENDP

; ----------------------------------------------------------------------------------------------------------- 
; Name: ParseTempsFromString 
;  
; This procedure will parse integers in string form into SDWORD formatted values, then store those into an array
; 
; Preconditions: The input array should be in string format with the delimiter used being equal to the constant
; In addition, the output array should be an empty SDWORD array with TEMPS_PER_DAY number of available indexes
; 
; Postconditions: The output is array is changed.
; 
; Receives: 
;	[EBP + 12] = OFFSET tempArray
;	[EBP + 8] = OFFSET fileBuffer
;
; Returns: The OFFSET tempArray is returned
; ----------------------------------------------------------------------------------------------------------- 
ParseTempsFromString PROC
	; Preserve Registers
	PUSH EBP
	MOV  EBP, ESP
	PUSH EAX
	PUSH EBX
	PUSH ECX
	PUSH EDX
	PUSH ESI
	PUSH EDI
	PUSHFD

	; ----------------------------------------------------------------
	; Will setup all needed flags and register
	; Will then use loop through the buffer and parse it into an array
	; ----------------------------------------------------------------

	; Setup registers and flags
	CLD
	mov ECX, TEMPS_PER_DAY
	mov ESI, [EBP + 8]
	mov EDI, [EBP + 12]
	MOV EDX, 0 ; Used as accum for current number
	MOV EBX, 0 ; Used to keep track if a number is negative
	MOV EAX, 0

	loopLabel:
		; Grab Next Value
		LODSB

		; Check if value is equal to delimiter
		MOV AH, DELIMITER
		CMP AL, AH
		JE delimiterFound ; if it is, end current loop 

		; Check if the value is a negative sign
		MOV AH, '-'
		CMP AL, AH
		JE isNegative
		JMP isNumber

		; Add value to accumulator
		isNumber:
			SUB AL, '0'
			IMUL EDX, 10 ; Multiply whats in the accumulator by 10 and store it back in the accumulator
			MOV AH, 0
			ADD EDX, EAX
			JMP loopLabel

		; Set Negative Flag
		isNegative:
			MOV EBX, 1
			JMP loopLabel

		; Store Number and End Current Loop
		delimiterFound:
			CMP EBX, 1
			JNE storeValue
			negate:
				NEG EDX
			storeValue:
				; Use STOSB to store value in EDX into array
				MOV EAX, EDX
				STOSD
				MOV EAX, 0

			MOV EDX, 0 ; Reset Accumulator
			MOV EBX, 0 ; Reset Zero

		endCurrentLoop:
			LOOP loopLabel

	; Preserve Registers		
	POPFD
	POP EDI
	POP ESI
	POP EDX
	POP ECX
	POP EBX
	POP EAX
	POP EBP
	RET 8
ParseTempsFromString ENDP

; ----------------------------------------------------------------------------------------------------------- 
; Name: WriteTempsReverse 
;  
; This procedure will print the inputted array in reverse order
; 
; Preconditions: The array should be SDWORD formatted integers to avoid potential errors
; 
; Postconditions: None, all changed registers are restored and the passed in array is not directly changed
; 
; Receives: 
;	[EBP + 8] = OFFSET tempArray
;
; Returns: None
; ----------------------------------------------------------------------------------------------------------- 
WriteTempsReverse PROC
	; Preserve Registers
	PUSH EBP
	MOV  EBP, ESP
	PUSH ECX
	PUSH EAX
	PUSH EBX
	PUSH ESI
	PUSHFD

	; Setup Register Values
	MOV ECX, TEMPS_PER_DAY
    MOV ESI, [EBP + 8]
	MOV EAX, TEMPS_PER_DAY * 4 - 4 ; TEMPS_PER_DAY * SDWORD Length - SDWORD Length
	ADD ESI, EAX

	; --------------------------------------
	; Loop through ECX number of times
	; Set Number of loops, then Load value from ESI, then decrement, then print value and delimiter, repeat TEMPS_PER_DAY number of times
	; --------------------------------------
    loopLabel:
		STD
		LODSD
        ; MOV EAX, [ESI]
        ; SUB ESI, 4
        CALL WriteInt
		mDisplayChar DELIMITER
    LOOP loopLabel
	
	; Preserve Registers
	POPFD
	POP ESI
	POP EBX
	POP EAX
	POP ECX
	POP EBP
	RET 4
WriteTempsReverse ENDP

END main
