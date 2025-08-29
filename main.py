# modern_main.py
import customtkinter as ctk
from collections import deque
from models import Cliente, Atendente, Chamado

# CONFIGURAÇÕES DE APARÊNCIA
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# DADOS GLOBAIS 
sistema_chamados = deque()
cliente_logado = Cliente(1, "Cliente Padrão", "cliente@email.com")
atendente_logado = Atendente(101, "Atendente Padrão")

# Adicionando dados de exemplo
sistema_chamados.append(Chamado(cliente_logado, "Computador não liga", "Aperto o botão e nada acontece."))
chamado_impressora = Chamado(cliente_logado, "Impressora com problema", "A luz do toner está piscando.")
chamado_impressora.prioridade = 3
sistema_chamados.append(chamado_impressora)
sistema_chamados.append(Chamado(cliente_logado, "Internet lenta", "Sites demoram para carregar."))
chamado_urgente = Chamado(cliente_logado, "Servidor de arquivos offline", "Ninguém consegue acessar os arquivos da rede.")
chamado_urgente.prioridade = 5
sistema_chamados.append(chamado_urgente)


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HelpDesk Moderno v2.0")
        self.geometry("800x650") 

        self.fonte_titulo = ctk.CTkFont(family="Roboto", size=24, weight="bold")
        self.fonte_corpo = ctk.CTkFont(family="Roboto", size=14)
        self.fonte_pequena = ctk.CTkFont(family="Roboto", size=12)

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (TelaLogin, TelaCliente, TelaAtendente):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TelaLogin")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

# Criar Chamado Cliente
class PopupNovoChamado(ctk.CTkToplevel):
    
    def __init__(self, master, controller, callback):
        super().__init__(master)
        self.callback = callback
        self.title("Registrar Novo Chamado"); self.geometry("500x400"); self.transient(master)
        ctk.CTkLabel(self, text="Título do Chamado:", font=controller.fonte_corpo).pack(pady=(20, 5), padx=20, anchor="w")
        self.titulo_entry = ctk.CTkEntry(self, width=460, font=controller.fonte_corpo); self.titulo_entry.pack(padx=20, fill='x')
        ctk.CTkLabel(self, text="Descrição Detalhada:", font=controller.fonte_corpo).pack(pady=(15, 5), padx=20, anchor="w")
        self.desc_textbox = ctk.CTkTextbox(self, font=controller.fonte_pequena); self.desc_textbox.pack(padx=20, fill='both', expand=True)
        ctk.CTkButton(self, text="Salvar Chamado", font=controller.fonte_corpo, command=self.salvar).pack(pady=20)
    def salvar(self):
        titulo = self.titulo_entry.get(); descricao = self.desc_textbox.get("1.0", "end-1c")
        if titulo and descricao: self.callback(titulo, descricao); self.destroy()
        else: print("Erro: campos vazios")

# --- TELA DE LOGIN
class TelaLogin(ctk.CTkFrame):
   
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        login_frame = ctk.CTkFrame(self, width=300, corner_radius=10); login_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(login_frame, text="Bem-Vindo", font=controller.fonte_titulo).pack(pady=(20, 10))
        self.user_entry = ctk.CTkEntry(login_frame, placeholder_text="Usuário", width=200, font=controller.fonte_corpo); self.user_entry.pack(pady=10, padx=20); self.user_entry.insert(0, "atendente")
        self.pass_entry = ctk.CTkEntry(login_frame, placeholder_text="Senha", show="*", width=200, font=controller.fonte_corpo); self.pass_entry.pack(pady=10, padx=20); self.pass_entry.insert(0, "atendente")
        ctk.CTkButton(login_frame, text="Login", font=controller.fonte_corpo, command=self.fazer_login).pack(pady=20, padx=20)
    def fazer_login(self):
        user = self.user_entry.get(); pwd = self.pass_entry.get()
        if user == "cliente" and pwd == "cliente": self.controller.show_frame("TelaCliente")
        elif user == "atendente" and pwd == "atendente": self.controller.show_frame("TelaAtendente")
        else: print("Erro de login")

