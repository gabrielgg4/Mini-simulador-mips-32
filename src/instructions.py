from src.datapath.alu import ALU
from src.datapath.control_unit import ControlUnit
from src.datapath.memory import Memory
from src.datapath.register_file import RegisterFile
import re
import tkinter as tk

class Instructions:
    def __init__(self, program_counter):
        self.alu = ALU()
        self.control_unit = ControlUnit()
        self.memory = Memory(4096)  # Aumentar o tamanho da memória para 4096 palavras
        self.register_file = RegisterFile()
        self.labels = {}
        self.data_section = {}
        self.program_counter = program_counter  # Adicionar o program_counter
        self.program = []  # Adicionar o atributo program

    def execute(self, instruction):
        # Manter os comentários ao executar as instruções
        instruction_with_comments = instruction.strip()
        instruction = instruction.split('#')[0].strip()
        if not instruction:
            return  # Ignorar linhas vazias ou instruções nulas
        # Verificar se a instrução contém apenas caracteres válidos (letras, números, espaços, vírgulas, parênteses)

        opcode, *operands = instruction.split()
        if not opcode:
            return  # Ignorar instruções vazias

        # Remover vírgulas dos operandos
        operands = [operand.replace(',', '').strip() for operand in operands]

        # Transformar MOVE para ADD $t1, $t2, $zero
        if opcode.upper() == "MOVE":
            reg1, reg2 = operands
            instruction = f"ADD {reg1}, {reg2}, $zero"
            opcode, *operands = instruction.split()

        # Descompactar LI para ADDI
        if opcode.upper() == "LI":
            reg, imm = self._parse_register(operands[0]), int(operands[1])
            instruction = f"ADDI {self.register_file.get_register_name(reg)} $zero, {imm}"
            print(f"Executando instrução: {instruction}")
            self.execute(instruction)
            return

        # Descompactar LA para LUI e ORI
        if opcode.upper() == "LA":
            reg, label = self._parse_register(operands[0]), operands[1]
            address = self.get_label_address(label)
            upper = (address >> 16) & 0xFFFF
            lower = address & 0xFFFF
            self.program.insert(self.program_counter.get() + 1, f"ORI {self.register_file.get_register_name(reg)}, {self.register_file.get_register_name(reg)}, {lower}")
            instruction = f"LUI {self.register_file.get_register_name(reg)}, {upper}"
            print(f"Executando instrução: {instruction}")
            self.execute(instruction)
            self.program_counter.increment()  # Increment the program counter to account for the inserted instruction
            return

        control_signals = self.control_unit.decode(opcode.upper())
        
        # Limpar operandos
        operands = [operand.replace(',', '').strip() for operand in operands]

        print(f"Executando instrução: {instruction}")  # Print da instrução transformada

        if opcode.upper() == "ADD":
            reg1, reg2, reg3 = map(self._parse_register, operands)
            operand1 = self.register_file.read(reg2)
            operand2 = self.register_file.read(reg3)
            result = self.alu.execute(control_signals["ALUOp"], operand1, operand2)
            self.register_file.write(reg1, result)
        elif opcode.upper() == "SUB":
            reg1, reg2, reg3 = map(self._parse_register, operands)
            operand1 = self.register_file.read(reg2)
            operand2 = self.register_file.read(reg3)
            result = self.alu.execute(control_signals["ALUOp"], operand1, operand2)
            self.register_file.write(reg1, result)
        elif opcode.upper() == "MUL":
            reg1, reg2, reg3 = map(self._parse_register, operands)
            operand1 = self.register_file.read(reg2)
            operand2 = self.register_file.read(reg3)
            result = self.alu.execute(control_signals["ALUOp"], operand1, operand2)
            self.register_file.write(reg1, result)
        elif opcode.upper() == "AND":
            reg1, reg2, reg3 = map(self._parse_register, operands)
            operand1 = self.register_file.read(reg2)
            operand2 = self.register_file.read(reg3)
            result = self.alu.execute(control_signals["ALUOp"], operand1, operand2)
            self.register_file.write(reg1, result)
        elif opcode.upper() == "OR":
            reg1, reg2, reg3 = map(self._parse_register, operands)
            operand1 = self.register_file.read(reg2)
            operand2 = self.register_file.read(reg3)
            result = self.alu.execute(control_signals["ALUOp"], operand1, operand2)
            self.register_file.write(reg1, result)
        elif opcode.upper() in ["ADDI", "ADDIU", "SLL"]:
            reg1, reg2, imm = self._parse_register(operands[0]), self._parse_register(operands[1]), int(operands[2])
            operand1 = self.register_file.read(reg2)
            result = self.alu.execute(control_signals["ALUOp"], operand1, imm)
            self.register_file.write(reg1, result)
        elif opcode.upper() == "LW":
            reg, offset_reg = self._parse_register(operands[0]), operands[1]
            offset, base_reg = int(offset_reg.split('(')[0]), self._parse_register(offset_reg.split('(')[1][:-1])
            address = self.register_file.read(base_reg) + offset
            value = self.memory.load(address)
            self.register_file.write(reg, value)
        elif opcode.upper() == "SW":
            reg, offset_reg = self._parse_register(operands[0]), operands[1]
            offset, base_reg = int(offset_reg.split('(')[0]), self._parse_register(offset_reg.split('(')[1][:-1])
            address = self.register_file.read(base_reg) + offset
            value = self.register_file.read(reg)
            self.memory.store(address, value)
        elif opcode.upper() == "LUI":
            reg, imm = self._parse_register(operands[0]), int(operands[1], 0)  # Aceitar valor hexadecimal
            self.register_file.write(reg, imm << 16)
            # self._print_to_console(f"Registrador {reg} atualizado com valor {imm << 16} (esperado: {imm} << 16)")
        elif opcode.upper() == "ORI":
            reg1, reg2, imm = self._parse_register(operands[0]), self._parse_register(operands[1]), int(operands[2], 0)  # Aceitar valor hexadecimal
            operand1 = self.register_file.read(reg2)
            result = operand1 | imm
            self.register_file.write(reg1, result)
        elif opcode.upper() == "SLT":
            reg1, reg2, reg3 = map(self._parse_register, operands)
            operand1 = self.register_file.read(reg2)
            operand2 = self.register_file.read(reg3)
            result = 1 if operand1 < operand2 else 0
            self.register_file.write(reg1, result)
        elif opcode.upper() == "SLTI":
            reg1, reg2, imm = self._parse_register(operands[0]), self._parse_register(operands[1]), int(operands[2])
            operand1 = self.register_file.read(reg2)
            result = 1 if operand1 < imm else 0
            self.register_file.write(reg1, result)
        elif opcode.upper() == "J":
            label = operands[0]
            self.jump_to_label(label)
        elif opcode.upper() == "JAL":
            label = operands[0]
            self.register_file.write(31, self.program_counter.get() + 1)  # Salvar o endereço de retorno em $ra
            self.jump_to_label(label)
        elif opcode.upper() == "JR":
            reg = self._parse_register(operands[0])
            address = self.register_file.read(reg)
            self.program_counter.set(address)
        elif opcode.upper() == "SYSCALL":
            self.handle_syscall()
        else:
            raise ValueError("Instrução desconhecida")

    def _parse_register(self, reg):
        if reg.startswith('$'):
            return self.register_file.register_names.index(reg)  # Obter o índice do registrador pelo nome
        return int(reg)

    def get_label_address(self, label):
        if label in self.data_section:
            return self.data_section[label]
        elif label in self.labels:
            return self.labels[label]
        else:
            raise ValueError(f"Label {label} não encontrado")

    def jump_to_label(self, label):
        if label in self.labels:
            self.program_counter.set(self.labels[label])
        else:
            raise ValueError(f"Label {label} não encontrado")

    def handle_syscall(self):
        v0 = self.register_file.read(2)  # $v0 é o registrador 2
        if v0 == 1:  # Imprimir inteiro
            a0 = self.register_file.read(4)  # $a0 é o registrador 4
            self._print_to_console(f"{a0}\n")
        elif v0 == 4:  # Imprimir string
            a0 = self.register_file.read(4)  # $a0 é o registrador 4
            address = a0
            string = ""
            while self.memory.load(address) != 0:
                char = chr(self.memory.load(address))
                if char == '\\':  # Verificar se o caractere é uma barra invertida
                    next_char = chr(self.memory.load(address + 1))
                    if next_char == 'n':
                        string += '\n'
                        address += 2  # Pular a barra invertida e o 'n'
                    elif next_char == 't':
                        string += '\t'
                        address += 2  # Pular a barra invertida e o 't'
                    else:
                        string += char  # Adicionar a barra invertida como está
                        address += 1
                else:
                    string += char
                    address += 1
            self._print_to_console(string)
        elif v0 == 5:  # Ler inteiro
            input_value = int(input("Digite um inteiro: "))
            self.register_file.write(2, input_value)  # Escrever o valor lido em $v0
        elif v0 == 10:  # Sair
            self._print_to_console("Saindo do programa.\n")
            # exit()
        else:
            raise ValueError(f"Syscall {v0} desconhecido\n")

    def _print_to_console(self, message):
        # Função para imprimir no console da interface gráfica
        if hasattr(self, 'output_text'):
            self.output_text.insert(tk.END, f"{message}")
            self.output_text.see(tk.END)

    def translate_to_binary(self, instruction):
        # Implementar a lógica de tradução de instruções para binário
        opcode, *operands = instruction.split()
        opcode = opcode.upper()
        binary_instruction = ""

        # Remover vírgulas dos operandos
        operands = [operand.replace(',', '') for operand in operands]

        if opcode == "ADD":
            binary_instruction = "000000" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[2]) + self._register_to_binary(operands[0]) + "00000" + "100000"
        elif opcode == "SUB":
            binary_instruction = "000000" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[2]) + self._register_to_binary(operands[0]) + "00000" + "100010"
        elif opcode == "MUL":
            binary_instruction = "011100" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[2]) + self._register_to_binary(operands[0]) + "00000" + "000010"
        elif opcode == "AND":
            binary_instruction = "000000" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[2]) + self._register_to_binary(operands[0]) + "00000" + "100100"
        elif opcode == "OR":
            binary_instruction = "000000" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[2]) + self._register_to_binary(operands[0]) + "00000" + "100101"
        elif opcode == "ADDI":
            binary_instruction = "001000" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[0]) + self._immediate_to_binary(operands[2])
        elif opcode == "ADDIU":
            binary_instruction = "001000" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[0]) + self._immediate_to_binary(operands[2])
        elif opcode == "SLL":
            binary_instruction = "000000" + "00000" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[0]) + self._immediate_to_binary(operands[2]) + "000000"
        elif opcode == "LW":
            offset, base_reg = operands[1].split('(')
            base_reg = base_reg[:-1]
            binary_instruction = "100011" + self._register_to_binary(base_reg) + self._register_to_binary(operands[0]) + self._immediate_to_binary(offset)
        elif opcode == "SW":
            offset, base_reg = operands[1].split('(')
            base_reg = base_reg[:-1]
            binary_instruction = "101011" + self._register_to_binary(base_reg) + self._register_to_binary(operands[0]) + self._immediate_to_binary(offset)
        elif opcode == "LUI":
            binary_instruction = "001111" + "00000" + self._register_to_binary(operands[0]) + self._immediate_to_binary(operands[1])
        elif opcode == "ORI":
            binary_instruction = "001101" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[0]) + self._immediate_to_binary(operands[2])
        elif opcode == "SLT":
            binary_instruction = "000000" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[2]) + self._register_to_binary(operands[0]) + "00000" + "101010"
        elif opcode == "SLTI":
            binary_instruction = "001010" + self._register_to_binary(operands[1]) + self._register_to_binary(operands[0]) + self._immediate_to_binary(operands[2])
        elif opcode == "LI":
            binary_instruction = "001000" + self._register_to_binary(operands[0]) + self._register_to_binary(operands[0]) + self._immediate_to_binary(operands[1])
        elif opcode == "LA":
            binary_instruction = "001000" + "00000" + self._register_to_binary(operands[0]) + self._immediate_to_binary(self.get_label_address(operands[1]))
        elif opcode == "J":
            binary_instruction = "000010" + self._address_to_binary(self.get_label_address(operands[0]))
        elif opcode == "JAL":
            binary_instruction = "000011" + self._address_to_binary(self.get_label_address(operands[0]))
        elif opcode == "JR":
            binary_instruction = "000000" + self._register_to_binary(operands[0]) + "000000000000000" + "001000"
        elif opcode == "SYSCALL":
            binary_instruction = "00000000000000000000000000001100"
        else:
            raise ValueError("Instrução desconhecida")

        if len(binary_instruction) > 32:
            binary_instruction = binary_instruction[-32:]  # Remover zeros à esquerda se for maior que 32 bits
        else:
            binary_instruction = binary_instruction.zfill(32)  # Adicionar zeros à esquerda se for menor que 32 bits
        # Formatar o código binário para adicionar espaços a cada quatro dígitos
        formatted_binary_instruction = ' '.join([binary_instruction[i:i+4] for i in range(0, len(binary_instruction), 4)])
        return formatted_binary_instruction

    def _register_to_binary(self, reg):
        reg_num = self._parse_register(reg)
        return format(reg_num, '05b')

    def _immediate_to_binary(self, imm):
        return format(int(imm), '016b')

    def _address_to_binary(self, address):
        return format(address, '026b').lstrip('0')

    def transform_instruction(self, instruction, extra_string):
        opcode, *operands = instruction.split()
        if opcode.upper() == "MOVE":
            reg1, reg2 = operands
            return f"add {reg1} {reg2} $zero", extra_string
        elif opcode.upper() == "LI":
            reg, imm = operands
            return f"addi {reg} {reg} {imm}", extra_string
        elif opcode.upper() == "LA":
            reg, label = operands
            address = self.get_label_address(label)
            upper = (address >> 16) & 0xFFFF
            lower = address & 0xFFFF
            extra_string += "\n"
            if lower != 0:
                return f"LUI {reg}, {upper}\nORI {reg}, {reg}, {lower}", extra_string
            else:
                return f"LUI {reg}, {upper}", extra_string
        return instruction, extra_string

    def get_instruction_with_comments(self, pc):
        if pc < len(self.program):
            return self.program[pc]
        return ""
