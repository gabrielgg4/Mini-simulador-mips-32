.data
array: .word 3, 4, 5, 8, 9, 10
.text
main:
    # inicializacao dos registradores
    li      $t0,    0                   # $t0 = 0
    li      $t1,    5                   # $t1 = 5
    li      $t2,    10                  # $t2 = 10
    la      $t3,    array               # carregar o endereco de 'array' em $t3

    # operacoes aritmeticas e logicas
    add     $t4,    $t0,    $t1         # $t4 = $t0 + $t1
    addi    $t5,    $t1,    5           # $t5 = $t1 + 5
    sub     $t6,    $t2,    $t1         # $t6 = $t2 - $t1
    and     $t8,    $t1,    $t2         # $t8 = $t1 & $t2
    or      $t9,    $t1,    $t2         # $t9 = $t1 | $t2
    slt     $s0,    $t1,    2           # $s0 = $t1 << 2

    # operacoes de carregamento e armazenamento
    lw      $s1,    0($t3)              # carregar o valor de memoria em $s1
    sw      $s1,    4($t3)              # armazenar o valor de $s1 na memoria

    # comparacoes
    slt     $s3,    $t1,    $t2         # $s3 = ($t1 < $t2) ? 1 : 0
    li      $t3,    15
    slt     $s4,    $t1,    $t3          # $s4 = ($t1 < 15) ? 1 : 0

    # imprimir resultados

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t4                 # mover o valor de $t4 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t5                 # mover o valor de $t5 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t6                 # mover o valor de $t6 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t7                 # mover o valor de $t7 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t8                 # mover o valor de $t8 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t9                 # mover o valor de $t9 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s0                 # mover o valor de $s0 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s1                 # mover o valor de $s1 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s3                 # mover o valor de $s3 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s4                 # mover o valor de $s4 para $a0
    # chamar o servico do sistema
    syscall

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s4                 # mover o valor de $s4 para $a0
    syscall

    # imprimir mensagem de fim do programa
    li      $v0,    4                   # codigo de servico para imprimir string
    # chamar o servico do sistema
    syscall
sair:
    # sair do programa
    li      $v0,    10                  # codigo de servico para sair
    # chamar o servico do sistema
    syscall