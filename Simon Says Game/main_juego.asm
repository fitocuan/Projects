#include <p18f45k50.inc>
    
    CONFIG WDTEN = OFF
    
    ;variables
    CONTA_1 EQU 0x01
    CONTA_2 EQU 0x02  
   
    yellow equ 0x03
    red equ 0x04
    green equ 0x05
    blue equ 0x06
    rand equ 0x07
    five equ 0x08
    lastKey equ 0x09
    colorSet equ 0x10
    HIGHSCORE equ 0x11
    aux equ 0x12
    contador EQU 0x13
 
    color1 equ 0x14
    color2 equ 0x15
    color3 equ 0x16
    color4 equ 0x17
    color5 equ 0x18
    color6 equ 0x19
    color7 equ 0x20
    color8 equ 0x21
    color9 equ 0x22
    color10 equ 0x23
 
    matchColor equ 0x24
    randomSet equ 0x25
    colorNum equ 0x26
 
    VAR1    EQU     0x27            ;DELAY VARIABLE
    VAR2    EQU     0x28            ;DELAY VARIABLE
    LCD_RS  EQU     0
    LCD_RW  EQU     1
    LCD_EN  EQU     2
 
    ORG 0 ; RESET VECTOR
    GOTO 0X1000
    ;
    ORG 0X08 ; HIGH INTERRUPT VECTOR
    GOTO 0X1008
    ;
    ORG 0X18 ; LOW INTERRUPT VECTOR
    GOTO 0X1018
    ;
    ; *** END OF CODE FOR SOFTWARE SIMULATION ***
    ;
    ;
    ; *** START OF PROGRAM ***
    ;
    ; JUMP VECTORS
    ;
    ORG 0X1000 ; RESET VECTOR
    GOTO configurar
    
    ORG 0X1008 ; HIGH INTERRUPT VECTOR
    ; GOTO ISR_HIGH ; UNCOMMENT WHEN NEEDED
 
    ORG 0X1018 ; LOW INTERRUPT VECTOR
    ; GOTO ISR_LOW 
;
    
SETUP:
    CLRF    ANSELD, BANKED  ;SET PINS IN PORTD AS DIGITALS D
    CLRF    TRISD           ;SET PORTD AS OUTPUT D
    CLRF    ANSELE, BANKED  ;SET PINS IN LATA AS DIGITALS
    CLRF    TRISE           ;SET LATA AS OUTPUT
    CLRF    LATE           ;SET VALUES AS ZEROs
    RETURN

DELAY:
        MOVLW   0x1F            ;COUNTING TO 0x03E8 2ms?
        MOVWF   VAR1
LOOPD2:
        MOVLW   0xE8
        MOVWF   VAR2
LOOPD1:
        DECFSZ  VAR2
        GOTO    LOOPD1
        DECFSZ  VAR1
        GOTO    LOOPD2
        RETURN

LCD_INIT:
        ;CALL    CHECK_BUSY
        CLRF    LATE
        BSF     LATE, LCD_EN   ;EN = 1
        BCF     LATE, LCD_RS   ;RS = 0
        MOVLW   0x38            ;8-BIT INTERFACE, CHARACTER DE 5x8
        MOVWF   LATD            ; D
	CALL    DELAY

        BCF     LATE, LCD_EN   ;EN = 0
        RETURN

LCD_ON:
        ;CALL    CHECK_BUSY
        BSF     LATE, LCD_EN   ;EN = 1
        BCF     LATE, LCD_RS   ;RS = 0
        MOVLW   0x0C            ;LCD ON, CURSOR ON 0F? 0C
        MOVWF   LATD            ; D
        BCF     LATE, LCD_EN   ;EN = 0
        CALL    DELAY
        RETURN

LCD_C1HOME:
        ;CALL    CHECK_BUSY
        BSF     LATE, LCD_EN   ;EN = 1
        BCF     LATE, LCD_RS   ;RS = 0
        MOVLW   0x02            ;CURSOR AT HOME
        MOVWF   LATD            ; D
        BCF     LATE, LCD_EN   ;EN = 0
        CALL    DELAY
        RETURN

LCD_CLEAR:
        ;CALL    CHECK_BUSY
        BSF     LATE, LCD_EN   ;EN = 1
        BCF     LATE, LCD_RS   ;RS = 0
        MOVLW   0x01            ;DISPLAY CLEAN
        MOVWF   LATD            ; D
        BCF     LATE, LCD_EN   ;EN = 0
        CALL    DELAY
        RETURN

