# main_com_deque.py
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Entry, Button, OptionMenu, StringVar
from collections import deque
from models import Cliente, Atendente, Chamado

# --- DADOS GLOBAIS ---
sistema_chamados = deque()
cliente_logado = Cliente(1, "Cliente Padrão", "cliente@email.com")
atendente_logado = Atendente(101, "Atendente Padrão")

# Adicionando alguns dados de exemplo
sistema_chamados.append(Chamado(cliente_logado, "Meu computador não liga"))
sistema_chamados.append(Chamado(cliente_logado, "Impressora está com problema no toner"))
sistema_chamados.append(Chamado(cliente_logado, "A internet está muito lenta hoje"))


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Atendimento (com Deque)")
        self.geometry("500x400")
        
        container = tk.Frame(self)
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

# --- TELA DE LOGIN ---
class TelaLogin(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Tela de Login", font=("Helvetica", 16))
        label.pack(pady=20)

        tk.Label(self, text="Usuário:").pack()
        self.user_entry = tk.Entry(self)
        self.user_entry.pack(pady=5)
        self.user_entry.insert(0, "cliente")

        tk.Label(self, text="Senha:").pack()
        self.pass_entry = tk.Entry(self, show="*")
        self.pass_entry.pack(pady=5)
        self.pass_entry.insert(0, "cliente")

        login_button = tk.Button(self, text="Login", command=self.fazer_login)
        login_button.pack(pady=20)

    def fazer_login(self):
        user = self.user_entry.get()
        pwd = self.pass_entry.get()
        if user == "cliente" and pwd == "cliente":
            self.controller.show_frame("TelaCliente")
        elif user == "atendente" and pwd == "atendente":
            self.controller.show_frame("TelaAtendente")
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")
        
        # Limpa os campos após a tentativa, caso queira
        # self.user_entry.delete(0, 'end')
        # self.pass_entry.delete(0, 'end')

# --- TELA DO CLIENTE ---
class TelaCliente(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text=f"Bem-vindo, {cliente_logado.nomeCliente}!", font=("Helvetica", 16))
        label.pack(pady=10)
        btn_registrar = tk.Button(self, text="Registrar Novo Chamado", command=self.registrar_chamado)
        btn_registrar.pack(pady=10)
        tk.Label(self, text="Seus Chamados Registrados:").pack(pady=10)
        self.chamados_listbox = tk.Listbox(self, width=80, height=10)
        self.chamados_listbox.pack(pady=5, padx=10)
        
        # VVVVVV BOTÃO DE VOLTAR/LOGOUT ADICIONADO AQUI VVVVVV
        btn_logout = tk.Button(self, text="Voltar (Logout)", command=lambda: controller.show_frame("TelaLogin"))
        btn_logout.pack(pady=15)
        # ^^^^^^ BOTÃO DE VOLTAR/LOGOUT ADICIONADO AQUI ^^^^^^

    def on_show(self):
        self.atualizar_lista_chamados()

    def registrar_chamado(self):
        descricao = simpledialog.askstring("Novo Chamado", "Digite a descrição do seu problema:")
        if descricao:
            novo_chamado = Chamado(cliente_logado, descricao)
            sistema_chamados.append(novo_chamado)
            messagebox.showinfo("Sucesso", f"Chamado ID {novo_chamado.idChamado} registrado!")
            self.atualizar_lista_chamados()

    def atualizar_lista_chamados(self):
        self.chamados_listbox.delete(0, 'end')
        lista_de_chamados = [c for c in list(sistema_chamados) if c.requisitante == cliente_logado]
        if not lista_de_chamados:
            self.chamados_listbox.insert('end', "  Nenhum chamado registrado.")
        else:
            for chamado in lista_de_chamados:
                self.chamados_listbox.insert('end', f"  {chamado}")

# --- TELA DO ATENDENTE ---
class TelaAtendente(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.lista_atual = []
        self.indice_atual = 0

        # ... (código do carrossel e da ordenação) ...
        frame_carrossel = tk.Frame(self, bd=2, relief="groove")
        frame_carrossel.pack(pady=10, padx=10, fill="x")
        tk.Label(frame_carrossel, text="Carrossel de Chamados", font=("Helvetica", 12)).pack()
        self.chamado_label = tk.Label(frame_carrossel, text="Nenhum chamado para exibir.", height=3, wraplength=450)
        self.chamado_label.pack(pady=5)
        botoes_carrossel = tk.Frame(frame_carrossel)
        botoes_carrossel.pack()
        tk.Button(botoes_carrossel, text="< Anterior", command=self.anterior_chamado).pack(side="left", padx=5)
        tk.Button(botoes_carrossel, text="Próximo >", command=self.proximo_chamado).pack(side="left", padx=5)
        tk.Button(botoes_carrossel, text="Detalhes/Editar", command=self.abrir_popup_detalhes).pack(side="left", padx=5)
        frame_ordenacao = tk.Frame(self)
        frame_ordenacao.pack(pady=10, padx=10, fill="x")
        tk.Label(frame_ordenacao, text="Ordenar por:").pack(side="left")
        self.ordem_var = StringVar(self)
        self.ordem_var.set("Ordem de Chegada")
        options = ["Ordem de Chegada", "Prioridade"]
        ordem_menu = OptionMenu(frame_ordenacao, self.ordem_var, *options, command=self.ordenar_e_atualizar)
        ordem_menu.pack(side="left", padx=5)
        self.chamados_ordenados_listbox = tk.Listbox(self, width=80, height=8)
        self.chamados_ordenados_listbox.pack(pady=5, padx=10, fill="x", expand=True)

        # VVVVVV BOTÃO DE VOLTAR/LOGOUT ADICIONADO AQUI VVVVVV
        btn_logout = tk.Button(self, text="Voltar (Logout)", command=lambda: controller.show_frame("TelaLogin"))
        btn_logout.pack(pady=15)
        # ^^^^^^ BOTÃO DE VOLTAR/LOGOUT ADICIONADO AQUI ^^^^^^


    def on_show(self):
        self.ordenar_e_atualizar()

    def ordenar_e_atualizar(self, *args):
        ordem = self.ordem_var.get()
        if ordem == "Prioridade":
            self.lista_atual = sorted(sistema_chamados, key=lambda c: (-c.prioridade, c.dataAbertura))
        else:
            self.lista_atual = list(sistema_chamados)
        self.indice_atual = 0
        self.atualizar_carrossel()
        self.atualizar_lista_ordenada()

    def atualizar_carrossel(self):
        if not self.lista_atual:
            self.chamado_label.config(text="Nenhum chamado para exibir.")
            return
        chamado_atual = self.lista_atual[self.indice_atual]
        texto = f"ID: {chamado_atual.idChamado} | {chamado_atual.descricao[:50]}...\nData: {chamado_atual.dataAbertura.strftime('%d/%m/%Y')} | Prioridade: {chamado_atual.prioridade}"
        self.chamado_label.config(text=texto)

    def atualizar_lista_ordenada(self):
        self.chamados_ordenados_listbox.delete(0, 'end')
        if not self.lista_atual:
            self.chamados_ordenados_listbox.insert('end', "  Nenhum chamado na lista.")
        else:
            for chamado in self.lista_atual:
                self.chamados_ordenados_listbox.insert('end', f"  {chamado}")

    def proximo_chamado(self):
        if not self.lista_atual: return
        self.indice_atual = (self.indice_atual + 1) % len(self.lista_atual)
        self.atualizar_carrossel()

    def anterior_chamado(self):
        if not self.lista_atual: return
        self.indice_atual = (self.indice_atual - 1 + len(self.lista_atual)) % len(self.lista_atual)
        self.atualizar_carrossel()

    def abrir_popup_detalhes(self):
        if not self.lista_atual:
            messagebox.showinfo("Aviso", "Não há chamados para detalhar.")
            return
        chamado_selecionado = self.lista_atual[self.indice_atual]
        PopupDetalhes(self, chamado_selecionado, self.controller)

# O PopupDetalhes não precisa de alteração
class PopupDetalhes(Toplevel):
    def __init__(self, master, chamado, controller):
        super().__init__(master)
        self.chamado = chamado
        self.controller = controller
        
        self.title(f"Detalhes do Chamado ID: {chamado.idChamado}")
        self.geometry("400x350")

        Label(self, text="Descrição:").pack(pady=(10,0))
        self.desc_entry = Entry(self, width=50)
        self.desc_entry.insert(0, chamado.descricao)
        self.desc_entry.pack()
        Label(self, text="Prioridade (1-5):").pack(pady=(10,0))
        self.prioridade_var = StringVar(self)
        self.prioridade_var.set(str(chamado.prioridade))
        OptionMenu(self, self.prioridade_var, *["1", "2", "3", "4", "5"]).pack()
        Label(self, text=f"Status: {chamado.status}").pack(pady=5)
        Label(self, text=f"Aberto em: {chamado.dataAbertura.strftime('%d/%m/%Y %H:%M')}").pack()
        Label(self, text=f"Requisitante: {chamado.requisitante.nomeCliente}").pack()
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        Button(btn_frame, text="Salvar Alterações", command=self.salvar).pack(side="left", padx=5)
        Button(btn_frame, text="Resolver Chamado", command=self.resolver).pack(side="left", padx=5)
        Button(btn_frame, text="Remover Chamado", bg="red", fg="white", command=self.remover).pack(side="left", padx=5)

    def salvar(self):
        self.chamado.atualizar(self.desc_entry.get(), self.prioridade_var.get())
        messagebox.showinfo("Sucesso", "Chamado atualizado.")
        self.master.on_show()
        self.destroy()

    def resolver(self):
        self.chamado.resolver()
        messagebox.showinfo("Sucesso", "Chamado marcado como resolvido.")
        self.master.on_show()
        self.destroy()

    def remover(self):
        global sistema_chamados
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o chamado ID {self.chamado.idChamado}?"):
            id_para_remover = self.chamado.idChamado
            tamanho_antes = len(sistema_chamados)
            sistema_chamados = deque([c for c in sistema_chamados if c.idChamado != id_para_remover])
            if len(sistema_chamados) < tamanho_antes:
                messagebox.showinfo("Sucesso", "Chamado removido.")
            else:
                messagebox.showerror("Erro", "Não foi possível encontrar e remover o chamado.")
            self.master.on_show()
            self.destroy()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()