# TELA DO CLIENTE
class TelaCliente(ctk.CTkFrame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller; self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        top_frame = ctk.CTkFrame(self, fg_color="transparent"); top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkLabel(top_frame, text=f"Painel do Cliente", font=controller.fonte_titulo).pack(side="left")
        ctk.CTkButton(top_frame, text="Voltar (Logout)", font=controller.fonte_corpo, command=lambda: controller.show_frame("TelaLogin")).pack(side="right")
        ctk.CTkButton(top_frame, text="Novo Chamado", font=controller.fonte_corpo, command=self.registrar_chamado).pack(side="right", padx=10)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Meus Chamados"); self.scrollable_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
    def on_show(self): self.atualizar_lista_chamados()
    def registrar_chamado(self): PopupNovoChamado(self, self.controller, self.salvar_novo_chamado)
    def salvar_novo_chamado(self, titulo, descricao):
        novo_chamado = Chamado(cliente_logado, titulo, descricao); sistema_chamados.append(novo_chamado); self.atualizar_lista_chamados()
    def atualizar_lista_chamados(self):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        lista_chamados_cliente = [c for c in sistema_chamados if c.requisitante == cliente_logado]
        for chamado in lista_chamados_cliente:
            item_frame = ctk.CTkFrame(self.scrollable_frame); item_frame.pack(fill="x", padx=10, pady=5)
            label_text = f"ID: {chamado.idChamado} | Título: {chamado.titulo} | Status: {chamado.status}"
            ctk.CTkLabel(item_frame, text=label_text, font=self.controller.fonte_corpo).pack(anchor="w", padx=10, pady=10)

#TELA DO ATENDENTE
class TelaAtendente(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) 
        
        self.lista_atual = [] # visualização ordenada
        self.indice_atual = 0
        
       
        self.chamado_selecionado = None
        self.botoes_chamado = {} # Dicionário para guardar os botões da lista

        # Top Frame
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        ctk.CTkLabel(top_frame, text="Painel do Atendente", font=controller.fonte_titulo).pack(side="left")
        ctk.CTkButton(top_frame, text="Voltar (Logout)", font=controller.fonte_corpo, command=lambda: controller.show_frame("TelaLogin")).pack(side="right")

        # Carrossel
        carrossel_frame = ctk.CTkFrame(self)
        carrossel_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.chamado_label = ctk.CTkLabel(carrossel_frame, text="Nenhum chamado.", font=controller.fonte_corpo, height=60, wraplength=700)
        self.chamado_label.pack(pady=10, padx=10, fill="x")
        botoes_carrossel = ctk.CTkFrame(carrossel_frame, fg_color="transparent")
        botoes_carrossel.pack(pady=10)
        ctk.CTkButton(botoes_carrossel, text="< Anterior", command=self.anterior_chamado).pack(side="left", padx=5)
        ctk.CTkButton(botoes_carrossel, text="Detalhes/Editar", command=self.abrir_popup_detalhes).pack(side="left", padx=5)
        ctk.CTkButton(botoes_carrossel, text="Próximo >", command=self.proximo_chamado).pack(side="left", padx=5)

        
        controles_frame = ctk.CTkFrame(self, fg_color="transparent")
        controles_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        controles_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(controles_frame, text="Ordenar por:", font=self.controller.fonte_corpo).pack(side="left")
        self.ordem_var = ctk.StringVar(value="Padrão")
        self.segmented_button = ctk.CTkSegmentedButton(controles_frame, values=["Padrão", "Prioridade"],
                                                       variable=self.ordem_var, command=self.ordenar_e_atualizar)
        self.segmented_button.pack(side="left", padx=10)

        # tem que atualizar
        self.btn_mover_fim = ctk.CTkButton(controles_frame, text="Mover para Fim", state="disabled", command=self.mover_para_fim)
        self.btn_mover_fim.pack(side="right")
        self.btn_mover_inicio = ctk.CTkButton(controles_frame, text="Mover para Início", state="disabled", command=self.mover_para_inicio)
        self.btn_mover_inicio.pack(side="right", padx=10)


        # Lista Ordenada
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Fila de Chamados")
        self.scrollable_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")

    # selecionar um chamado na lista
    def selecionar_chamado(self, chamado, botao_clicado):
        self.chamado_selecionado = chamado
        
        # botões de ação
        self.btn_mover_inicio.configure(state="normal")
        self.btn_mover_fim.configure(state="normal")

        # Feedback visual
        for btn in self.botoes_chamado.values():
            btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        botao_clicado.configure(fg_color="#1F6AA5") 

    
    def mover_para_inicio(self):
        if self.chamado_selecionado:
            global sistema_chamados
            sistema_chamados.remove(self.chamado_selecionado)
            sistema_chamados.appendleft(self.chamado_selecionado)
            self.on_show() # Atualiza toda a tela

    def mover_para_fim(self):
        if self.chamado_selecionado:
            global sistema_chamados
            sistema_chamados.remove(self.chamado_selecionado)
            sistema_chamados.append(self.chamado_selecionado)
            self.on_show() # Atualiza toda a tela

    def on_show(self):
        # se nao tiver selecionado, desabilita os botoes
        self.chamado_selecionado = None
        self.btn_mover_inicio.configure(state="disabled")
        self.btn_mover_fim.configure(state="disabled")
        self.ordenar_e_atualizar(self.ordem_var.get())

    
    def ordenar_e_atualizar(self, ordem_selecionada):
        if ordem_selecionada == "Prioridade":
            
            self.lista_atual = sorted(list(sistema_chamados), key=lambda c: (-c.prioridade, c.dataAbertura))
        else: 
            self.lista_atual = list(sistema_chamados)
        
        
        self.atualizar_carrossel(list(sistema_chamados))
        self.atualizar_lista_ordenada()

    def atualizar_lista_ordenada(self):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        self.botoes_chamado.clear() # Limpa o dicionário de botões
        
        for chamado in self.lista_atual:
            
            label_text = f"ID: {chamado.idChamado} | Prio: {chamado.prioridade} | Título: {chamado.titulo} ({chamado.status})"
            
            
            item_button = ctk.CTkButton(self.scrollable_frame, text=label_text, font=self.controller.fonte_pequena, anchor="w")
            item_button.configure(command=lambda c=chamado, b=item_button: self.selecionar_chamado(c, b))
            item_button.pack(fill="x", padx=10, pady=5)
            
            self.botoes_chamado[chamado.idChamado] = item_button

    def atualizar_carrossel(self, lista_base):
        if not lista_base: self.chamado_label.configure(text="Nenhum chamado para exibir."); return
        
        # Garante que o índice não estoure se a lista diminuir
        if self.indice_atual >= len(lista_base):
            self.indice_atual = 0

        chamado_atual = lista_base[self.indice_atual]
        texto = f"ID: {chamado_atual.idChamado} | Título: {chamado_atual.titulo}\nData: {chamado_atual.dataAbertura.strftime('%d/%m/%Y')} | Prioridade: {chamado_atual.prioridade}"
        self.chamado_label.configure(text=texto)

    def proximo_chamado(self):
        lista_base = list(sistema_chamados)
        if not lista_base: return
        self.indice_atual = (self.indice_atual + 1) % len(lista_base)
        self.atualizar_carrossel(lista_base)

    def anterior_chamado(self):
        lista_base = list(sistema_chamados)
        if not lista_base: return
        self.indice_atual = (self.indice_atual - 1 + len(lista_base)) % len(lista_base)
        self.atualizar_carrossel(lista_base)

    def abrir_popup_detalhes(self):
        lista_base = list(sistema_chamados)
        if not lista_base: return
        chamado_para_editar = lista_base[self.indice_atual]
        PopupDetalhes(self, self.controller, chamado_para_editar)


class PopupDetalhes(ctk.CTkToplevel):
    def __init__(self, master, controller, chamado):
        super().__init__(master)
        self.master_frame = master
        
        self.chamado = chamado
        self.title(f"Detalhes do Chamado ID: {chamado.idChamado}"); self.geometry("500x550"); self.transient(master)
        ctk.CTkLabel(self, text="Título:", font=controller.fonte_corpo).pack(pady=(20, 5), padx=20, anchor="w")
        self.titulo_entry = ctk.CTkEntry(self, font=controller.fonte_corpo); self.titulo_entry.insert(0, chamado.titulo); self.titulo_entry.pack(padx=20, fill='x')
        ctk.CTkLabel(self, text="Descrição:", font=controller.fonte_corpo).pack(pady=(15, 5), padx=20, anchor="w")
        self.desc_textbox = ctk.CTkTextbox(self, font=controller.fonte_pequena); self.desc_textbox.insert("1.0", chamado.descricao); self.desc_textbox.pack(padx=20, fill='both', expand=True)
        ctk.CTkLabel(self, text="Prioridade (1-5):", font=controller.fonte_corpo).pack(pady=(15, 5))
        self.prioridade_var = ctk.StringVar(self, value=str(chamado.prioridade)); ctk.CTkOptionMenu(self, variable=self.prioridade_var, values=["1", "2", "3", "4", "5"]).pack()
        btn_frame = ctk.CTkFrame(self, fg_color="transparent"); btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="Salvar Alterações", command=self.salvar).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Resolver", command=self.resolver).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Remover", command=self.remover, fg_color="#D32F2F", hover_color="#B71C1C").pack(side="left", padx=5)
    def salvar(self):
        self.chamado.atualizar(self.titulo_entry.get(), self.desc_textbox.get("1.0", "end-1c"), self.prioridade_var.get()); self.master_frame.on_show(); self.destroy()
    def resolver(self):
        self.chamado.resolver(); self.master_frame.on_show(); self.destroy()
    def remover(self):
        global sistema_chamados; id_para_remover = self.chamado.idChamado; sistema_chamados = deque([c for c in sistema_chamados if c.idChamado != id_para_remover]); self.master_frame.on_show(); self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()