LCD_WRITE:                     ;NEEDS DATA ON W REGISTER
        ;CALL    CHECK_BUSY
        BSF     LATE, LCD_EN   ;EN = 1
        BSF     LATE, LCD_RS   ;RS = 1
        MOVWF   LATD            ; D
        BCF     LATE, LCD_EN   ;EN = 0
        CALL    DELAY
        RETURN

LCD_C2HOME:
        ;CALL    CHECK_BUSY
        BSF     LATE, LCD_EN   ;EN = 1
        BCF     LATE, LCD_RS   ;RS = 0
        MOVLW   0xC0           ;CURSOR AT SECOND HOME
        MOVWF   LATD            ; D
        BCF     LATE, LCD_EN   ;EN = 0
        BCF     LATE, LCD_RS   ;RS = 0
        CALL    DELAY
        CALL    DELAY
        RETURN
	
LCD_MOVE:
        ;CALL    CHECK_BUSY
        BSF     LATE, LCD_EN   ;EN = 1
        BCF     LATE, LCD_RS   ;RS = 0
        MOVWF   LATD            ; D
        BCF     LATE, LCD_EN   ;EN = 0
        BCF     LATE, LCD_RS   ;RS = 0
        CALL    DELAY
        CALL    DELAY
        RETURN
	
MENU_INICIO:
    MOVLW   'I'    
    CALL    LCD_WRITE
    MOVLW   'N'    
    CALL    LCD_WRITE
    MOVLW   'I'    
    CALL    LCD_WRITE
    MOVLW   'C'    
    CALL    LCD_WRITE
    MOVLW   'I'    
    CALL    LCD_WRITE
    MOVLW   'A'    
    CALL    LCD_WRITE
    MOVLW   'R'    
    CALL    LCD_WRITE
    MOVLW   ' '    
    CALL    LCD_WRITE
    MOVLW   'J'    
    CALL    LCD_WRITE
    MOVLW   'U'    
    CALL    LCD_WRITE
    MOVLW   'E'    
    CALL    LCD_WRITE
    MOVLW   'G'    
    CALL    LCD_WRITE
    MOVLW   'O'    
    CALL    LCD_WRITE
    MOVLW b'00111100'
    CALL    LCD_WRITE
    CALL    LCD_ON
    RETURN
    
MENU_INICIO_ABAJO:
    CALL LCD_C2HOME
    MOVLW   'H'    
    CALL    LCD_WRITE
    MOVLW   'I'    
    CALL    LCD_WRITE
    MOVLW   'G'    
    CALL    LCD_WRITE
    MOVLW   'H'    
    CALL    LCD_WRITE
    MOVLW   'S'    
    CALL    LCD_WRITE
    MOVLW   'C'    
    CALL    LCD_WRITE
    MOVLW   'O'    
    CALL    LCD_WRITE
    MOVLW   'R'    
    CALL    LCD_WRITE
    MOVLW   'E'    
    CALL    LCD_WRITE
    CALL    LCD_ON
    
    RETURN
 

	
configurar
    
    CALL    SETUP
    CALL    LCD_INIT
    CALL    LCD_ON
    CALL    LCD_C1HOME
    CALL    LCD_CLEAR
    CLRF 0x35,A
    CALL INICIALIZAR_ROM
    
    
    movlw d'0'
    movwf CONTA_1, A ; los registros de conteo empiezan vacios
    movwf CONTA_2, A
    movwf lastKey, A
    movwf colorSet, A
    movwf score,A
    movwf aux,A
    movwf randomSet,A
    movwf colorNum,A
    
    movlw d'2' ;contador para repetir el retardo + 1
    movwf contador,A
    
    movlw d'6' ;contador para repetir el retardo + 1
    movwf five,A
    
    movlw d'1'
    movwf yellow, A ;para prender el led amarillo 
    movlw d'2'
    movwf red, A ;para prender el led amarillo 
    movlw d'4'
    movwf green, A ;para prender el led amarillo 
    movlw d'8'
    movwf blue, A ;para prender el led amarillo 
    
    movff green,color1
    movff green,color6
    movff green,color7
    movff green,color10
    movff blue,color2
    movff blue,color8
    movff yellow,color3
    movff yellow,color4
    movff red,color5
    movff red,color9

    movlb d'15'
    clrf ANSELB, BANKED ;puertos Digitales
    clrf ANSELA, BANKED
    clrf ANSELD, BANKED
    clrf ANSELE, BANKED
    bcf INTCON2, 7, A ;activa las resistencias globales pull-up (pin negado)
    movlw b'00001111' ; 50-50 I/O *bits mas significativos son salidas
    movwf TRISB, A
    movwf WPUB, A ; Enables pull-up on inputs
    clrf TRISD, A ;salidas
    clrf TRISA, A ;salidas
    clrf LATD, A ;limpia la salida
    setf LATB, A ;niveles iniciales de high
    
    ;TIMER3
    bcf T3GCON,7,A ;activa el enable global de tmr3
    movlw b'00110010' ;configuracion inicial
    movwf T3CON,A 
    
    ;TIMER0
    movlw b'11001111'
    movwf T0CON,A ;tmr0 ACTIVADO, modo 16 bit, pre-256
    
    ;************
    CALL    LCD_C1HOME
    CALL    LCD_CLEAR
    CALL MENU_INICIO
    CALL MENU_INICIO_ABAJO
    
