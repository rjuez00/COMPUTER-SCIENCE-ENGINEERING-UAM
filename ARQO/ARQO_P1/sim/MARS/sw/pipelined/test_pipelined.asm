.data 0
num0:  .word 0
num1:  .word 0
num2:  .word 0
num3:  .word 0
num4:  .word 0
num5:  .word 0


.text 0
main:
addi $t0, $zero, 29
nop
nop
nop

addi $t1, $zero, 10
nop
nop
nop

add $t2, $t0, $t1 #t2 = 35
nop
nop
nop

sub $t2, $t0, $t1 #t2 = t0 = 1d
nop
nop
nop

and $t2, $t0, $t1
nop
nop
nop

or $t2, $t0, $t1
nop
nop
nop


slti $t2, $t0, 30
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

beq $t0, $t1, fin
nop
nop
nop

beq $t0, $t0, aqui


lui $t3, 500

fin:
    nop
    nop
    nop
    j fin
    

aqui: 
    nop
    nop
    nop

    addi $t0, $zero, 10000
    nop
    nop
    nop

    j fin
