
.data
    mensagem: .asciiz "Por favor, digite o primeiro número\n\n"
    mensagem2: .asciiz "Por favor, digite o segundo número\n\n"
.text
    main:
        li $v0, 4
        la $a0, mensagem
        syscall
        
        li $v0, 5
        syscall      
        move $t0, $v0
        
        
        li $v0, 4
        la $a0, mensagem2
        syscall
        
        li $v0, 5
        syscall      
        
        move $t1, $v0
        
        add $t2, $t0, $t1        
        sub $t3, $t0, $t1
        mul $t4, $t0, $t1
        
        li $v0, 10
        syscall