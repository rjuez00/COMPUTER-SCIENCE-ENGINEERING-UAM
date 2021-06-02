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
addi $t1, $zero, 24
add $t2, $t0, $t1 #t2 = 35
sub $t2, $t2, $t1 #t2 = t0 = 1d

addi $t3, $zero, 14
addi $t4, $zero, 8
and $t5, $t4, $t3
or $t6, $t4, $t3
xor $t7, $t4, $t3

nop

slti $t0, $t0, 30
sw $t1, 0x0008
lw $t7, 0x0008

beq $t1, $t2, fin
addi $t0, $zero, 24
lui $t3, 500
beq $t1, $t0, aqui

fin: j fin

aqui: addi $t0, $zero, 10000
j fin