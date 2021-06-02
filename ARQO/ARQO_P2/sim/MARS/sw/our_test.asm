# Prog de prueba para Practica 2. Ej 1

.data 0
num0: .word 777
num1: .word 755


.text 0
main:
  #REGISTER
  addi $t0, $zero, 100 
  addi $t1, $zero, 100
  beq $t0, $t1, Rtestsuccess             #si funciona t7 = 0, si no t7=1
  addi $t7, $zero, 1
  
Rtestsuccess:
 addi $t7, $zero, 0
 
 
 addi $t1, $zero, 777
 beq $t0, $t1, Rtestnosuccess            #si funciona t7 = 0, si no t7=2
 addi $t7, $zero, 0
 
 lw $t0, num0
 beq $t0, $t1, LWtestsuccess             #si funciona t7 = 0, si no t7=3
 addi $t7, $zero, 3

LWtestsuccess:
 addi $t7, $zero, 0
 lw $t1, num1
 beq $t0, $t1, LWtestnosuccess           #si funciona t7 = 0, si no t6=4
 addi $t7, $zero, 0
 nop
 nop
 nop
 j end
 nop
 nop
 nop
 
LWtestnosuccess:
 addi $t6, $zero, 4
Rtestnosuccess:
 addi $t7, $zero, 2
 
end:
j end
