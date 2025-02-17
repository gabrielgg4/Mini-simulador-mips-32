.data
array: .word 3, 4, 5, 8, 9, 10
.text
main:
    # inicializacao dos registradores
    li      $t0,    0                   # $t0 = 0
    li      $t1,    5                   # $t1 = 5
    li      $t2,    10                  # $t2 = 10
    la      $t3,    array               # $t3 = &array

    # operacoes aritmeticas e logicas
    add     $t4,    $t0,    $t1         # $t4 = $t0 + $t1
    addi    $t5,    $t1,    5           # $t5 = $t1 + 5
    sub     $t6,    $t2,    $t1         # $t6 = $t2 - $t1
    and     $t8,    $t1,    $t2         # $t8 = $t1 & $t2
    or      $t9,    $t1,    $t2         # $t9 = $t1 | $t2
    slt     $s0,    $t1,    2           # $s0 = $t1 << 2

    # operacoes de carregamento e armazenamento
    lw      $s1,    0($t3)              # 
    sw      $s1,    4($t3)              # 

    # comparacoes
    slt     $s3,    $t1,    $t2         # $s3 = ($t1 < $t2)
    li      $t3,    15
    slt     $s4,    $t1,    $t3         # $s4 = ($t1 < 15)

    # imprimir resultados

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t4                 # $a0 = $t4
    # syscall
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t5                 # $a0 = $t5
    # syscall
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t6                 # $a0 = $t6
    # syscall
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t7                 # $a0 = $t7
    # syscall
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t8                 # $a0 = $t8
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $t9                 # $a0 = $t9
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s0                 # $a0 = $s0
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s1                 # $a0 = $s1
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s3                 # $a0 = $s3
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s4                 # $a0 = $s4
    syscall

    li      $v0,    1                   # $v0 = 1
    move    $a0,    $s4                 # $a0 = $s4
    syscall

    li      $v0,    4                   # $v0 = 4
    syscall
sair:
    li      $v0,    10                  # v0 = 10
    syscall