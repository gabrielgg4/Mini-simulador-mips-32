class Registers:
    # Simula os registradores criando um array, pra ficar mais facil de implementar a interface
    # tem um array com os nomes dos registradores, em ordem igual
    def __init__(self):
        self.registers = [0] * 32
        self.register_names = [
            "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
            "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
            "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
            "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
        ]

    def ler(self, reg_num):
        valor = self.registers[reg_num]
        print(f"Lendo registrador {reg_num} ({self.register_names[reg_num]}): {valor}")
        return valor

    def escrever(self, reg_num, valor):
        if reg_num != 0:
            self.registers[reg_num] = valor
            print(f"Escrevendo registrador {reg_num} ({self.register_names[reg_num]}): {valor}")

    def reiniciar(self):
        self.registers = [0] * 32 # Recria o array com todos os registradores zerados
        print("Todos os registradores foram resetados.")

    def obter_nome_registrador(self, reg_num):
        return self.register_names[reg_num]

    def log_registradores(self):
        for i, valor in enumerate(self.registers):
            print(f"{self.register_names[i]}: {valor}")
