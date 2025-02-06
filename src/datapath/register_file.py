class RegisterFile:
    def __init__(self):
        self.registers = [0] * 32
        self.register_names = [
            "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
            "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
            "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
            "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
        ]

    def read(self, reg_num):
        value = self.registers[reg_num]
        print(f"Lendo registrador {reg_num} ({self.register_names[reg_num]}): {value}")
        return value

    def write(self, reg_num, value):
        if reg_num != 0:  # O registrador 0 é sempre 0
            self.registers[reg_num] = value
            print(f"Escrevendo registrador {reg_num} ({self.register_names[reg_num]}): {value}")

    def reset(self):
        self.registers = [0] * 32
        print("Todos os registradores foram resetados.")

    def get_register_name(self, reg_num):
        return self.register_names[reg_num]

    def debug_registers(self):
        for i, value in enumerate(self.registers):
            print(f"{self.register_names[i]}: {value}")
