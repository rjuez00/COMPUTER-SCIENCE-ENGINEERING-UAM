.data 0
num0:  .word 0
num1:  .word 0
num2:  .word 0
num3:  .word 0
num4:  .word 0
num5:  .word 0


.text 0
main:
addi $t1, $zero, 420
nop
nop
nop

sw $t1, 0x0000
nop
nop
nop

lw $t2, 0x0000
nop
nop
nop

fin:
    nop
    nop
    nop
    j fin
    
