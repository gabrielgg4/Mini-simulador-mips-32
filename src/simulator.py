import pickle
import os
from src.instructions import Instructions
from src.datapath.program_counter import ProgramCounter

class Simulator:
    def __init__(self):
        self.program_counter = ProgramCounter()
        self.instructions = Instructions(self.program_counter)
        self.program = []
        self.program_with_comments = []  # Adicionar lista para armazenar instruções com comentários
        self.data_section = {}
        self.last_program_file = os.path.join("data", "last_program.pkl")
        self.load_last_program()

    def load_program(self, program):
        self.program = []
        self.program_with_comments = []  # Resetar a lista de instruções com comentários
        self.data_section = {}
        self.instructions.labels = {}  # Resetar os labels
        self.program_counter.set(0)  # Resetar o PC ao carregar um novo programa
        self.instructions.register_file.reset()  # Resetar todos os registradores
        self.last_program = program  # Armazenar o último programa carregado
        self.save_last_program()

        in_data_section = False
        in_text_section = False
        data_address = 100  # Garantir que os endereços de memória da seção .data comecem a partir de 100

        for line in program:
            # Manter os comentários ao armazenar as instruções
            line_with_comments = line.strip()
            line = line.split('#')[0].strip()  # Remover comentários e espaços em branco
            if not line:  # Ignorar linhas em branco
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
                        values = list(map(int, value[5:].strip().split(',')))
                        self.data_section[label] = data_address
                        print(f"Label {label} armazenado no endereço {data_address}")  # Exibir endereço de memória
                        # Carregar os valores na memória
                        for val in values:
                            self.instructions.memory.store(data_address, val)
                            data_address += 4
                    elif value.lstrip().startswith('.asciiz'):
                        value = value.lstrip()
                        string = value[7:].strip().strip('"')
                        self.data_section[label] = data_address
                        print(f"Label {label} armazenado no endereço {data_address}")  # Exibir endereço de memória
                        # Carregar a string na memória
                        for char in string:
                            self.instructions.memory.store(data_address, ord(char))
                            data_address += 1
                        self.instructions.memory.store(data_address, 0)  # Null terminator
                        data_address += 1
                self.instructions.data_section = self.data_section
            elif in_text_section:
                if ':' in line:
                    label, instruction = line.split(':', 1)
                    label = label.strip()
                    instruction = instruction.strip()
                    self.instructions.labels[label] = len(self.program)
                    if instruction:
                        # Transformar MOVE para ADD $t1, $t2, $zero
                        if instruction.upper().startswith("MOVE"):
                            parts = instruction.split()
                            reg1, reg2 = parts[1], parts[2]
                            instruction = f"add {reg1}, {reg2}, $zero"
                        # Transformar LI para ADDI
                        elif instruction.upper().startswith("LI"):
                            parts = instruction.split()
                            reg, imm = parts[1], parts[2]
                            instruction = f"addi {reg}, $zero, {imm}"
                        # Transformar LA para LUI e ORI
                        elif instruction.upper().startswith("LA"):
                            parts = instruction.split()
                            reg, label = parts[1], parts[2]
                            address = self.instructions.get_label_address(label)
                            upper = (address >> 16) & 0xFFFF
                            lower = address & 0xFFFF
                            self.program.append(f"lui {reg}, {upper}")
                            self.program_with_comments.append(line_with_comments)
                            self.program.append(f"ori {reg}, {reg}, {lower}")
                            self.program_with_comments.append(line_with_comments)
                            continue
                        self.program.append(instruction)
                        self.program_with_comments.append(line_with_comments)
                else:
                    # Transformar MOVE para ADD $t1, $t2, $zero
                    if line.upper().startswith("MOVE"):
                        parts = line.split()
                        reg1, reg2 = parts[1], parts[2]
                        line = f"add {reg1} {reg2}, $zero"
                    # Transformar LI para ADDI
                    elif line.upper().startswith("LI"):
                        parts = line.split()
                        reg, imm = parts[1], parts[2]
                        line = f"addi {reg} $zero, {imm}"
                    # Transformar LA para LUI e ORI
                    elif line.upper().startswith("LA"):
                        parts = line.split()
                        reg, label = parts[1], parts[2]
                        address = self.instructions.get_label_address(label)
                        upper = (address >> 16) & 0xFFFF
                        lower = address & 0xFFFF
                        self.program.append(f"lui {reg} {upper}")
                        self.program_with_comments.append(line_with_comments)
                        self.program.append(f"ori {reg} {reg} {lower}")
                        self.program_with_comments.append(line_with_comments)
                        continue
                    self.program.append(line)
                    self.program_with_comments.append(line_with_comments)
        self.instructions.data_section = self.data_section  # Ensure data_section is passed to instructions
        self.instructions.labels = self.instructions.labels  # Ensure labels are passed to instructions
        self.instructions.program = self.program  # Ensure program is passed to instructions
        self.program_counter.set(0)  # Reset the program counter to the start of the program

    def step(self, update_registers_callback=None):
        if not self.program:
            raise RuntimeError("Nenhum programa carregado.")
        pc = self.program_counter.get()
        if pc < len(self.program):
            instruction = self.program[pc]
            print(f"Executando instrução: {instruction}")
            self.instructions.execute(instruction)
            self.program_counter.increment()  # Incrementa o PC após a execução da instrução
            if update_registers_callback:
                update_registers_callback()  # Chamar a função de atualização dos registradores
        else:
            print("Fim do programa.")

    def run(self):
        if not self.program:
            raise RuntimeError("Nenhum programa carregado.")
        while self.program_counter.get() < len(self.program):
            self.step()

    def save_last_program(self):
        os.makedirs(os.path.dirname(self.last_program_file), exist_ok=True)
        with open(self.last_program_file, 'wb') as file:
            pickle.dump(self.last_program, file)

    def load_last_program(self):
        try:
            with open(self.last_program_file, 'rb') as file:
                self.last_program = pickle.load(file)
        except FileNotFoundError:
            self.last_program = None