start
    movlw b'01111111' ;scan primera columna
    movwf LATB,A 
    btfss PORTB, 0, A ;checa el boton asterisco
    goto keyAst
    btfss PORTB, 1, A ;checa el boton 7
    goto key7
    btfss PORTB, 2, A ;checa el boton 4
    goto key4
    btfss PORTB, 3, A ;checa el boton 1
    goto key1
    
    
    movlw b'10111111' ;scan segunda columna
    movwf LATB,A 
    btfss PORTB, 0, A ;checa el boton 0
    goto key0
    btfss PORTB, 1, A ;checa el boton 8
    goto key8
    btfss PORTB, 2, A ;checa el boton 5
    goto key5
    btfss PORTB, 3, A ;checa el boton 2
    goto key2
    
    
    movlw b'11011111' ;scan tercera columna
    movwf LATB,A 
    btfss PORTB, 0, A ;checa el boton gato
    goto keyGato
    btfss PORTB, 1, A ;checa el boton 9
    goto key9
    btfss PORTB, 2, A ;checa el boton 6
    goto key6
    btfss PORTB, 3, A ;checa el boton 3
    goto key3
    
 
    movlw b'11101111' ;scan cuarta columna
    movwf LATB,A 
    btfss PORTB, 0, A ;checa el boton Yellow
    goto keyYellow
    btfss PORTB, 1, A ;checa el boton Red
    goto keyRed
    btfss PORTB, 2, A ;checa el boton Green
    goto keyGreen
    btfss PORTB, 3, A ;checa el boton Blue
    goto keyBlue
    
    
    btfss colorSet,0,A ;Checa si ya entro a la rut de color
    goto SS
    goto W8

SS
    btfss randomSet,0,A ;Checa si ya se activo el random
    goto start ;bucle
    
    
SECUENCIA:
UNO    
    movff color1, LATA ;led verde encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    movlw d'1' 
    movwf colorSet,A ;lo activa si entra en la rut de color
    
    movlw d'0'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto DOS ; salta a DOS si ya pasó el primer evento
    
    
DOS
    movff color2, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    movlw d'2'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto TRES ; salta a DOS si ya pasó el primer evento

TRES
    movff color3, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    movlw d'5'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto CUATRO ; salta a DOS si ya pasó el primer evento
    
CUATRO
    movff color4, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    movlw d'9'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto CINCO ; salta a DOS si ya pasó el primer evento
    
CINCO
    movff color5, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    movlw d'14'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto SEIS ; salta a DOS si ya pasó el primer evento
    
SEIS
    movff color6, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    movlw d'20'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto SIETE ; salta a DOS si ya pasó el primer evento
    
SIETE

    movff color7, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    movlw d'27'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto OCHO ; salta a DOS si ya pasó el primer evento
    
OCHO
    movff color8, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    movlw d'35'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto NUEVE ; salta a DOS si ya pasó el primer evento
    
NUEVE
    movff color9, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    movlw d'44'
    cpfsgt aux,A ;skip if greater than WREG
    goto check ; si es menor o igual
    goto DIEZ ; salta a DOS si ya pasó el primer evento
    
DIEZ 
    movff color10, LATA ;led azul encendido
    movff five,contador
    CALL RET ;retardo de 0.5s para poderlo ver
    clrf LATA,A ;apaga leds
    call RET
    
    goto check
   
    
