.data
array:  .word   1, 2, 3, 4, 5
msg1:   .asciiz "Resultado: "
msg2:   .asciiz "Fim do Programa\n"
msg3:   .asciiz "Fim do Programa\n"
msg4:   .asciiz "Fim do Programa\n"

.text
main:
    li      $t0,    0                   # $t0 = 0
    li      $t1,    5                   # $t1 = 5
    li      $t2,    10                  # $t2 = 10
    la      $t3,    array               # $t3 = &array

    # Testando as operacoes
    add     $t4,    $t0,    $t1         # $t4 = $t0 + $t1
    addi    $t5,    $t1,    5           # $t5 = $t1 + 5
    sub     $t6,    $t2,    $t1         # $t6 = $t2 - $t1
    mul     $t7,    $t1,    $t2         # $t7 = $t1 * $t2
    and     $t8,    $t1,    $t2         # $t8 = $t1 & $t2
    or      $t9,    $t1,    $t2         # $t9 = $t1 | $t2
    sll     $s0,    $t1,    2           # $s0 = $t1 << 2

    # testando sw e lw
    lw      $s1,    0($t3)              # 
    sw      $s1,    4($t3)              # 

    # testando comparacoes
    slt     $s3,    $t1,    $t2         # $s3 = ($t1 < $t2)
    slti    $s4,    $t1,    15          # $s4 = ($t1 < 15)

    # Imprimindo resultados
    li      $v0,    4                   # $v0 = 4
    la      $a0,    msg1                # $a0 = &msg1
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t4                 # $a0 = $t4
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t5                 # $a0 = $t5
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t6                 # $a0 = $t6
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t7                 # $a0 = $t7
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t8                 # $a0 = $t8
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t9                 # $a0 = $t9
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s0                 # $a0 = $s0
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s1                 # $a0 = $s1
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s3                 # $a0 = $s3
    syscall                             # syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s4                 # $a0 = $s4
    syscall                             # syscall

  ma
    li      $v0,    4                   # $v0 = 4
    la      $a0,    msg2                # $a0 = &msg2
    syscall                             # syscall
sair:
    li      $v0,    10                  # v0 = 10
    syscall                             # syscall
