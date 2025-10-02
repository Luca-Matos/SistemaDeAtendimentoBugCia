# modern_main.py (Modificado)
import os
import customtkinter as ctk
from collections import deque
from models import Cliente, Atendente, Chamado # Mantido models2 conforme o arquivo original
import tkinter.filedialog as filedialog

# CONFIGURAÇÕES DE APARÊNCIA
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

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
chamado_urgente = Chamado(cliente_logado, "Servidor de arquivos offline",
                          "Ninguém consegue acessar os arquivos da rede.")
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
        if hasattr(frame, 'on_show'): frame.on_show()


class PopupNovoChamado(ctk.CTkToplevel):
    def __init__(self, master, controller, callback):
        super().__init__(master)
        self.callback = callback
        self.title("Registrar Novo Chamado");
        self.geometry("500x400");
        self.transient(master)
        ctk.CTkLabel(self, text="Título do Chamado:", font=controller.fonte_corpo).pack(pady=(20, 5), padx=20,
                                                                                        anchor="w")
        self.titulo_entry = ctk.CTkEntry(self, width=460, font=controller.fonte_corpo);
        self.titulo_entry.pack(padx=20, fill='x')
        ctk.CTkLabel(self, text="Descrição Detalhada:", font=controller.fonte_corpo).pack(pady=(15, 5), padx=20,
                                                                                          anchor="w")
        self.desc_textbox = ctk.CTkTextbox(self, font=controller.fonte_pequena);
        self.desc_textbox.pack(padx=20, fill='both', expand=True)
        ctk.CTkButton(self, text="Salvar Chamado", font=controller.fonte_corpo, command=self.salvar).pack(pady=20)

    def salvar(self):
        titulo = self.titulo_entry.get();
        descricao = self.desc_textbox.get("1.0", "end-1c")
        if titulo and descricao:
            self.callback(titulo, descricao);
            self.destroy()
        else:
            print("Erro: campos vazios")


class TelaLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        login_frame = ctk.CTkFrame(self, width=300, corner_radius=10);
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(login_frame, text="Bem-Vindo", font=controller.fonte_titulo).pack(pady=(20, 10))
        # Mantendo os valores de login originais
        self.user_entry = ctk.CTkEntry(login_frame, placeholder_text="Usuário", width=200, font=controller.fonte_corpo);
        self.user_entry.pack(pady=10, padx=20);
        self.user_entry.insert(0, "cliente")
        self.pass_entry = ctk.CTkEntry(login_frame, placeholder_text="Senha", show="*", width=200,
                                       font=controller.fonte_corpo);
        self.pass_entry.pack(pady=10, padx=20);
        self.pass_entry.insert(0, "cliente")
        ctk.CTkButton(login_frame, text="Login", font=controller.fonte_corpo, command=self.fazer_login).pack(pady=20,
                                                                                                             padx=20)

    def fazer_login(self):
        user = self.user_entry.get();
        pwd = self.pass_entry.get()
        if user == "cliente" and pwd == "cliente":
            self.controller.show_frame("TelaCliente")
        elif user == "atendente" and pwd == "atendente":
            self.controller.show_frame("TelaAtendente")
        else:
            print("Erro de login")