check:
   ch1
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color1,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'1' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 1 = skip 
    goto ch2
    goto SECUENCIA
    
   ch2 
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color2,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'3' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 3 = skip 
    goto ch3
    goto SECUENCIA
    
   ch3 
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color3,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'6' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 6 = skip 
    goto ch4
    goto SECUENCIA
    
    ch4 
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color4,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'10' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 6 = skip 
    goto ch5
    goto SECUENCIA
    
    ch5 
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color5,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'15' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 6 = skip 
    goto ch6
    goto SECUENCIA
    
    ch6 
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color6,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'21' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 6 = skip 
    goto ch7
    goto SECUENCIA
    
    ch7 
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color7,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'28' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 6 = skip 
    goto ch8
    goto SECUENCIA
    
    ch8
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color8,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'36' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 6 = skip 
    goto ch9
    goto SECUENCIA
    
    ch9
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color9,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
    movlw d'45' 
    cpfseq aux,A ;checa la rutina en la que va, igual a 6 = skip 
    goto ch10
    goto SECUENCIA
    
    ch10
    call W8
    movf lastKey,W,A ;mueve lo ultimo presionado a WREG
    cpfseq color10,W ;si el color y el boton presionado son iguales salta
    goto MAL
    call BIEN 
   
    goto BYE ;terminar
    
W8:
    movlw d'0'
    cpfseq lastKey,A ;checa si ya se presiono algun boton, igual a cero = skip
    return ;si es diferente a 0 entonces ya se presiono algo, regresa
    goto start
    
RANDOM:
    movff TMR0L,rand ;mueve lo que hay en tmr0 a rand
    bcf rand,7,A
    bcf rand,6,A
    bcf rand,5,A
    bcf rand,4,A
    bcf rand,3,A
    bcf rand,2,A ;Quedan solo los valores de 0 a 3
    
    C1
    movlw d'3'
    cpfseq rand,A ;si es igual a 3 skip
    goto C2
    movff yellow,matchColor
    goto putColor
    
    C2
    movlw d'2'
    cpfseq rand,A ;si es igual a 2 skip
    goto C3
    movff red,matchColor
    goto putColor
    
    C3
    movlw d'1'
    cpfseq rand,A ;si es igual a 1 skip
    goto C4
    movff green, matchColor
    goto putColor
    
    C4
    movff blue, matchColor
    
putColor
    incf colorNum,F,A ;incrementa el contador 
    
    p1
    movlw d'1'
    cpfseq colorNum,A ;si es igual a 1 skip
    goto p2
    movff matchColor,color1
    return
    ;goto RANDOM
    
    p2
    movlw d'2'
    cpfseq colorNum,A ;si es igual a 2 skip
    goto p3
    movff matchColor,color2
    return
    ;goto RANDOM
    
    p3
    movlw d'3'
    cpfseq colorNum,A ;si es igual a 2 skip
    goto p4
    movff matchColor,color3
    return
    ;goto RANDOM
    
    p4
    movlw d'4'
    cpfseq colorNum,A ;si es igual a 2 skip
    goto p5
    movff matchColor,color4
    return
    ;goto RANDOM
    
    p5
    movlw d'5'
    cpfseq colorNum,A ;si es igual a 2 skip
    goto p6
    movff matchColor,color5
    return
    ;goto RANDOM
    
    p6
    movlw d'6'
    cpfseq colorNum,A ;si es igual a 2 skip
    goto p7
    movff matchColor,color6
    return
    ;goto RANDOM
    
    p7
    movlw d'7'
    cpfseq colorNum,A ;si es igual a 2 skip
    goto p8
    movff matchColor,color7
    return
    ;goto RANDOM
    
    p8
    movlw d'8'
    cpfseq colorNum,A ;si es igual a 2 skip
    goto p9
    movff matchColor,color8
    return
    ;goto RANDOM
    
    p9
    movlw d'9'
    cpfseq colorNum,A ;si es igual a 2 skip
    goto p10
    movff matchColor,color9
    return
    ;goto RANDOM
    
    p10
    movlw d'10'
    cpfseq colorNum,A ;si es igual a 10 skip
    return
    movff matchColor,color10
    return
    
    
key0: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 0, A ;checa si ya se dejó de presionar
    goto key0
    ;movlw b'00000000'
    ;movwf LATD, A
    goto start
key1: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 1, A ;checa si ya se dejó de presionar
    goto key1
    
    MOVLW b'10001101'
    CALL LCD_MOVE  
    MOVLW b'00111100'
    CALL    LCD_WRITE
    MOVLW 0xC9
    CALL LCD_MOVE  
    MOVLW ' '
    CALL    LCD_WRITE
    BSF  0x35,0
    
    goto start
key2: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 2, A ;checa si ya se dejó de presionar
    goto key2
    ;movlw b'00000010'
    ;movwf LATD, A
    goto start
key3: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 3, A ;checa si ya se dejó de presionar
    goto key3
    ;movlw b'00000011'
    ;movwf LATD, A
    goto start
