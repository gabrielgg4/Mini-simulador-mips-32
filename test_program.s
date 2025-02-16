.data
array:  .word   1, 2, 3, 4, 5
msg1:   .asciiz "resultado: "
msg2:   .asciiz "fim do programa\n"
msg3:   .asciiz "fim do programa\n"
msg4:   .asciiz "fim do programa\n"

.text
main:
    li      $t0,    0                   # $t0 = 0
    li      $t1,    5                   # $t1 = 5
    li      $t2,    10                  # $t2 = 10
    la      $t3,    array               # carregar o endereco de 'array' em $t3

    # testando as operacoes
    add     $t4,    $t0,    $t1         # $t4 = $t0 + $t1
    addi    $t5,    $t1,    5           # $t5 = $t1 + 5
    sub     $t6,    $t2,    $t1         # $t6 = $t2 - $t1
    mul     $t7,    $t1,    $t2         # $t7 = $t1 * $t2
    and     $t8,    $t1,    $t2         # $t8 = $t1 & $t2
    or      $t9,    $t1,    $t2         # $t9 = $t1 | $t2
    sll     $s0,    $t1,    2           # $s0 = $t1 << 2

    # testando sw e lw
    lw      $s1,    0($t3)              # carregar o valor de memoria em $s1
    sw      $s1,    4($t3)              # armazenar o valor de $s1 na memoria

    # testando comparacoes
    slt     $s3,    $t1,    $t2         # $s3 = ($t1 < $t2) ? 1 : 0
    slti    $s4,    $t1,    15          # $s4 = ($t1 < 15) ? 1 : 0

    # imprimindo resultados
    li      $v0,    4                   # codigo de servico para imprimir string
    la      $a0,    msg1                # carregar o endereco da mensagem em $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t4                 # mover o valor de $t4 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t5                 # mover o valor de $t5 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t6                 # mover o valor de $t6 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t7                 # mover o valor de $t7 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t8                 # mover o valor de $t8 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $t9                 # mover o valor de $t9 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s0                 # mover o valor de $s0 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s1                 # mover o valor de $s1 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s3                 # mover o valor de $s3 para $a0
    syscall                             # chamar o servico do sistema

    li      $v0,    1                   # codigo de servico para imprimir inteiro
    move    $a0,    $s4                 # mover o valor de $s4 para $a0
    syscall                             # chamar o servico do sistema

  ma
    li      $v0,    4                   # codigo de servico para imprimir string
    la      $a0,    msg2                # carregar o endereco da mensagem em $a0
    syscall                             # chamar o servico do sistema
sair:
    li      $v0,    10                  # codigo de servico para sair
    syscall                             # chamar o servico do sistema