class TelaCliente(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller;
        self.grid_columnconfigure(0, weight=1);
        self.grid_rowconfigure(1, weight=1)
        top_frame = ctk.CTkFrame(self, fg_color="transparent");
        top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkLabel(top_frame, text=f"Painel do Cliente", font=controller.fonte_titulo).pack(side="left")
        ctk.CTkButton(top_frame, text="Voltar (Logout)", font=controller.fonte_corpo,
                      command=lambda: controller.show_frame("TelaLogin")).pack(side="right")
        ctk.CTkButton(top_frame, text="Novo Chamado", font=controller.fonte_corpo, command=self.registrar_chamado).pack(
            side="right", padx=10)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Meus Chamados");
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def on_show(self):
        self.atualizar_lista_chamados()

    def registrar_chamado(self):
        PopupNovoChamado(self, self.controller, self.salvar_novo_chamado)

    def salvar_novo_chamado(self, titulo, descricao):
        novo_chamado = Chamado(cliente_logado, titulo, descricao);
        sistema_chamados.append(novo_chamado);
        self.atualizar_lista_chamados()

    def abrir_popup_detalhes(self, chamado):
        PopupDetalhes(self, self.controller, chamado, cliente_logado)

    # --- INÍCIO DA MUDANÇA DE INTERFACE NA LISTA DE CHAMADOS ---
    def atualizar_lista_chamados(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        lista_chamados_cliente = [c for c in sistema_chamados if c.requisitante == cliente_logado]

        for chamado in lista_chamados_cliente:
            # Novo estilo do main.py: Um único botão para toda a linha.
            label_text = (f"ID: {chamado.idChamado} | Título: {chamado.titulo} | "
                          f"Data: {chamado.dataAbertura.strftime('%d/%m/%Y')} | Status: {chamado.status}")

            item_button = ctk.CTkButton(
                self.scrollable_frame,
                text=label_text,
                font=self.controller.fonte_corpo,
                anchor="w",
                # Mantido o comando original que chama o PopupDetalhes avançado
                command=lambda c=chamado: self.abrir_popup_detalhes(c)
            )
            item_button.pack(fill="x", padx=10, pady=5)
    # --- FIM DA MUDANÇA DE INTERFACE ---


class TelaAtendente(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1);
        self.grid_rowconfigure(3, weight=1)
        self.lista_atual = [];
        self.indice_atual = 0;
        self.chamado_para_mover = None
        top_frame = ctk.CTkFrame(self, fg_color="transparent");
        top_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        ctk.CTkLabel(top_frame, text="Painel do Atendente", font=controller.fonte_titulo).pack(side="left")
        ctk.CTkButton(top_frame, text="Voltar (Logout)", font=controller.fonte_corpo,
                      command=lambda: controller.show_frame("TelaLogin")).pack(side="right")
        carrossel_frame = ctk.CTkFrame(self);
        carrossel_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.chamado_label = ctk.CTkLabel(carrossel_frame, text="Nenhum chamado.", font=controller.fonte_corpo,
                                          height=60, wraplength=700)
        self.chamado_label.pack(pady=10, padx=10, fill="x")
        botoes_carrossel = ctk.CTkFrame(carrossel_frame, fg_color="transparent");
        botoes_carrossel.pack(pady=10)
        ctk.CTkButton(botoes_carrossel, text="< Anterior", command=self.anterior_chamado).pack(side="left", padx=5)
        ctk.CTkButton(botoes_carrossel, text="Detalhes/Editar", command=self.abrir_popup_detalhes).pack(side="left",
                                                                                                        padx=5)
        ctk.CTkButton(botoes_carrossel, text="Próximo >", command=self.proximo_chamado).pack(side="left", padx=5)
        controles_frame = ctk.CTkFrame(self, fg_color="transparent");
        controles_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        controles_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(controles_frame, text="Ordenar por:", font=self.controller.fonte_corpo).pack(side="left")
        self.ordem_var = ctk.StringVar(value="Padrão")
        self.segmented_button = ctk.CTkSegmentedButton(controles_frame, values=["Padrão", "Prioridade"],
                                                       variable=self.ordem_var, command=self.ordenar_e_atualizar)
        self.segmented_button.pack(side="left", padx=10)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Fila de Chamados");
        self.scrollable_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def manipular_clique_lista(self, chamado_clicado):
        if self.ordem_var.get() != "Padrão": return
        global sistema_chamados
        if self.chamado_para_mover is None:
            self.chamado_para_mover = chamado_clicado;
            self.scrollable_frame.configure(
                label_text="Clique na nova posição para o chamado (ou clique novamente para cancelar)")
        elif self.chamado_para_mover == chamado_clicado:
            self.resetar_modo_mover()
        else:
            try:
                index_destino = list(sistema_chamados).index(chamado_clicado)
                sistema_chamados.remove(self.chamado_para_mover);
                sistema_chamados.insert(index_destino, self.chamado_para_mover)
            except ValueError:
                print("Erro: Chamado não encontrado na fila principal.")
            finally:
                self.resetar_modo_mover();
                self.on_show();
                return
        self.atualizar_lista_ordenada()

    def resetar_modo_mover(self):
        self.chamado_para_mover = None;
        self.scrollable_frame.configure(label_text="Fila de Chamados")

    def on_show(self):
        self.resetar_modo_mover();
        self.ordenar_e_atualizar(self.ordem_var.get())

    def ordenar_e_atualizar(self, ordem_selecionada):
        self.resetar_modo_mover()
        if ordem_selecionada == "Prioridade":
            self.lista_atual = sorted(list(sistema_chamados), key=lambda c: (-c.prioridade, c.dataAbertura))
        else:
            self.lista_atual = list(sistema_chamados)
        self.atualizar_carrossel(list(sistema_chamados));
        self.atualizar_lista_ordenada()

    def atualizar_lista_ordenada(self):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        for chamado in self.lista_atual:
            label_text = f"ID: {chamado.idChamado} | Prio: {chamado.prioridade} | Título: {chamado.titulo} ({chamado.status})"
            item_button = ctk.CTkButton(self.scrollable_frame, text=label_text, font=self.controller.fonte_pequena,
                                        anchor="w")
            item_button.configure(command=lambda c=chamado: self.manipular_clique_lista(c))
            if self.chamado_para_mover == chamado: item_button.configure(fg_color="#1F6AA5")
            item_button.pack(fill="x", padx=10, pady=5)

    def atualizar_carrossel(self, lista_base):
        if not lista_base: self.chamado_label.configure(text="Nenhum chamado para exibir."); return
        if self.indice_atual >= len(lista_base): self.indice_atual = 0
        chamado_atual = lista_base[self.indice_atual]
        texto = f"ID: {chamado_atual.idChamado} | Título: {chamado_atual.titulo}\n\nDescrição: {chamado_atual.descricao}\n\nData: {chamado_atual.dataAbertura.strftime('%d/%m/%Y')} | Prioridade: {chamado_atual.prioridade}"
        self.chamado_label.configure(text=texto)

    def proximo_chamado(self):
        lista_base = list(sistema_chamados)
        if not lista_base: return
        self.indice_atual = (self.indice_atual + 1) % len(lista_base);
        self.atualizar_carrossel(lista_base)

    def anterior_chamado(self):
        lista_base = list(sistema_chamados)
        if not lista_base: return
        self.indice_atual = (self.indice_atual - 1 + len(lista_base)) % len(lista_base);
        self.atualizar_carrossel(lista_base)

    # CORREÇÃO AQUI: Adicionar argumento opcional para compatibilidade com PopupDetalhes
    def abrir_popup_detalhes(self, chamado_opcional=None):
        if chamado_opcional:
            chamado_para_editar = chamado_opcional
        else:
            lista_base = list(sistema_chamados)
            if not lista_base: return
            chamado_para_editar = lista_base[self.indice_atual]

        # Chamada original
        PopupDetalhes(self, self.controller, chamado_para_editar, atendente_logado)


class PopupDetalhes(ctk.CTkToplevel):
    def __init__(self, master, controller, chamado, ator):
        super().__init__(master)
        self.master_frame = master
        self.chamado = chamado
        self.ator = ator

        self.title(f"Detalhes do Chamado ID: {chamado.idChamado}")
        self.geometry("700x600")
        self.transient(master)

        # --- Frame para Título e Versão (Versão preservada) ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 5))

        ctk.CTkLabel(header_frame, text="Título:", font=controller.fonte_corpo).pack(anchor="w")

        # NOVO: Exibe a versão atual do chamado. A versão anterior é implicitamente a (versão atual - 1).
        ctk.CTkLabel(header_frame, text=f"Versão Atual: {chamado.versao}", font=controller.fonte_pequena).pack(
            anchor="e")

        self.titulo_entry = ctk.CTkEntry(self, font=controller.fonte_corpo)
        self.titulo_entry.insert(0, chamado.titulo)
        self.titulo_entry.pack(padx=20, fill='x', pady=(0, 10))

        ctk.CTkLabel(self, text="Descrição:", font=controller.fonte_corpo).pack(padx=20, anchor="w")
        self.desc_textbox = ctk.CTkTextbox(self, font=controller.fonte_pequena);
        self.desc_textbox.insert("1.0", chamado.descricao);
        self.desc_textbox.pack(padx=20, fill='both', expand=True)
        ctk.CTkLabel(self, text=f"Status: {self.chamado.status}", font=controller.fonte_corpo).pack(padx=20, anchor="w")

        if isinstance(self.ator, Atendente):
            # NOVO: Registra que o atendente abriu/visualizou o chamado.
            self.chamado.registrar_visualizacao(self.ator)

            self.titulo_entry.configure(state="disabled")
            self.desc_textbox.configure(state="disabled")
            ctk.CTkLabel(self, text="Prioridade (1-5):", font=controller.fonte_corpo).pack(pady=(15, 5))
            self.prioridade_var = ctk.StringVar(self, value=str(chamado.prioridade))
            ctk.CTkOptionMenu(self, variable=self.prioridade_var, values=["1", "2", "3", "4", "5"]).pack()

        # --- Frame de Botões ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        # Botão Desfazer (função preservada)
        self.btn_desfazer = ctk.CTkButton(btn_frame, text="Desfazer", command=self.desfazer_e_atualizar_ui)
        self.btn_desfazer.pack(side="left", padx=5)
        self.atualizar_estado_botoes_desfazer()
        ctk.CTkButton(btn_frame, text="Salvar Alterações", command=self.salvar).pack(side="left", padx=5)
        if isinstance(self.ator, Atendente):
            ctk.CTkButton(btn_frame, text="Gerar Relatório PDF", command=self.gerar_pdf).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="Resolver", command=self.resolver).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="Remover", command=self.remover, fg_color="#D32F2F",
                          hover_color="#B71C1C").pack(side="left", padx=5)

    def atualizar_estado_botoes_desfazer(self):
        if len(self.chamado._historico_rascunhos) > 1:
            self.btn_desfazer.configure(state="normal")
        else:
            self.btn_desfazer.configure(state="disabled")

    def salvar(self):
        if isinstance(self.ator, Cliente):
            novo_titulo = self.titulo_entry.get()
            nova_descricao = self.desc_textbox.get("1.0", "end-1c")
            nova_prioridade = self.chamado.prioridade # Preserva a prioridade
        elif isinstance(self.ator, Atendente):
            novo_titulo = self.chamado.titulo # Preserva o título
            nova_descricao = self.chamado.descricao # Preserva a descrição
            nova_prioridade = self.prioridade_var.get()
        else:
            self.destroy();
            return
        self.chamado.atualizar(novo_titulo, nova_descricao, nova_prioridade, self.ator)
        self.master_frame.on_show()
        self.destroy()

    def gerar_pdf(self):
        nome_sugerido = f"relatorio_chamado_{self.chamado.idChamado}.pdf"
        caminho_arquivo = filedialog.asksaveasfilename(initialfile=nome_sugerido, defaultextension=".pdf",
                                                       filetypes=[("arquivos PDF", ".pdf"),
                                                                  ("Todos os arquivos", ",*")], title="Salvar PDF como")
        if caminho_arquivo:
            try:
                self.chamado.gerar_relatorio_pdf(caminho_arquivo);
                print(f"PDF gerado: {caminho_arquivo}")
            except Exception as e:
                print(f"ERRO ao gerar o PDF: {e}")
        else:
            print("Geração de PDF cancelada.")

    # Função de Desfazer (função e sistema de versão preservados)
    def desfazer_e_atualizar_ui(self):
        if self.chamado.desfazer_alteracao(self.ator):
            if isinstance(self.ator, Cliente):
                self.titulo_entry.delete(0, "end");
                self.titulo_entry.insert(0, self.chamado.titulo)
                self.desc_textbox.delete("1.0", "end");
                self.desc_textbox.insert("1.0", self.chamado.descricao)
            if isinstance(self.ator, Atendente):
                self.prioridade_var.set(str(self.chamado.prioridade))
            print("Alteração desfeita. Estado anterior restaurado.")
            self.atualizar_estado_botoes_desfazer()
            # Recarregar a janela para mostrar a nova versão
            self.destroy()
            # CORREÇÃO AQUI: Passar o objeto chamado
            self.master_frame.abrir_popup_detalhes(self.chamado)
        else:
            print("Não foi possível desfazer a alteração (verifique as permissões).")

    def resolver(self):
        self.chamado.resolver(self.ator)
        self.master_frame.on_show()
        self.destroy()

    def remover(self):
        global sistema_chamados
        sistema_chamados.remove(self.chamado)
        self.master_frame.on_show()
        self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()