.data
array:  .word   1, 2, 3, 4, 5
msg1:   .asciiz "Resultado: "
msg2:   .asciiz "Fim do Programa\n"
msg3:   .asciiz "Fim do Programa\n"
msg4:   .asciiz "Fim do Programa\n"

.text
main:
    # Inicialização dos registradores
    li      $t0,    0                   # $t0 = 0
    li      $t1,    5                   # $t1 = 5
    li      $t2,    10                  # $t2 = 10
    la      $t3,    array               # Carregar o endereço de 'array' em $t3

    # Operações aritméticas e lógicas
    add     $t4,    $t0,    $t1         # $t4 = $t0 + $t1
    addi    $t5,    $t1,    5           # $t5 = $t1 + 5
    sub     $t6,    $t2,    $t1         # $t6 = $t2 - $t1
    mul     $t7,    $t1,    $t2         # $t7 = $t1 * $t2
    and     $t8,    $t1,    $t2         # $t8 = $t1 & $t2
    or      $t9,    $t1,    $t2         # $t9 = $t1 | $t2
    sll     $s0,    $t1,    2           # $s0 = $t1 << 2

    # Operações de carregamento e armazenamento
    lw      $s1,    0($t3)              # Carregar o valor de memória em $s1
    sw      $s1,    4($t3)              # Armazenar o valor de $s1 na memória

    # Comparações
    slt     $s3,    $t1,    $t2         # $s3 = ($t1 < $t2) ? 1 : 0
    slti    $s4,    $t1,    15          # $s4 = ($t1 < 15) ? 1 : 0

    # Imprimir resultados
    li      $v0,    4                   # Código de serviço para imprimir string
    la      $a0,    msg1                # Carregar o endereço da mensagem em $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $t4                 # Mover o valor de $t4 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $t5                 # Mover o valor de $t5 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $t6                 # Mover o valor de $t6 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $t7                 # Mover o valor de $t7 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $t8                 # Mover o valor de $t8 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $t9                 # Mover o valor de $t9 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $s0                 # Mover o valor de $s0 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $s1                 # Mover o valor de $s1 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $s3                 # Mover o valor de $s3 para $a0
    syscall                             # Chamar o serviço do sistema

    li      $v0,    1                   # Código de serviço para imprimir inteiro
    move    $a0,    $s4                 # Mover o valor de $s4 para $a0
    syscall                             # Chamar o serviço do sistema

    # Imprimir mensagem de fim do programa
    li      $v0,    4                   # Código de serviço para imprimir string
    la      $a0,    msg2                # Carregar o endereço da mensagem em $a0
    syscall                             # Chamar o serviço do sistema
sair:
    # Sair do programa
    li      $v0,    10                  # Código de serviço para sair
    syscall                             # Chamar o serviço do sistema
