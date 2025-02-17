import pickle
import os
from src.instructions import Instructions
from src.datapath.program_counter import ProgramCounter

class Simulator:
    def __init__(self):
        self.program_counter = ProgramCounter()
        self.instructions = Instructions(self.program_counter)
        self.programa = []
        self.programa_com_comentarios = []  
        self.selecao_data = {}
        self.arquivo_ultimo_programa = os.path.join("data", "ultimo_programa.pkl")
        self.carregar_ultimo_programa()

    def carregar_programa(self, programa):
        # Reseta tudo e dps salva o programa
        self.programa = []
        self.programa_com_comentarios = [] 
        self.selecao_data = {}
        self.instructions.labels = {}  
        self.program_counter.set(0)
        self.instructions.registers.reiniciar()  
        self.ultimo_programa = programa  
        self.salvar_ultimo_programa()

        in_data_section = False
        in_text_section = False
        data_endereco = 0  
        
        for line in programa:
            linha_com_cometarios = line.strip()
            line = line.split('#')[0].strip()  # Remover comentários e espaços em branco
            if not line:
                continue
            if line == ".data":
                in_data_section = True
                in_text_section = False
            elif line == ".text":
                in_data_section = False
                in_text_section = True
            elif in_data_section:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    label, value = parts
                    label = label.strip()
                    value = value.strip()
                    if value.lstrip().startswith('.word'):
                        value = value.lstrip()
                        # Pega os valores inteiros da linha,
                        # faz começar pelo 5 pra tirar o .word
                        values = list(map(int, value[5:].strip().split(',')))
                        self.selecao_data[label] = data_endereco
                        print(f"Label {label} armazenado no endereço {data_endereco}")  #
                        for val in values:
                            self.instructions.memoria.armazenar(data_endereco, val)
                            data_endereco += 4
                    elif value.lstrip().startswith('.asciiz'):
                        value = value.lstrip()
                        # Pega só oque está dentro do " "
                        string = value[7:].strip().strip('"')
                        self.selecao_data[label] = data_endereco
                        print(f"Label {label} armazenado no endereço {data_endereco}")  
                        for char in string:
                            self.instructions.memoria.armazenar(data_endereco, ord(char))
                            data_endereco += 1
                        self.instructions.memoria.armazenar(data_endereco, 0) # Terminador de string
                        data_endereco += 1
                self.instructions.selecao_data = self.selecao_data
            elif in_text_section:
                # Esse if trata se estiver na linha que ta declarando a label 
                # tipo se tiver assim: main:   add $t0, $t1, $t2
                if ':' in line:
                    label, instrucao = line.split(':', 1)
                    label = label.strip()
                    instrucao = instrucao.strip()
                    self.instructions.labels[label] = len(self.programa)
                    if instrucao:
                        if instrucao.upper().startswith("MOVE"):
                            parts = instrucao.split()
                            reg1, reg2 = parts[1], parts[2]
                            instrucao = f"add {reg1}, {reg2}, $zero"
                        elif instrucao.upper().startswith("LI"):
                            parts = instrucao.split()
                            reg, imm = parts[1], parts[2]
                            instrucao = f"addi {reg}, $zero, {imm}"
                        elif instrucao.upper().startswith("LA"):
                            parts = instrucao.split()
                            reg, label = parts[1], parts[2]
                            address = self.instructions.get_endereco(label)
                            upper = (address >> 16) & 0xFFFF
                            lower = address & 0xFFFF
                            self.programa.append(f"lui {reg}, {upper}")
                            self.programa_com_comentarios.append(linha_com_cometarios)
                            self.programa.append(f"ori {reg}, {reg}, {lower}")
                            self.programa_com_comentarios.append("                                    # Instrucão alterada")
                            continue
                        self.programa.append(instrucao)
                        self.programa_com_comentarios.append(linha_com_cometarios)
                else:
                    if line.upper().startswith("MOVE"):
                        parts = line.split()
                        reg1, reg2 = parts[1], parts[2]
                        line = f"add {reg1} {reg2}, $zero"
                    elif line.upper().startswith("LI"):
                        parts = line.split()
                        reg, imm = parts[1], parts[2]
                        line = f"addi {reg} $zero, {imm}"
                    elif line.upper().startswith("LA"):
                        parts = line.split()
                        reg, label = parts[1], parts[2]
                        address = self.instructions.get_endereco(label)
                        upper = (address >> 16) & 0xFFFF
                        lower = address & 0xFFFF
                        self.programa.append(f"lui {reg} {upper}")
                        self.programa_com_comentarios.append(linha_com_cometarios)
                        self.programa.append(f"ori {reg} {reg} {lower}")
                        self.programa_com_comentarios.append("                                    # Instrucão alterada")
                        continue
                    self.programa.append(line)
                    self.programa_com_comentarios.append(linha_com_cometarios)
        self.instructions.selecao_data = self.selecao_data 
        self.instructions.labels = self.instructions.labels 
        self.instructions.programa = self.programa  
        self.program_counter.set(0) 

    def passo(self, atualizar_registradores=None):
        if not self.programa:
            raise RuntimeError("Nenhum programa carregado.")
        pc = self.program_counter.get()
        if pc < len(self.programa):
            instrucao = self.programa[pc]
            print(f"Executando instrução: {instrucao}")
            self.instructions.executar(instrucao)
            self.program_counter.incrementar()  
            if atualizar_registradores:
                atualizar_registradores()  
        else:
            print("Fim do programa.")

    def executar(self):
        if not self.programa:
            raise RuntimeError("Nenhum programa carregado.")
        while self.program_counter.get() < len(self.programa):
            self.passo()

    def salvar_ultimo_programa(self):
        # Cria pasta se não existir
        os.makedirs(os.path.dirname(self.arquivo_ultimo_programa), exist_ok=True)
        # Abre o arquivo
        with open(self.arquivo_ultimo_programa, 'wb') as file:
            # Salva o último programa
            pickle.dump(self.ultimo_programa, file)

    def carregar_ultimo_programa(self):
        try:
            print(f"Carregando último programa de {self.arquivo_ultimo_programa}")	
            with open(self.arquivo_ultimo_programa, 'rb') as file:
                self.ultimo_programa = pickle.load(file)
        except FileNotFoundError:
            self.ultimo_programa = None