key4: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 0, A ;checa si ya se dejó de presionar
    goto key4
    
    MOVLW 0xC9
    CALL LCD_MOVE  
    MOVLW b'00111100'
    CALL    LCD_WRITE
    MOVLW b'10001101'
    CALL LCD_MOVE  
    MOVLW ' '
    CALL    LCD_WRITE
    BCF  0x35,0
    CALL    RET
    
    goto start
key5: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 1, A ;checa si ya se dejó de presionar
    goto key5
    ;movlw b'00000101'
    ;movwf LATD, A
    goto start
key6: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 2, A ;checa si ya se dejó de presionar
    goto key6
    ;movlw b'00000110'
    ;movwf LATD, A
    goto start
key7: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 3, A ;checa si ya se dejó de presionar
    goto key7
    ;movlw b'00000111'
    ;movwf LATD, A
    goto start
key8: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 0, A ;checa si ya se dejó de presionar
    goto key8
    ;movlw b'00001000'
    ;movwf LATD, A
    goto start
key9: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 1, A ;checa si ya se dejó de presionar
    goto key9
    ;movlw b'00001001'
    ;movwf LATD, A
    goto start
keyBlue: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 3, A ;checa si ya se dejó de presionar
    goto keyBlue
    btfsc colorSet,0,A ;Checa si ya entro a la rut de color, si no se salta
    movff blue,lastKey
    goto start
keyGreen: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 2, A ;checa si ya se dejó de presionar
    goto keyGreen
    btfsc colorSet,0,A ;Checa si ya entro a la rut de color, si no se salta
    movff green,lastKey
    goto start
keyRed: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 1, A ;checa si ya se dejó de presionar
    goto keyRed
    btfsc colorSet,0,A ;Checa si ya entro a la rut de color, si no se salta
    movff red,lastKey
    goto start
keyYellow: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 0, A ;checa si ya se dejó de presionar
    goto keyYellow
    btfsc colorSet,0,A ;Checa si ya entro a la rut de color, si no se salta
    movff yellow,lastKey
    goto start
keyGato: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 0, A ;checa si ya se dejó de presionar
    goto keyGato
    ;call RANDOM
    ;setf randomSet,A ;activa el modo random
    goto start
keyAst: 
    call DEBOUNCE; retardo de 60ms
    btfss PORTB, 0, A ;checa si ya se dejó de presionar
    goto keyAst
    
    CALL    LCD_C1HOME
    CALL    LCD_CLEAR
    BTFSS 0x35,0
    CALL VER_HIGHSCORE
    call BIEN
    setf randomSet,A ;activa el modo random
    clrf aux,A
    
    goto start
    
    
    
    
    
DEBOUNCE: ;retardo de 60mS
     call rutDel ; llama la primera rutina de delay = 1028 ciclos
     call rutDel2 ;llama la segunda rutina de delay = 264196 ciclos
     return ;regresa
     
    rutDel 
	incf CONTA_1, F, A
	btfss STATUS, 2
	goto rutDel
	return
    rutDel2 
	call rutDel
	incf CONTA_2, F, A
	btfss STATUS, 2
	goto rutDel2
	return
	
	RET: ;retardo de .125s
	bsf T3CON,0,A ;activa el conteo
	movlw b'00001011'
	movwf TMR3H,A ;inicia la parte alta en 2816
	movlw b'11011100'
	movwf TMR3L,A ;inicia la parte baja en 220
	;de esta manera tenemos que el contador inicia en 3036 para
	;que el conteo sea de .5s exactamente
	bcf PIR2,1,A ;apaga la bandera the overflow
	decfsz contador,F,A; decrementa el contador hasta llegar a 0
	goto espera
	bcf T3CON,0,A ;desactiva el conteo
	movlw d'2' ;contador para repetir el retardo + 1
	movwf contador,A
	return

espera ;
	btfss PIR2,1,A ;checa bandera de desborde
	goto espera ;repetir si no se ha desbordado
	goto RET
	
	
	
BIEN:
    
	CALL    LCD_C1HOME
	CALL    LCD_CLEAR
	MOVF    aux,W,A
	ADDLW   0x30
	CALL LCD_WRITE
	movlw d'16'
	movwf LATA,A ;indica que esta bien
	call RET
	clrf LATA,A ;apaga leds
	incf aux,F,A ;incrementa en 1 si esta bien
	;movff score,aux ;copia el valor de score a aux
	clrf lastKey,A ;limpia el ultimo estado del boton presinado
	call RANDOM
	
	return
MAL:
	movlw d'32'
	movwf LATA,A ;indica que esta mal
	call RET
	clrf LATA,A ;apaga leds
	GOTO configurar
	
	
    BYE
	end