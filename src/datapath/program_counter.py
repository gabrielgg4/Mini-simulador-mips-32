from src.datapath.adder import Adder

class ProgramCounter:
    # Faz a função de PC, que no caso é simples pq não tem nenhuma função do tipo J implemetada
    def __init__(self):
        self.pc = 0  
        self.adder = Adder()  

    def incrementar(self):
        self.pc = self.adder.incrementar(self.pc, 1)

    def set(self, valor):
        self.pc = valor

    def get(self):
        return self.pc
