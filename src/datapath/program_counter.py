from src.datapath.adder import Adder

class ProgramCounter:
    def __init__(self):
        self.pc = 0  # Inicializa o PC com 0
        self.adder = Adder()  # Adiciona uma instância do Adder

    def increment(self):
        self.pc = self.adder.increment(self.pc, 1)  # Usa o Adder para incrementar o PC

    def set(self, value):
        self.pc = value  # Define o PC para um valor específico

    def get(self):
        return self.pc  # Retorna o valor atual do PC
