class Memory:
    # Simula a memoria do MIPS, armazenando as coisas em um array
    def __init__(self, tamanho):
        self.memoria = [0] * tamanho

    def ler(self, endereco):
        return self.memoria[endereco]

    def armazenar(self, endereco, valor):
        self.memoria[endereco] = valor
