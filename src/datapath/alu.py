class ALU:
    def __init__(self):
        self.result = 0
        self.zero = 0

    def execute(self, operation, operand1, operand2):
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
        
        self.zero = 1 if self.result == 0 else 0
        return self.result
