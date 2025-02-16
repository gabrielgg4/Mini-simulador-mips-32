import tkinter as tk
from tkinter import filedialog
from src.simulator import Simulator, ProgramCounter


class JanelaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("mini simulador mips 32 bits")
        self.simulator = Simulator()
        self.program_counter = ProgramCounter() 
        self.registradores_antigos = [0] * 32
        self.caminho_programa = None
        self.modo_codigos = tk.StringVar(value="binary")  # adicionar variavel para o modo de exibicao
        self.codigos_binarios = []  # adicionar array para armazenar codigos binarios
        self.codigos_hexa = []  # adicionar array para armazenar codigos hexadecimais
        self.modo_registradores = tk.StringVar(value="name")  # adicionar variavel para o modo de exibicao dos registradores
        self.create_widgets()
        self.carregar_ultimo_programa()

    def create_widgets(self):
        # frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # frame para os botoes
        self.frame_botoes = tk.Frame(main_frame)
        self.frame_botoes.pack(side=tk.TOP, fill=tk.X)

        self.botao_load = tk.Button(self.frame_botoes, text="carregar programa", command=self.carregar_programa)
        self.botao_load.pack(side=tk.LEFT)

        self.frame_botoes = tk.Frame(main_frame)
        self.frame_botoes.pack(side=tk.TOP, fill=tk.X)

        # self.datapath_button = tk.Button(self.frame_botoes, text="mostrar datapath", command=self.show_datapath_window)
        # self.datapath_button.pack(side=tk.LEFT)

        self.botao_passo = tk.Button(self.frame_botoes, text="executar passo", command=self.step)
        self.botao_passo.pack(side=tk.LEFT)

        self.botao_run = tk.Button(self.frame_botoes, text="Executar Tudo", command=self.run)
        self.botao_run.pack(side=tk.LEFT)

        self.botao_recarregar = tk.Button(self.frame_botoes, text="Recarregar Programa", command=self.recarregar_programa)
        self.botao_recarregar.pack(side=tk.LEFT)

        self.load_last_button = tk.Button(self.frame_botoes, text="Carregar Último Programa", command=self.carregar_ultimo_programa)
        self.load_last_button.pack(side=tk.LEFT)

        # Adicionar opção para alternar entre binário e hexadecimal
        self.modo_dos_codigos = tk.Frame(self.frame_botoes)
        self.modo_dos_codigos.pack(side=tk.LEFT)

        self.binary_radio = tk.Radiobutton(self.modo_dos_codigos, text="Binário", variable=self.modo_codigos, value="binary", command=self.atualizar_codigos_display)
        self.binary_radio.pack(side=tk.LEFT)

        self.hex_radio = tk.Radiobutton(self.modo_dos_codigos, text="Hexadecimal", variable=self.modo_codigos, value="hex", command=self.atualizar_codigos_display)
        self.hex_radio.pack(side=tk.LEFT)

        # Adicionar opção para alternar entre nome e número dos registradores
        self.register_display_mode_frame = tk.Frame(self.frame_botoes)
        self.register_display_mode_frame.pack(side=tk.LEFT)

        self.name_radio = tk.Radiobutton(self.register_display_mode_frame, text="Nome", variable=self.modo_registradores, value="name", command=self.atualizar_registradores)
        self.name_radio.pack(side=tk.LEFT)

        self.number_radio = tk.Radiobutton(self.register_display_mode_frame, text="Número", variable=self.modo_registradores, value="number", command=self.atualizar_registradores)
        self.number_radio.pack(side=tk.LEFT)

        # Frame para os registradores e a linha de código sendo executada
        self.middle_frame = tk.Frame(main_frame)
        self.middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Frame para os registradores
        self.frame_registradores = tk.Frame(self.middle_frame)
        self.frame_registradores.pack(side=tk.LEFT, fill=tk.Y)

        self.registers_text_col1 = tk.Text(self.frame_registradores, height=20, width=12)
        self.registers_text_col1.grid(row=0, column=0)
        self.registers_text_col1.tag_configure("modified", background="red")  # Definir a tag

        self.registers_text_col2 = tk.Text(self.frame_registradores, height=20, width=12)
        self.registers_text_col2.grid(row=0, column=1)
        self.registers_text_col2.tag_configure("modified", background="red")  # Definir a tag

        # Frame para a linha de código sendo executada
        self.code_frame = tk.Frame(self.middle_frame)
        self.code_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Adicionar um Text widget para o código binário
        self.texto_binario = tk.Text(self.code_frame, height=20, width=45)
        self.texto_binario.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Adicionar um Text widget para o código executado
        self.texto_executado = tk.Text(self.code_frame, height=20, width=25)
        self.texto_executado.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Adicionar um Text widget para o código do programa
        self.texto_do_programa = tk.Text(self.code_frame, height=20, width=40)
        self.texto_do_programa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adicionar uma scrollbar compartilhada
        self.scrollbar = tk.Scrollbar(self.code_frame, orient="vertical", command=self.sincronizar_scroll)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar os widgets Text para usar a scrollbar
        self.texto_binario.config(yscrollcommand=self.scrollbar.set)
        self.texto_executado.config(yscrollcommand=self.scrollbar.set)
        self.texto_do_programa.config(yscrollcommand=self.scrollbar.set)

        # Bind mouse scroll events to sincronizar_scroll
        self.texto_binario.bind("<MouseWheel>", self.on_mouse_wheel)
        self.texto_executado.bind("<MouseWheel>", self.on_mouse_wheel)
        self.texto_do_programa.bind("<MouseWheel>", self.on_mouse_wheel)

        # Frame para o console
        self.console_frame = tk.Frame(main_frame)
        self.console_frame.pack(side=tk.BOTTOM, fill=tk.X)
        # Adicionar uma scrollbar para o console

        self.console_scrollbar = tk.Scrollbar(self.console_frame)
        self.console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.texto_output = tk.Text(self.console_frame, height=15)
        self.texto_output.pack(fill=tk.BOTH, expand=True)

        # Configurar o widget Text para usar a scrollbar
        self.texto_output.config(yscrollcommand=self.console_scrollbar.set)
        self.console_scrollbar.config(command=self.texto_output.yview)

        # Passar a referência do texto_output para a instância de Instructions
        self.simulator.instructions.console_output = self.texto_output
        self.simulator.instructions.texto_output = self.texto_output

        self.atualizar_registradores()  # Inicializar a exibição dos registradores

    def formatar_mensagens(self, message):
        return f"########## {message} ##########\n"

    def sincronizar_scroll(self, *args):
        self.texto_binario.yview(*args)
        self.texto_executado.yview(*args)
        self.texto_do_programa.yview(*args)

    def on_mouse_wheel(self, event):
        if event.delta:
            delta = -1 if event.delta > 0 else 1
        else:
            delta = 1 if event.num == 5 else -1

        self.texto_binario.yview_scroll(delta, "units")
        self.texto_executado.yview_scroll(delta, "units")
        self.texto_do_programa.yview_scroll(delta, "units")
        return "break"

    def carregar_programa(self):
        caminho_arquivo= filedialog.askopenfilename(title="Selecione o arquivo de programa",
                                               filetypes=(("Todos os arquivos", "*.*"), ("Arquivos ASM", "*.asm"), ("Arquivos S", "*.s")))
        if caminho_arquivo:
            self.caminho_programa = caminho_arquivo
            self._carregar_arquivo(caminho_arquivo)
 
    def show_datapath_window(self):
        datapath_window = tk.Toplevel(self.root)
        datapath_window.title("Datapath")

        datapath_label = tk.Label(datapath_window, text="Parte do Datapath usada:")
        datapath_label.pack()

    def recarregar_programa(self):
        if self.caminho_programa:
            self.simulator = Simulator()  # Resetar o simulador
            self._carregar_arquivo(self.caminho_programa)
            self.texto_output.delete(1.0, tk.END)  # Limpar o console
            self.texto_binario.delete(1.0, tk.END)  # Limpar o console de código binário
            self.texto_executado.delete(1.0, tk.END)  # Limpar o console de código executado
            self.texto_do_programa.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.texto_output.insert(tk.END, self.formatar_mensagens("Programa recarregado."))
            self.atualizar_registradores()  # Atualizar a exibição dos registradores
            self.limpar_tabela_registradores()  # Limpar a exibição dos registradores
            self.atualizar_codigos_arrays()  # Atualizar os arrays de códigos
            self.atualizar_codigos_display()  # Atualizar a exibição do código
        elif self.simulator.ultimo_programa:
            self.texto_output.delete(1.0, tk.END)  # Limpar o console
            self.texto_binario.delete(1.0, tk.END)  # Limpar o console de código binário
            self.texto_executado.delete(1.0, tk.END)  # Limpar o console de código executado
            self.texto_do_programa.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.texto_output.insert(tk.END, self.formatar_mensagens("Último programa recarregado."))
            self.atualizar_registradores()  # Atualizar a exibição dos registradores
            self.limpar_tabela_registradores()  # Limpar a exibição dos registradores
            self.atualizar_codigos_arrays()  # Atualizar os arrays de códigos
            self.atualizar_codigos_display()  # Atualizar a exibição do código
            self.simulator.carregar_programa(self.simulator.ultimo_programa)
        else:
            self.texto_output.delete(1.0, tk.END)  # Limpar o console
            self.texto_binario.delete(1.0, tk.END)  # Limpar o console de código binário
            self.texto_executado.delete(1.0, tk.END)  # Limpar o console de código executado
            self.texto_do_programa.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.texto_output.insert(tk.END, self.formatar_mensagens("Nenhum programa carregado para recarregar."))

    def _carregar_arquivo(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            programa = file.readlines()
        # Replace call to carregar_programa with carregar_programa
        self.simulator.carregar_programa(programa)
        self.texto_output.delete(1.0, tk.END)  # Limpar o console
        self.texto_binario.delete(1.0, tk.END)  # Limpar o console de código binário
        self.texto_executado.delete(1.0, tk.END)  # Limpar o console de código executado
        self.texto_do_programa.delete(1.0, tk.END)  # Limpar o console de código do programa
        self.texto_output.insert(tk.END, self.formatar_mensagens(f"Programa {file_path} carregado."))
        self.atualizar_registradores()  # Atualizar a exibição dos registradores
        self.limpar_tabela_registradores()  # Limpar a exibição dos registradores
        self.atualizar_codigos_arrays()  # Atualizar os arrays de códigos
        self.atualizar_codigos_display()  # Atualizar a exibição do código

    def carregar_ultimo_programa(self):
        if self.simulator.ultimo_programa:
            self.simulator.carregar_programa(self.simulator.ultimo_programa)
            self.texto_output.delete(1.0, tk.END)  # Limpar o console
            self.texto_binario.delete(1.0, tk.END)  # Limpar o console de código binário
            self.texto_executado.delete(1.0, tk.END)  # Limpar o console de código executado
            self.texto_do_programa.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.texto_output.insert(tk.END, self.formatar_mensagens("Último programa carregado."))
            self.atualizar_registradores()  # Atualizar a exibição dos registradore
            self.limpar_tabela_registradores()  # Limpar a exibição dos registradores
            self.atualizar_codigos_arrays()  # Atualizar os arrays de códigos
            self.atualizar_codigos_display()  # Atualizar a exibição do código
        else:
            self.texto_output.delete(1.0, tk.END)  # Limpar o console
            self.texto_binario.delete(1.0, tk.END)  # Limpar o console de código binário
            self.texto_executado.delete(1.0, tk.END)  # Limpar o console de código executado
            self.texto_do_programa.delete(1.0, tk.END)  # Limpar o console de código do programa
            self.texto_output.insert(tk.END, self.formatar_mensagens("Nenhum programa salvo encontrado."))

    def step(self):
        if self.simulator.program_counter.get() >= len(self.simulator.programa):
            return
        try:
            self.simulator.passo(self.atualizar_registradores)  # Passar a função de atualização dos registradores
            # self.atualizar_registradores()  # Atualizar a exibição dos registradores
            self.atualizar_codigos_display()  # Atualizar a exibição da linha de código sendo executada
            self.root.update_idletasks()  # Forçar a atualização da interface gráfica
            
        except RuntimeError as e:
            self.texto_output.insert(tk.END, self.formatar_mensagens(f"Erro: {e}"))

    def run(self):
        if self.simulator.program_counter.get() >= len(self.simulator.programa):
            return
        try:
            while self.simulator.program_counter.get() < len(self.simulator.programa):
                self.simulator.passo(self.atualizar_registradores)  # Passar a função de atualização dos registradores
                # self.atualizar_registradores()  # Atualizar a exibição dos registradores
                self.atualizar_codigos_display()  # Atualizar a exibição da linha de código sendo executada
                self.root.update_idletasks()  # Forçar a atualização da interface gráfica
            self.texto_output.insert(tk.END, self.formatar_mensagens("Programa executado."))
        except RuntimeError as e:
            self.texto_output.insert(tk.END, self.formatar_mensagens(f"Erro: {e}"))

    def limpar_tabela_registradores(self):
        self.registers_text_col1.delete(1.0, tk.END)
        self.registers_text_col2.delete(1.0, tk.END)
        self.simulator.instructions.registers.registers = registers = [0] * 32
        registers = self.simulator.instructions.registers.registers
        register_names = self.simulator.instructions.registers.register_names
        for i in range(16):
            if self.modo_registradores.get() == "name":
                text = f"{register_names[i]}: {registers[i]}\n"
            else:
                text = f"${i}: {registers[i]}\n"
            
            self.registers_text_col1.insert(tk.END, text)
        for i in range(16, 32):
            if self.modo_registradores.get() == "name":
                text = f"{register_names[i]}: {registers[i]}\n"
            else:
                text = f"${i}: {registers[i]}\n"
            
            self.registers_text_col2.insert(tk.END, text)
        
    def atualizar_registradores(self):
        self.registers_text_col1.delete(1.0, tk.END)
        self.registers_text_col2.delete(1.0, tk.END)
        registers = self.simulator.instructions.registers.registers
        register_names = self.simulator.instructions.registers.register_names

        for i in range(16):
            if self.modo_registradores.get() == "name":
                text = f"{register_names[i]}: {registers[i]}\n"
            else:
                text = f"${i}: {registers[i]}\n"
            
            self.registers_text_col1.insert(tk.END, text)
            
            # Verificar se o registrador foi modificado e aplicar a tag
            if registers[i] != self.registradores_antigos[i]:
                line_start = f"{i + 1}.0"
                line_end = f"{i + 1}.end"
                self.registers_text_col1.tag_add("modified", line_start, line_end)

        for i in range(16, 32):
            if self.modo_registradores.get() == "name":
                text = f"{register_names[i]}: {registers[i]}\n"
            else:
                text = f"${i}: {registers[i]}\n"
            
            self.registers_text_col2.insert(tk.END, text)
            
            # Verificar se o registrador foi modificado e aplicar a tag
            if registers[i] != self.registradores_antigos[i]:
                line_start = f"{i - 15}.0"
                line_end = f"{i - 15}.end"
                self.registers_text_col2.tag_add("modified", line_start, line_end)

        # Atualizar self.registradores_antigos após todas as comparações
        self.registradores_antigos = registers.copy()
        
        pc = self.program_counter.get() * 4
        self.registers_text_col1.insert(tk.END, f"PC: {pc}\n")
        
    def atualizar_codigos_arrays(self):
        self.codigos_binarios = []
        self.codigos_hexa = []
        for instrucao in self.simulator.programa:
            binary_instruction = self.simulator.instructions.traduzir_para_binario(instrucao)
            hex_instruction = "0x" + hex(int(binary_instruction.replace(" ", ""), 2))[2:].zfill(8).upper()
            self.codigos_binarios.append(binary_instruction)
            self.codigos_hexa.append(hex_instruction)

    def atualizar_codigos_display(self):
        self.texto_binario.delete(1.0, tk.END)
        self.texto_executado.delete(1.0, tk.END)
        self.texto_do_programa.delete(1.0, tk.END)
        
        if self.modo_codigos.get() == "binary":
            self.texto_binario.config(width=45)
        else: 
            self.texto_binario.config(width=20)

        for pc in range(len(self.simulator.programa)):
            instrucao = self.simulator.programa[pc]
            instrucao_com_comentarios = self.simulator.programa_com_comentarios[pc]
            transformed_instruction, instruction_with_comment = self.simulator.instructions.transformar_instrucao(instrucao, instrucao_com_comentarios)
            # Aplicar replace separadamente
            transformed_instruction = transformed_instruction.replace('      ', ' ').replace('    ', ' ')
            
            # Exibir a instrução com comentários, seu código binário e a instrução transformada
            if pc < len(self.codigos_binarios) and pc < len(self.codigos_hexa):
                if self.modo_codigos.get() == "binary":
                    self.texto_binario.insert(tk.END, f"{self.codigos_binarios[pc]}\n")
                else:
                    self.texto_binario.insert(tk.END, f"{self.codigos_hexa[pc]}\n")
                self.texto_executado.insert(tk.END, f"{transformed_instruction}\n")
                self.texto_do_programa.insert(tk.END, f"{instrucao_com_comentarios}\n")
        self.texto_binario.see(tk.END)  # Rolagem automática para a última linha
        self.texto_executado.see(tk.END)  # Rolagem automática para a última linha
        self.texto_do_programa.see(tk.END)  # Rolagem automática para a última linha

        # Destacar a linha de código sendo executada
        pc = self.simulator.program_counter.get() - 1
        if pc >= 0 and pc < len(self.simulator.programa):
            self.texto_do_programa.tag_remove("highlight", "1.0", tk.END)
            self.texto_do_programa.tag_add("highlight", f"{pc + 1}.0", f"{pc + 1}.end+1c")
            self.texto_do_programa.tag_configure("highlight", background="#d3d3d3")
            self.texto_do_programa.see(f"{pc + 1}.0")
            self.texto_binario.tag_remove("highlight", "1.0", tk.END)
            self.texto_binario.tag_add("highlight", f"{pc + 1}.0", f"{pc + 1}.end+1c")
            self.texto_binario.tag_configure("highlight", background="#d3d3d3")
            self.texto_binario.see(f"{pc + 1}.0")
            self.texto_executado.tag_remove("highlight", "1.0", tk.END)
            self.texto_executado.tag_add("highlight", f"{pc + 1}.0", f"{pc + 1}.end+1c")
            self.texto_executado.tag_configure("highlight", background="#d3d3d3")
            self.texto_executado.see(f"{pc + 1}.0")
            

if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaPrincipal(root)
    root.mainloop()