import tkinter as tk
from tkinter import filedialog
from src.simulator import Simulator, ProgramCounter


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Simulador MIPS 32 Bits")
        self.simulator = Simulator()
        self.program_counter = ProgramCounter() 
        self.registers_last = [0] * 32
        self.program_path = None
        self.display_mode = tk.StringVar(value="binary")  # Adicionar variável para o modo de exibição
        self.binary_codes = []  # Adicionar array para armazenar códigos binários
        self.hex_codes = []  # Adicionar array para armazenar códigos hexadecimais
        self.register_display_mode = tk.StringVar(value="name")  # Adicionar variável para o modo de exibição dos registradores
        self.create_widgets()
        self.load_last_program()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para os botões
        self.buttons_frame = tk.Frame(main_frame)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)

        self.load_button = tk.Button(self.buttons_frame, text="Carregar Programa", command=self.load_program)
        self.load_button.pack(side=tk.LEFT)

        self.buttons_frame = tk.Frame(main_frame)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)

        # self.datapath_button = tk.Button(self.buttons_frame, text="Mostrar Datapath", command=self.show_datapath_window)
        # self.datapath_button.pack(side=tk.LEFT)

        self.step_button = tk.Button(self.buttons_frame, text="Executar Passo", command=self.step)
        self.step_button.pack(side=tk.LEFT)

        self.run_button = tk.Button(self.buttons_frame, text="Executar Tudo", command=self.run)
        self.run_button.pack(side=tk.LEFT)

        self.reload_button = tk.Button(self.buttons_frame, text="Recarregar Programa", command=self.reload_program)
        self.reload_button.pack(side=tk.LEFT)

        self.load_last_button = tk.Button(self.buttons_frame, text="Carregar Último Programa", command=self.load_last_program)
        self.load_last_button.pack(side=tk.LEFT)

        # Adicionar opção para alternar entre binário e hexadecimal
        self.display_mode_frame = tk.Frame(self.buttons_frame)
        self.display_mode_frame.pack(side=tk.LEFT)

        self.binary_radio = tk.Radiobutton(self.display_mode_frame, text="Binário", variable=self.display_mode, value="binary", command=self.update_code_display)
        self.binary_radio.pack(side=tk.LEFT)

        self.hex_radio = tk.Radiobutton(self.display_mode_frame, text="Hexadecimal", variable=self.display_mode, value="hex", command=self.update_code_display)
        self.hex_radio.pack(side=tk.LEFT)

        # Adicionar opção para alternar entre nome e número dos registradores
        self.register_display_mode_frame = tk.Frame(self.buttons_frame)
        self.register_display_mode_frame.pack(side=tk.LEFT)

        self.name_radio = tk.Radiobutton(self.register_display_mode_frame, text="Nome", variable=self.register_display_mode, value="name", command=self.update_registers_display)
        self.name_radio.pack(side=tk.LEFT)

        self.number_radio = tk.Radiobutton(self.register_display_mode_frame, text="Número", variable=self.register_display_mode, value="number", command=self.update_registers_display)
        self.number_radio.pack(side=tk.LEFT)

        # Frame para os registradores e a linha de código sendo executada
        self.middle_frame = tk.Frame(main_frame)
        self.middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Frame para os registradores
        self.registers_frame = tk.Frame(self.middle_frame)
        self.registers_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.registers_text_col1 = tk.Text(self.registers_frame, height=20, width=12)
        self.registers_text_col1.grid(row=0, column=0)
        self.registers_text_col1.tag_configure("modified", background="red")  # Definir a tag

        self.registers_text_col2 = tk.Text(self.registers_frame, height=20, width=12)
        self.registers_text_col2.grid(row=0, column=1)
        self.registers_text_col2.tag_configure("modified", background="red")  # Definir a tag

        # Frame para a linha de código sendo executada
        self.code_frame = tk.Frame(self.middle_frame)
        self.code_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Adicionar um Text widget para o código binário
        self.binary_text = tk.Text(self.code_frame, height=20, width=45)
        self.binary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Adicionar um Text widget para o código executado
        self.executed_text = tk.Text(self.code_frame, height=20, width=25)
        self.executed_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Adicionar um Text widget para o código do programa
        self.program_text = tk.Text(self.code_frame, height=20, width=40)
        self.program_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adicionar uma scrollbar compartilhada
        self.scrollbar = tk.Scrollbar(self.code_frame, orient="vertical", command=self.sync_scroll)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar os widgets Text para usar a scrollbar
        self.binary_text.config(yscrollcommand=self.scrollbar.set)
        self.executed_text.config(yscrollcommand=self.scrollbar.set)
        self.program_text.config(yscrollcommand=self.scrollbar.set)

        # Bind mouse scroll events to sync_scroll
        self.binary_text.bind("<MouseWheel>", self.on_mouse_wheel)
        self.executed_text.bind("<MouseWheel>", self.on_mouse_wheel)
        self.program_text.bind("<MouseWheel>", self.on_mouse_wheel)

        # Frame para o console
        self.console_frame = tk.Frame(main_frame)
        self.console_frame.pack(side=tk.BOTTOM, fill=tk.X)
        # Adicionar uma scrollbar para o console

        self.console_scrollbar = tk.Scrollbar(self.console_frame)
        self.console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(self.console_frame, height=15)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Configurar o widget Text para usar a scrollbar
        self.output_text.config(yscrollcommand=self.console_scrollbar.set)
        self.console_scrollbar.config(command=self.output_text.yview)

        # Passar a referência do output_text para a instância de Instructions
        self.simulator.instructions.console_output = self.output_text
        self.simulator.instructions.output_text = self.output_text

        self.update_registers_display()  # Inicializar a exibição dos registradores

    def format_message(self, message):
        return f"########## {message} ##########\n"

    def sync_scroll(self, *args):
        self.binary_text.yview(*args)
        self.executed_text.yview(*args)
        self.program_text.yview(*args)

    def on_mouse_wheel(self, event):
        # Ajustar a direção do scroll para Windows
        if event.delta:
            delta = -1 if event.delta > 0 else 1
        else:
            delta = 1 if event.num == 5 else -1

        self.binary_text.yview_scroll(delta, "units")
        self.executed_text.yview_scroll(delta, "units")
        self.program_text.yview_scroll(delta, "units")
        return "break"

    def load_program(self):
        file_path = filedialog.askopenfilename(title="Selecione o arquivo de programa",
                                               filetypes=(("Todos os arquivos", "*.*"), ("Arquivos ASM", "*.asm"), ("Arquivos S", "*.s")))
        if file_path:
            self.program_path = file_path
            self._load_program_from_file(file_path)
    def show_datapath_window(self):
        datapath_window = tk.Toplevel(self.root)
        datapath_window.title("Datapath")

        datapath_label = tk.Label(datapath_window, text="Parte do Datapath usada:")
        datapath_label.pack()

    def reload_program(self):
        if self.program_path:
            self.simulator = Simulator()  # Resetar o simulador
            self._load_program_from_file(self.program_path)
            self.output_text.delete(1.0, tk.END)  # Limpar o console
            self.binary_text.delete(1.0, tk.END)  # Limpar o console de código binário
            self.executed_text.delete(1.0, tk.END)  # Limpar o console de código executado
            self.program_text.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.output_text.insert(tk.END, self.format_message("Programa recarregado."))
            self.update_registers_display()  # Atualizar a exibição dos registradores
            self.clean_registers_diplay()  # Limpar a exibição dos registradores
            self.update_code_arrays()  # Atualizar os arrays de códigos
            self.update_code_display()  # Atualizar a exibição do código
        elif self.simulator.last_program:
            self.simulator.load_program(self.simulator.last_program)
            self.output_text.delete(1.0, tk.END)  # Limpar o console
            self.binary_text.delete(1.0, tk.END)  # Limpar o console de código binário
            self.executed_text.delete(1.0, tk.END)  # Limpar o console de código executado
            self.program_text.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.output_text.insert(tk.END, self.format_message("Último programa recarregado."))
            self.update_registers_display()  # Atualizar a exibição dos registradores
            self.clean_registers_diplay()  # Limpar a exibição dos registradores
            self.update_code_arrays()  # Atualizar os arrays de códigos
            self.update_code_display()  # Atualizar a exibição do código
        else:
            self.output_text.delete(1.0, tk.END)  # Limpar o console
            self.binary_text.delete(1.0, tk.END)  # Limpar o console de código binário
            self.executed_text.delete(1.0, tk.END)  # Limpar o console de código executado
            self.program_text.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.output_text.insert(tk.END, self.format_message("Nenhum programa carregado para recarregar."))

    def _load_program_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:  # Ler o arquivo com codificação UTF-8
            program = file.readlines()
        self.simulator.load_program(program)
        self.output_text.delete(1.0, tk.END)  # Limpar o console
        self.binary_text.delete(1.0, tk.END)  # Limpar o console de código binário
        self.executed_text.delete(1.0, tk.END)  # Limpar o console de código executado
        self.program_text.delete(1.0, tk.END)  # Limpar o console de código do programa
        self.output_text.insert(tk.END, self.format_message(f"Programa {file_path} carregado."))
        self.update_registers_display()  # Atualizar a exibição dos registradores
        self.clean_registers_diplay()  # Limpar a exibição dos registradores
        self.update_code_arrays()  # Atualizar os arrays de códigos
        self.update_code_display()  # Atualizar a exibição do código

    def load_last_program(self):
        if self.simulator.last_program:
            self.simulator.load_program(self.simulator.last_program)
            self.output_text.delete(1.0, tk.END)  # Limpar o console
            self.binary_text.delete(1.0, tk.END)  # Limpar o console de código binário
            self.executed_text.delete(1.0, tk.END)  # Limpar o console de código executado
            self.program_text.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.output_text.insert(tk.END, self.format_message("Último programa carregado."))
            self.update_registers_display()  # Atualizar a exibição dos registradore
            self.clean_registers_diplay()  # Limpar a exibição dos registradores
            self.update_code_arrays()  # Atualizar os arrays de códigos
            self.update_code_display()  # Atualizar a exibição do código
        else:
            self.output_text.delete(1.0, tk.END)  # Limpar o console
            self.binary_text.delete(1.0, tk.END)  # Limpar o console de código binário
            self.executed_text.delete(1.0, tk.END)  # Limpar o console de código executado
            self.program_text.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.output_text.insert(tk.END, self.format_message("Nenhum programa salvo encontrado."))

    def step(self):
        if self.simulator.program_counter.get() >= len(self.simulator.program):
            return
        try:
            self.simulator.step(self.update_registers_display)  # Passar a função de atualização dos registradores
            # self.update_registers_display()  # Atualizar a exibição dos registradores
            self.update_code_display()  # Atualizar a exibição da linha de código sendo executada
            self.root.update_idletasks()  # Forçar a atualização da interface gráfica
            
        except RuntimeError as e:
            self.output_text.insert(tk.END, self.format_message(f"Erro: {e}"))

    def run(self):
        if self.simulator.program_counter.get() >= len(self.simulator.program):
            return
        try:
            while self.simulator.program_counter.get() < len(self.simulator.program):
                self.simulator.step(self.update_registers_display)  # Passar a função de atualização dos registradores
                # self.update_registers_display()  # Atualizar a exibição dos registradores
                self.update_code_display()  # Atualizar a exibição da linha de código sendo executada
                self.root.update_idletasks()  # Forçar a atualização da interface gráfica
            self.output_text.insert(tk.END, self.format_message("Programa executado."))
        except RuntimeError as e:
            self.output_text.insert(tk.END, self.format_message(f"Erro: {e}"))

    def clean_registers_diplay(self):
        self.registers_text_col1.delete(1.0, tk.END)
        self.registers_text_col2.delete(1.0, tk.END)
        self.simulator.instructions.register_file.registers = registers = [0] * 32
        registers = self.simulator.instructions.register_file.registers
        register_names = self.simulator.instructions.register_file.register_names
        for i in range(16):
            if self.register_display_mode.get() == "name":
                text = f"{register_names[i]}: {registers[i]}\n"
            else:
                text = f"${i}: {registers[i]}\n"
            
            self.registers_text_col1.insert(tk.END, text)
        for i in range(16, 32):
            if self.register_display_mode.get() == "name":
                text = f"{register_names[i]}: {registers[i]}\n"
            else:
                text = f"${i}: {registers[i]}\n"
            
            self.registers_text_col2.insert(tk.END, text)
        
    def update_registers_display(self):
        self.registers_text_col1.delete(1.0, tk.END)
        self.registers_text_col2.delete(1.0, tk.END)
        registers = self.simulator.instructions.register_file.registers
        register_names = self.simulator.instructions.register_file.register_names

        for i in range(16):
            if self.register_display_mode.get() == "name":
                text = f"{register_names[i]}: {registers[i]}\n"
            else:
                text = f"${i}: {registers[i]}\n"
            
            self.registers_text_col1.insert(tk.END, text)
            
            # Verificar se o registrador foi modificado e aplicar a tag
            if registers[i] != self.registers_last[i]:
                line_start = f"{i + 1}.0"
                line_end = f"{i + 1}.end"
                self.registers_text_col1.tag_add("modified", line_start, line_end)

        for i in range(16, 32):
            if self.register_display_mode.get() == "name":
                text = f"{register_names[i]}: {registers[i]}\n"
            else:
                text = f"${i}: {registers[i]}\n"
            
            self.registers_text_col2.insert(tk.END, text)
            
            # Verificar se o registrador foi modificado e aplicar a tag
            if registers[i] != self.registers_last[i]:
                line_start = f"{i - 15}.0"
                line_end = f"{i - 15}.end"
                self.registers_text_col2.tag_add("modified", line_start, line_end)

        # Atualizar self.registers_last após todas as comparações
        self.registers_last = registers.copy()
        
        pc = self.program_counter.get() * 4
        self.registers_text_col1.insert(tk.END, f"PC: {pc}\n")
        
    def update_code_arrays(self):
        self.binary_codes = []
        self.hex_codes = []
        for instruction in self.simulator.program:
            binary_instruction = self.simulator.instructions.translate_to_binary(instruction)
            hex_instruction = "0x" + hex(int(binary_instruction.replace(" ", ""), 2))[2:].zfill(8).upper()
            self.binary_codes.append(binary_instruction)
            self.hex_codes.append(hex_instruction)

    def update_code_display(self):
        self.binary_text.delete(1.0, tk.END)
        self.executed_text.delete(1.0, tk.END)
        self.program_text.delete(1.0, tk.END)
        
        if self.display_mode.get() == "binary":
            self.binary_text.config(width=45)
        else: 
            self.binary_text.config(width=20)

        for pc in range(len(self.simulator.program)):
            instruction = self.simulator.program[pc]
            instruction_with_comments = self.simulator.program_with_comments[pc]
            transformed_instruction, instruction_with_comment = self.simulator.instructions.transform_instruction(instruction, instruction_with_comments)
            
            # Aplicar replace separadamente
            transformed_instruction = transformed_instruction.replace('      ', ' ').replace('    ', ' ')
            
            # Exibir a instrução com comentários, seu código binário e a instrução transformada
            if pc < len(self.binary_codes) and pc < len(self.hex_codes):
                if self.display_mode.get() == "binary":
                    self.binary_text.insert(tk.END, f"{self.binary_codes[pc]}\n")
                else:
                    self.binary_text.insert(tk.END, f"{self.hex_codes[pc]}\n")
                self.executed_text.insert(tk.END, f"{transformed_instruction}\n")
                self.program_text.insert(tk.END, f"{instruction_with_comments}\n")
        self.binary_text.see(tk.END)  # Rolagem automática para a última linha
        self.executed_text.see(tk.END)  # Rolagem automática para a última linha
        self.program_text.see(tk.END)  # Rolagem automática para a última linha

        # Destacar a linha de código sendo executada
        pc = self.simulator.program_counter.get() - 1
        if pc >= 0 and pc < len(self.simulator.program):
            self.program_text.tag_remove("highlight", "1.0", tk.END)
            self.program_text.tag_add("highlight", f"{pc + 1}.0", f"{pc + 1}.end+1c")
            self.program_text.tag_configure("highlight", background="#d3d3d3")
            self.program_text.see(f"{pc + 1}.0")
            self.binary_text.tag_remove("highlight", "1.0", tk.END)
            self.binary_text.tag_add("highlight", f"{pc + 1}.0", f"{pc + 1}.end+1c")
            self.binary_text.tag_configure("highlight", background="#d3d3d3")
            self.binary_text.see(f"{pc + 1}.0")
            self.executed_text.tag_remove("highlight", "1.0", tk.END)
            self.executed_text.tag_add("highlight", f"{pc + 1}.0", f"{pc + 1}.end+1c")
            self.executed_text.tag_configure("highlight", background="#d3d3d3")
            self.executed_text.see(f"{pc + 1}.0")
            

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()