class Memory:
    def __init__(self, size):
        self.memory = [0] * size  # Inicializar a memória com o tamanho especificado

    def load(self, address):
        return self.memory[address]

    def store(self, address, value):
        self.memory[address] = value
