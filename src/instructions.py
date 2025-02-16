from src.datapath.alu import ALU
from src.datapath.control_unit import ControlUnit
from src.datapath.memory import Memory
from src.datapath.registers import Registers
import tkinter as tk

class Instructions:
    def __init__(self, program_counter):
        self.alu = ALU()
        self.control_unit = ControlUnit()
        self.memoria = Memory(4096)
        self.registers = Registers()
        self.labels = {}
        self.selecao_data = {}
        self.program_counter = program_counter
        self.programa = []

    def executar(self, instrucao):
        instrucao = instrucao.split('#')[0].strip() # Aqui ele remove os espacos em branco strip()
                                                    # e o que tiver depois do # (split)
        if not instrucao:
            return

        # Separa a instrução em partes pelos espaços
        # então codigin_operacao recebe a primeira parte da instrução
        # e operandos recebe um array com o resto 
        codigo_operacao, *operandos = instrucao.split()
        if not codigo_operacao:
            return

        #Tira as virgulas dos registradores
        operandos = [op.replace(',', '').strip() for op in operandos]

        # Isso aqui é meio meme pq literalmente ele pede pra control_unit
        # buscar o codigo da operacao, que é o mesmo que ele já tem
        sinais_controle = self.control_unit.decode(codigo_operacao.upper())
        operandos = [op.replace(',', '').strip() for op in operandos] # Tira as virgulas dos registradores
        print(f"Executando instrução: {instrucao}")

        if codigo_operacao.upper() == "ADD":
            #Tranforma os registradores em indices
            reg1, reg2, reg3 = map(self._tranformar_registrador, operandos)
            op1 = self.registers.ler(reg2)
            op2 = self.registers.ler(reg3)
            # Manda a ALU fazer a opercao
            resultado = self.alu.executar(sinais_controle["ALUOp"], op1, op2)
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() == "SUB":
            reg1, reg2, reg3 = map(self._tranformar_registrador, operandos)
            op1 = self.registers.ler(reg2)
            op2 = self.registers.ler(reg3)
            resultado = self.alu.executar(sinais_controle["ALUOp"], op1, op2)
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() == "MUL":
            reg1, reg2, reg3 = map(self._tranformar_registrador, operandos)
            op1 = self.registers.ler(reg2)
            op2 = self.registers.ler(reg3)
            resultado = self.alu.executar(sinais_controle["ALUOp"], op1, op2)
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() == "AND":
            reg1, reg2, reg3 = map(self._tranformar_registrador, operandos)
            op1 = self.registers.ler(reg2)
            op2 = self.registers.ler(reg3)
            resultado = self.alu.executar(sinais_controle["ALUOp"], op1, op2)
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() == "OR":
            reg1, reg2, reg3 = map(self._tranformar_registrador, operandos)
            op1 = self.registers.ler(reg2)
            op2 = self.registers.ler(reg3)
            resultado = self.alu.executar(sinais_controle["ALUOp"], op1, op2)
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() in ["ADDI", "ADDIU", "SLL"]:
            reg1, reg2, imm = self._tranformar_registrador(operandos[0]), self._tranformar_registrador(operandos[1]), int(operandos[2])
            op1 = self.registers.ler(reg2)
            resultado = self.alu.executar(sinais_controle["ALUOp"], op1, imm)
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() == "LW":
            reg = self._tranformar_registrador(operandos[0])
            offset, base = self._analisar_offset_e_registrador(operandos[1])
            endereco = self.registers.ler(base) + offset
            valor = self.memoria.ler(endereco)
            self.registers.escrever(reg, valor)

        elif codigo_operacao.upper() == "SW":
            reg = self._tranformar_registrador(operandos[0])
            offset, base = self._analisar_offset_e_registrador(operandos[1])
            endereco = self.registers.ler(base) + offset
            valor = self.registers.ler(reg)
            self.memoria.armazenar(endereco, valor)

        elif codigo_operacao.upper() == "LUI":
            # Esse int(operandos[1], 0) já tranforma se for em hexadecimal ou int normal
            reg, imm = self._tranformar_registrador(operandos[0]), int(operandos[1], 0)
            self.registers.escrever(reg, imm << 16)

        elif codigo_operacao.upper() == "ORI":
            reg1, reg2, imm = self._tranformar_registrador(operandos[0]), self._tranformar_registrador(operandos[1]), int(operandos[2], 0)
            op1 = self.registers.ler(reg2)
            # op1: 0101 (binarui0
            # imm: 0011
            # 
            # resultado: 0111
            resultado = op1 | imm
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() == "SLT":
            reg1, reg2, reg3 = map(self._tranformar_registrador, operandos)
            op1 = self.registers.ler(reg2)
            op2 = self.registers.ler(reg3)
            resultado = 1 if op1 < op2 else 0
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() == "SLTI":
            reg1, reg2, imm = self._tranformar_registrador(operandos[0]), self._tranformar_registrador(operandos[1]), int(operandos[2])
            op1 = self.registers.ler(reg2)
            resultado = 1 if op1 < imm else 0
            self.registers.escrever(reg1, resultado)

        elif codigo_operacao.upper() == "SYSCALL":
            self.tratar_syscall()
        else:
            raise ValueError("Instrução desconhecida")

    def _tranformar_registrador(self, reg):
        if reg.startswith('$'):
            return self.registers.register_names.index(reg)
        return int(reg)

    def get_endereco(self, label):
        if label in self.selecao_data:
             return self.selecao_data[label]
        elif label in self.labels:
            return self.labels[label]
        else:
            raise ValueError(f"Label {label} não encontrado")

    def pular_para_label(self, label):
        if label in self.labels:
            self.program_counter.definir(self.labels[label])
        else:
            raise ValueError(f"Label {label} não encontrado")

    def tratar_syscall(self):
        print("Executando syscall")
        v0 = self.registers.ler(2)
        if v0 == 1:
            a0 = self.registers.ler(4)
            self._imprimir_no_console(f"{a0}\n")
        elif v0 == 4:
            a0 = self.registers.ler(4)
            endereco = a0
            texto = ""
            while self.memoria.ler(endereco) != 0:
                char = chr(self.memoria.ler(endereco))
                if char == '\\':
                    prox = chr(self.memoria.ler(endereco + 1))
                    if prox == 'n':
                        texto += '\n'
                        endereco += 2
                    elif prox == 't':
                        texto += '\t'
                        endereco += 2
                    else:
                        texto += char
                        endereco += 1
                else:
                    texto += char
                    endereco += 1
            self._imprimir_no_console(texto)
        elif v0 == 5:
            entrada = int(input("Digite um inteiro: "))
            self.registers.escrever(2, entrada)
        elif v0 == 10:
            self._imprimir_no_console("------ Saindo do programa. ------\n")
        else:
            raise ValueError(f"Syscall {v0} desconhecido\n")

    def _imprimir_no_console(self, mensagem):
        if hasattr(self, 'texto_output'):
            self.texto_output.insert(tk.END, f"{mensagem}")
            self.texto_output.see(tk.END)

    def traduzir_para_binario(self, instrucao):
        codigo_operacao, *operandos = instrucao.split()
        codigo_operacao = codigo_operacao.upper()
        binario = ""
        operandos = [op.replace(',', '') for op in operandos]
        if codigo_operacao == "ADD":
            binario = "000000" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[2]) + self._registrador_para_binario(operandos[0]) + "00000" + "100000"
        elif codigo_operacao == "SUB":
            binario = "000000" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[2]) + self._registrador_para_binario(operandos[0]) + "00000" + "100010"
        elif codigo_operacao == "MUL":
            binario = "011100" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[2]) + self._registrador_para_binario(operandos[0]) + "00000" + "000010"
        elif codigo_operacao == "AND":
            binario = "000000" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[2]) + self._registrador_para_binario(operandos[0]) + "00000" + "100100"
        elif codigo_operacao == "OR":
            binario = "000000" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[2]) + self._registrador_para_binario(operandos[0]) + "00000" + "100101"
        elif codigo_operacao == "SLL":
            binario = "000000" + "00000" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(operandos[2]) + "000000"
        elif codigo_operacao == "SLT":
            binario = "000000" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[2]) + self._registrador_para_binario(operandos[0]) + "00000" + "101010"
        elif codigo_operacao == "SYSCALL":
            binario = "00000000000000000000000000001100"
        elif codigo_operacao == "LW":
            offset, base = operandos[1].split('(')
            base = base[:-1]
            binario = "100011" + self._registrador_para_binario(base) + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(offset)
        elif codigo_operacao == "SW":
            offset, base = operandos[1].split('(')
            base = base[:-1]
            binario = "101011" + self._registrador_para_binario(base) + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(offset)
        elif codigo_operacao == "ADDI":
            binario = "001000" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(operandos[2])
        elif codigo_operacao == "ADDIU":
            binario = "001001" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(operandos[2])
        elif codigo_operacao == "LUI":
            binario = "001111" + "00000" + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(operandos[1])
        elif codigo_operacao == "ORI":
            binario = "001101" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(operandos[2])
        elif codigo_operacao == "SLTI":
            binario = "001010" + self._registrador_para_binario(operandos[1]) + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(operandos[2])
        elif codigo_operacao == "LI":
            binario = "001000" + self._registrador_para_binario(operandos[0]) + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(operandos[1])
        elif codigo_operacao == "LA":
            binario = "001000" + "00000" + self._registrador_para_binario(operandos[0]) + self._imediato_para_binario(self.get_endereco(operandos[1]))
        else:
            raise ValueError("Instrução não disponivel: " + codigo_operacao)

        if len(binario) > 32:
            binario = binario[-32:]
        else:
            binario = binario.zfill(32)
        formato = ' '.join([binario[i:i+4] for i in range(0, len(binario), 4)])
        return formato

    def _registrador_para_binario(self, reg):
        num = self._tranformar_registrador(reg)
        return format(num, '05b')

    def _imediato_para_binario(self, imm):
        return format(int(imm), '016b')

    def _endereco_para_binario(self, endereco):
        return format(endereco, '026b').lstrip('0')

    def transformar_instrucao(self, instrucao, extra):
        codigo_operacao, *operandos = instrucao.split()
        if codigo_operacao.upper() == "MOVE":
            reg1, reg2 = operandos
            return f"add {reg1} {reg2} $zero", extra
        elif codigo_operacao.upper() == "LI":
            reg, imm = operandos
            return f"addi {reg} {reg} {imm}", extra
        elif codigo_operacao.upper() == "LA":
            reg, label = operandos
            endereco = self.get_endereco(label)
            upper = (endereco >> 16) & 0xFFFF
            lower = endereco & 0xFFFF
            extra += "\n"
            if lower != 0:
                return f"LUI {reg}, {upper}\nORI {reg}, {reg}, {lower}", extra
            else:
                return f"LUI {reg}, {upper}", extra
        return instrucao, extra
    
    def _analisar_offset_e_registrador(self, offset_com_registrador):
        # Espera uma string no formato numero(registrador)
        string_offset, resto = offset_com_registrador.split('(')
        offset = int(string_offset)
        string_registrador = resto.rstrip(')')  
        indice_registrador = self._tranformar_registrador(string_registrador)
        return offset, indice_registrador