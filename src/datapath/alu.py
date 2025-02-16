class ALU:
    def __init__(self):
        self.result = 0
        # Função faz os calculos que a ALU faria no MIPS 
    def executar(self, operation, operand1, operand2):
        #ADD  ADDI   SUB  MUL   AND  OR  SLL
        if operation == "ADD":
            self.result = operand1 + operand2
        elif operation == "ADDI":
            self.result = operand1 + operand2
        elif operation == "SUB":
            self.result = operand1 - operand2
        elif operation == "MUL":
            self.result = operand1 * operand2    
        elif operation == "AND":
            self.result = operand1 & operand2
        elif operation == "OR":
            self.result = operand1 | operand2
        elif operation == "SLL":
            self.result = operand1 << operand2
        else:
            raise ValueError("Operação desconhecida")
        
        return self.result
