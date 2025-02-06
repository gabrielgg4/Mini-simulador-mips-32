class ControlUnit:
    def __init__(self):
        self.control_signals = {}

    def decode(self, opcode):
        print(f"Decodificando opcode: {opcode}")  # Log de depuração
        # Definir sinais de controle com base no opcode
        if opcode == "ADD":
            self.control_signals = {"ALUOp": "ADD", "RegWrite": 1}
        elif opcode == "ADDI":
            self.control_signals = {"ALUOp": "ADDI", "RegWrite": 1}
        elif opcode == "ADDIU":
            self.control_signals = {"ALUOp": "ADDIU", "RegWrite": 1}    
        elif opcode == "SUB":
            self.control_signals = {"ALUOp": "SUB", "RegWrite": 1}
        elif opcode == "MUL":
            self.control_signals = {"ALUOp": "MUL", "RegWrite": 1}
        elif opcode == "AND":
            self.control_signals = {"ALUOp": "AND", "RegWrite": 1}
        elif opcode == "OR":
            self.control_signals = {"ALUOp": "OR", "RegWrite": 1}
        elif opcode == "SLL":
            self.control_signals = {"ALUOp": "SLL", "RegWrite": 1}
        elif opcode == "LW":
            self.control_signals = {"ALUOp": "LW", "MemRead": 1, "RegWrite": 1}
        elif opcode == "SW":
            self.control_signals = {"ALUOp": "SW", "MemWrite": 1}
        elif opcode == "LUI":
            self.control_signals = {"ALUOp": "LUI", "RegWrite": 1}
        elif opcode == "SLT":
            self.control_signals = {"ALUOp": "SLT", "RegWrite": 1}
        elif opcode == "SLTI":
            self.control_signals = {"ALUOp": "SLTI", "RegWrite": 1}
        elif opcode == "SYSCALL":
            self.control_signals = {"ALUOp": "SYSCALL"}
        elif opcode == "ORI":
            self.control_signals = {"ALUOp": "ORI", "RegWrite": 1}
        else:
            raise ValueError("Opcode desconhecido")
        
        return self.control_signals
