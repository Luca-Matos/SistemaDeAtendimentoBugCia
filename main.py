import random #essa serve pra gerar IDS aleatorios
from tkinter import messagebox #biblioteca padrão do python para janelas de mensagem
import customtkinter as ctk #biblioteca customtkinter pra interface gráfica
from arvore_bst import ArvoreBST # importa a classe da árvore de busca binária
from models import Cliente, Atendente, Chamado
import tkinter.filedialog as filedialog

# CONFIGURAÇÕES DE APARÊNCIA
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# DADOS GLOBAIS 
#antes era sistema_chamados = deque() então muda para sistema_chamados arvorebst 
sistema_chamados = ArvoreBST() #essa troca tbm é importante pq antes era sistema_chamados.append mas esse método nao existe em árvore entao agora é inserir 
cliente_logado = Cliente(1, "Cliente Padrão", "cliente@email.com")
atendente_logado = Atendente(101, "Atendente Padrão")

# INTERRUPTOR DE TESTE 
# Mude para 'False' para ver o galho (IDs 1, 2, 3...).
# Mude para 'True' para ver a árvore de demonstração (IDs 100, 50, 150...) isso serve pra dar sequencencia nos IDS randoms tbmm
MODO_DEMONSTRACAO = True
# Dependendo do modo, carregamos dados diferentes na árvore

if MODO_DEMONSTRACAO:
    #  CENÁRIO 1: A árvore completa (Para Testar e Demonstrar) 
    print("INFO: Carregando em MODO DE DEMONSTRAÇÃO (IDs 'bagunçados')...") #os IDS bagunçados são para criar uma árvore com galhos (mais "cheia") de propósito, facilitando a demonstração visual e o teste completo de todas as funções (como a remoção de nós com dois "próximos nós").
    
    # 1. Criamos os objetos Chamados com os dados fixos
    chamado_raiz = Chamado(cliente_logado, "Servidor Offline", "Ninguém consegue acessar os arquivos.")
    chamado_esquerda = Chamado(cliente_logado, "PC não liga", "Aperto o botão e nada acontece.")
    chamado_direita = Chamado(cliente_logado, "Internet lenta", "Sites demoram para carregar.")
    chamado_esquerda_direita = Chamado(cliente_logado, "Impressora com problema", "A luz do toner está piscando.")
    
    # 2. Forçamos os IDs (e ajustamos as prioridades, se quiser)
    chamado_raiz.idChamado = 100
    chamado_raiz.prioridade = 5
    
    chamado_esquerda.idChamado = 50
    chamado_esquerda.prioridade = 2

    chamado_direita.idChamado = 150
    chamado_direita.prioridade = 1
    
    chamado_esquerda_direita.idChamado = 75
    chamado_esquerda_direita.prioridade = 3

    # 3. Inserimos na árvore usando o método inserir
    sistema_chamados.inserir(chamado_raiz)
    sistema_chamados.inserir(chamado_esquerda)
    sistema_chamados.inserir(chamado_direita)
    sistema_chamados.inserir(chamado_esquerda_direita)

else:
    # --- CENÁRIO 2: o galhão gigante
    print("INFO: Carregando em MODO REAL (IDs sequenciais 1, 2, 3...)...")
    
    # 1. definir os dados dos chamados 
    # isso separa os dados da lógica em si, facilitando a adição ou remoção de novos exemplos no futuro, sem precisar alterar o código de inserção (o código de inserção é o que começa com for dados in chamados_iniciais)
    chamados_iniciais = [
    {
            "titulo": "Computador não liga",
            "descricao": "Aperto o botão e nada acontece.",
            "prioridade": 1 
        },
        {
            "titulo": "Impressora com problema",
            "descricao": "A luz do toner está piscando.",
            "prioridade": 2 
        },
        {
            "titulo": "Internet lenta",
            "descricao": "Sites demoram para carregar.",
            "prioridade": 1
        },
        {
            "titulo": "Servidor de arquivos offline",
            "descricao": "Ninguém consegue acessar os arquivos da rede.",
            "prioridade": 5
        }
    ]

    # 2. usamos um laço de repetição (for loop) para processar essa lista 
    #    para cada 'chamados_iniciais', o código abaixo cria o objeto Chamado e o insere na nossa árvore
    print("INFO: Iniciando a inserção de chamados de exemplo na árvore...")
    for dados in chamados_iniciais:
        
        #primeiro, cria o objeto 'Chamado' usando os dados
        # o id único é gerado automaticamente pelo __init__ da classe Chamado
        novo_chamado = Chamado(
            cliente_ou_atendente=cliente_logado,
            titulo=dados["titulo"],
            descricao=dados["descricao"]
        )
        # atribui a prioridade especificada
        novo_chamado.prioridade = dados["prioridade"]

        # insere o novo chamado na árvore binária de busca
    
        sistema_chamados.inserir(novo_chamado)

    print(f"INFO: {len(chamados_iniciais)} chamados de exemplo inseridos com sucesso.")


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HelpDesk Moderno v3.0 - Árvore BST") # Atualizei o título
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

# --- TELA DE LOGIN ---
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

# --- TELA DO CLIENTE ---
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
        
        #inicio da lógica do ID aleatório e único
        
        novo_id_unico = None #prepara uma variável para guardar o ID
        
        # 1. Entra em um loop para procurar um ID único
        while True:
            # 2. gera um número aleatório entre 1 e 200 pra n ficar gigante e sem sentido tipo ID 12 e ID 500
            id_tentativa = random.randint(1, 200) 
            
            # 3.usa a função 'buscar' da nossa árvore para checar se esse ID já existe
            no_existente = sistema_chamados.buscar(id_tentativa)
            
            # 4. se 'buscar' retornou None, significa que o ID NÃO existe (é único ebaaa)
            if no_existente is None:
                novo_id_unico = id_tentativa #vai guarda o ID encontrado
                break #sai do loop 'while'
            # (Se o ID já existia, o loop continua e tenta outro número aleatório pra n ter substituição de chamado)

        # FIM DA NOVA LÓGICA DE ID ALEATÓRIO!!! 

        # 5.agora que TEMOS um ID único, criamos o objeto Chamado
        novo_chamado = Chamado(cliente_logado, titulo, descricao)
        
        # 6. (IMPORTANTE!) Sobrescrevemos o ID sequencial pelo nosso ID aleatório único, porque o objeto Chamado (do models.py) cria automaticamente um ID sequencial (como 5 e ai ID 6 e assim adiante), mas nós queremos que ele use o ID aleatório (como 137) que acabamos de encontrar. Essa linha substitui o ID automático pelo ID aleatório que escolhemos.
        novo_chamado.idChamado = novo_id_unico
        
        # 7.inserimos o objeto Chamado (agora com o ID aleatório) na árvore
        sistema_chamados.inserir(novo_chamado) 
        
        print(f"INFO: Novo chamado criado com ID aleatório: {novo_id_unico}") # Mensagem de teste
        self.atualizar_lista_chamados()
    
    def atualizar_lista_chamados(self):
       
        for widget in self.scrollable_frame.winfo_children(): 
            widget.destroy()
        
        # 2.pede a arvore_bst a lista completa de todos os nós
        #    a função .listar_em_ordem() retorna uma LISTA de objetos 'No'.
        todos_os_nos_ordenados = sistema_chamados.listar_em_ordem()
        
        # 3.filtramos para pegar apenas os nós cujo 'Chamado' interno pertence ao cliente logado,porque essa parte do código está na Tela do Cliente, e o cliente só pode ver a lista dos chamados que ele mesmo abriu. O filtro remove os chamados de outros clientes da lista antes de mostrar na tela
        lista_chamados_cliente = [no for no in todos_os_nos_ordenados if no.chamado_completo.requisitante == cliente_logado]

        # 4. Agora, o 'for' loop vai funcionar sobre essa lista 
        #    ('chamado_no' aqui é um objeto 'No') É uma variável temporária que o for loop usa. A cada "volta" do loop, ela guarda um objeto Nó da lista_chamados_cliente. É através dela que acessamos os dados de cada chamado para mostrar na tela (como chamado_no.id)
        for chamado_no in lista_chamados_cliente:
            
            # 5. Criamos o texto acessando os dados DENTRO do 'chamado_completo'
            label_text = (f"ID: {chamado_no.id} | Título: {chamado_no.chamado_completo.titulo} | "
                          f"Prioridade: {chamado_no.chamado_completo.prioridade} | Status: {chamado_no.chamado_completo.status}")
            
            item_button = ctk.CTkButton(
                self.scrollable_frame, 
                text=label_text, 
                font=self.controller.fonte_corpo, 
                anchor="w",
                # O 'command' agora vai passar o objeto 'No' para a função de detalhes
                command=lambda c=chamado_no: self.abrir_detalhes_cliente(c)
            )
            item_button.pack(fill="x", padx=10, pady=5)
    
    def abrir_detalhes_cliente(self, no_clicado): # Renomeei para 'no_clicado' para clareza
        #Abre o pop-up de detalhes e edição para o cliente, passando o Nó
        PopupDetalhesCliente(self, self.controller, no_clicado) # Passa o objeto Nó

# --- TELA DO ATENDENTE ---
class TelaAtendente(ctk.CTkFrame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(3, weight=1)
        self.lista_atual = []; self.indice_atual = 0; self.chamado_para_mover = None
        top_frame = ctk.CTkFrame(self, fg_color="transparent"); top_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        ctk.CTkLabel(top_frame, text="Painel do Atendente", font=controller.fonte_titulo).pack(side="left")
        ctk.CTkButton(top_frame, text="Voltar (Logout)", font=controller.fonte_corpo, command=lambda: controller.show_frame("TelaLogin")).pack(side="right")
        carrossel_frame = ctk.CTkFrame(self); carrossel_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.chamado_label = ctk.CTkLabel(carrossel_frame, text="Nenhum chamado.", font=controller.fonte_corpo, height=60, wraplength=700); self.chamado_label.pack(pady=10, padx=10, fill="x")
        botoes_carrossel = ctk.CTkFrame(carrossel_frame, fg_color="transparent"); botoes_carrossel.pack(pady=10)
        ctk.CTkButton(botoes_carrossel, text="< Anterior", command=self.anterior_chamado).pack(side="left", padx=5)
        ctk.CTkButton(botoes_carrossel, text="Detalhes/Editar", command=self.abrir_popup_detalhes).pack(side="left", padx=5)
        ctk.CTkButton(botoes_carrossel, text="Próximo >", command=self.proximo_chamado).pack(side="left", padx=5)
        controles_frame = ctk.CTkFrame(self, fg_color="transparent"); controles_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew"); controles_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(controles_frame, text="Ordenar por:", font=self.controller.fonte_corpo).pack(side="left")
        self.ordem_var = ctk.StringVar(value="Padrão"); self.segmented_button = ctk.CTkSegmentedButton(controles_frame, values=["Padrão", "Prioridade"], variable=self.ordem_var, command=self.ordenar_e_atualizar); self.segmented_button.pack(side="left", padx=10)

        #novo bloco a busca por ID
        ctk.CTkLabel(controles_frame, text="Buscar ID:", 
                     font=self.controller.fonte_corpo).pack(side="left", padx=(20, 5)) # Adiciona espaço à esquerda
        
        self.entry_busca_id = ctk.CTkEntry(controles_frame, 
                                           placeholder_text="Digite o ID", 
                                           width=100, # Largura pequena para o ID
                                           font=self.controller.fonte_corpo)
        self.entry_busca_id.pack(side="left", padx=5)
        
        self.btn_buscar = ctk.CTkButton(controles_frame, 
                                        text="Buscar", 
                                        width=70, # Botão menor
                                        font=self.controller.fonte_corpo, 
                                        command=self.buscar_chamado_interface)
        self.btn_buscar.pack(side="left", padx=5)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Fila de Chamados")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Fila de Chamados"); self.scrollable_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")


    def manipular_clique_lista(self, chamado_clicado):
        print(f"Aviso: Reordenação manual desabilitada. Item selecionado: {chamado_clicado.id}")
        self.resetar_modo_mover() 
        self.atualizar_lista_ordenada()


    def resetar_modo_mover(self):
        self.chamado_para_mover = None
        self.scrollable_frame.configure(label_text="Fila de Chamados")

    
    def on_show(self):
        self.resetar_modo_mover()
        self.ordenar_e_atualizar(self.ordem_var.get())

   
    def ordenar_e_atualizar(self, ordem_selecionada):
        self.resetar_modo_mover() 
        
        if ordem_selecionada == "Prioridade":
            todos_os_nos = sistema_chamados.listar_em_ordem()
            # CORREÇÃO: Acessar a prioridade DENTRO do 'chamado_completo'
            self.lista_atual = sorted(todos_os_nos, key=lambda no: no.chamado_completo.prioridade, reverse=True) 
        else: 
            self.lista_atual = sistema_chamados.listar_em_ordem()
        
        lista_para_carrossel = sistema_chamados.listar_em_ordem()
        self.atualizar_carrossel(lista_para_carrossel)
        
        self.atualizar_lista_ordenada()

    
    def atualizar_lista_ordenada(self):
        for widget in self.scrollable_frame.winfo_children(): 
            widget.destroy()

        # ('chamado_no' é um objeto 'No')
        for chamado_no in self.lista_atual: 
            
            # CORREÇÃO: Acessar titulo e prioridade DENTRO do 'chamado_completo'
            label_text = f"ID: {chamado_no.id} | Prio: {chamado_no.chamado_completo.prioridade} | Título: {chamado_no.chamado_completo.titulo}"
            
            item_button = ctk.CTkButton(self.scrollable_frame, text=label_text, font=self.controller.fonte_pequena, anchor="w")
            item_button.configure(command=lambda c=chamado_no: self.manipular_clique_lista(c)) # Passa o Nó
            if self.chamado_para_mover == chamado_no:
                item_button.configure(fg_color="#1F6AA5") 
            item_button.pack(fill="x", padx=10, pady=5)

    
    def atualizar_carrossel(self, lista_base): # 'lista_base' é uma lista de Nós
        if not lista_base: self.chamado_label.configure(text="Nenhum chamado para exibir."); return

        if self.indice_atual >= len(lista_base): self.indice_atual = 0

        # 'no_atual' é um objeto 'No'
        no_atual = lista_base[self.indice_atual] 
        
        # CORREÇÃO: Acessar os dados DENTRO do 'chamado_completo'
        chamado_original = no_atual.chamado_completo
        texto = (f"ID: {no_atual.id} | Título: {chamado_original.titulo}\n\n"
                 f"Descrição: {chamado_original.descricao}\n\n"
                 f"Data: {chamado_original.dataAbertura.strftime('%d/%m/%Y')} | "
                 f"Prioridade: {chamado_original.prioridade} | Status: {chamado_original.status}")
        
        self.chamado_label.configure(text=texto)

    
    def proximo_chamado(self):
       
        lista_base = sistema_chamados.listar_em_ordem() 
        if not lista_base: return
        self.indice_atual = (self.indice_atual + 1) % len(lista_base)
        self.atualizar_carrossel(lista_base)

    def anterior_chamado(self):
       
        lista_base = sistema_chamados.listar_em_ordem()
        if not lista_base: return
        self.indice_atual = (self.indice_atual - 1 + len(lista_base)) % len(lista_base)
        self.atualizar_carrossel(lista_base)

    
    def abrir_popup_detalhes(self):
        
        lista_base = sistema_chamados.listar_em_ordem() 
        if not lista_base: return
        # 'no_para_editar' é um objeto 'No'
        no_para_editar = lista_base[self.indice_atual] 
        # Passamos o Nó para o Popup
        PopupDetalhes(self, self.controller, no_para_editar) 
        

    #NOVA FUNÇÃO: BUSCAR CHAMADO PELA INTERFACE
    def buscar_chamado_interface(self):
        #Pega o ID digitado pelo usuário, busca na árvore e atualiza o carrossel
        
        # 1. Pega o texto digitado no campo de busca
        id_texto = self.entry_busca_id.get()

        # 2. Tenta converter o texto para um número inteiro
        try:
            id_buscado = int(id_texto)
        except ValueError:
            # Se não for um número válido, mostra erro e para
            print(f"ERRO: ID inválido digitado: '{id_texto}'. Por favor, digite apenas números.")
            # (Opcional: Mostrar um pop-up de erro para o usuário)
            # messagebox.showerror("Erro", "ID inválido. Digite apenas números.")
            self.entry_busca_id.delete(0, 'end') # Limpa o campo
            return # Para a execução da função

        # 3. Se a conversão deu certo, chama a função 'buscar' do nosso "cérebro"
        print(f"INFO: Buscando pelo ID: {id_buscado}...")
        no_encontrado = sistema_chamados.buscar(id_buscado)

        # 4. Verifica o resultado da busca
        if no_encontrado is not None:
            # SE ACHOU:
            print(f"INFO: Chamado com ID {id_buscado} encontrado!")
            
            # Precisamos atualizar o 'indice_atual' do carrossel
            # para que ele mostre o nó encontrado.
            try:
                # Pega a lista completa em ordem de ID
                lista_completa = sistema_chamados.listar_em_ordem()
                # Encontra a posição (índice) do nó na lista
                self.indice_atual = lista_completa.index(no_encontrado)
                # Atualiza o carrossel para mostrar esse índice
                self.atualizar_carrossel(lista_completa)
                print(f"INFO: Carrossel atualizado para o índice {self.indice_atual}.")
            except ValueError:
                # Isso não deveria acontecer se o 'buscar' funcionou, mas é bom ter
                print("ERRO: Nó encontrado pela busca, mas não encontrado na lista completa?")

            self.entry_busca_id.delete(0, 'end') # Limpa o campo de busca
        else:
            # SE NÃO ACHOU:
            # Substituímos o print por uma janela pop-up de informação
            messagebox.showinfo("Busca de Chamado", f"Chamado com ID {id_buscado} não encontrado.") 
            self.entry_busca_id.delete(0, 'end') # Limpa o campo de busca  


#POPUP DETALHES CLIENTE 
class PopupDetalhesCliente(ctk.CTkToplevel):
    # O __init__ recebe um Nó
    def __init__(self, master, controller, no_chamado): # Renomeei para 'no_chamado'
        super().__init__(master)
        self.master_frame = master
        self.controller = controller
        # Guardamos o Nó que recebemos
        self.no_chamado_atual = no_chamado 
        # Criamos uma variável fácil para acessar o Chamado original dentro do Nó
        chamado_original = self.no_chamado_atual.chamado_completo

        # CORREÇÃO: Usar dados do Nó e do Chamado interno
        self.title(f"Chamado ID: {self.no_chamado_atual.id} - {chamado_original.status}")
        self.geometry("500x450"); self.transient(master)
        edit_frame = ctk.CTkFrame(self, fg_color="transparent"); edit_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(edit_frame, text="Título do Chamado:", font=controller.fonte_corpo).pack(pady=(10, 5), anchor="w")
        self.titulo_entry = ctk.CTkEntry(edit_frame, font=controller.fonte_corpo)
        self.titulo_entry.insert(0, chamado_original.titulo) # CORREÇÃO
        self.titulo_entry.pack(fill='x')

        ctk.CTkLabel(edit_frame, text="Descrição Detalhada:", font=controller.fonte_corpo).pack(pady=(10, 5), anchor="w")
        self.desc_textbox = ctk.CTkTextbox(edit_frame, font=controller.fonte_pequena)
        self.desc_textbox.insert("1.0", chamado_original.descricao) # CORREÇÃO
        self.desc_textbox.pack(fill='both', expand=True)

        ctk.CTkLabel(edit_frame, text=f"Prioridade: {chamado_original.prioridade} | Status: {chamado_original.status}", font=controller.fonte_pequena).pack(pady=(10, 0), anchor="w") # CORREÇÃO
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent"); btn_frame.pack(pady=10)
        self.btn_desfazer = ctk.CTkButton(btn_frame, text="Desfazer", command=self.desfazer_e_atualizar_ui); self.btn_desfazer.pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Salvar Alterações", command=self.salvar).pack(side="left", padx=10)
        
        self.atualizar_estado_botoes()

    def salvar(self):
        chamado_original = self.no_chamado_atual.chamado_completo
        chamado_original.atualizar(
            self.titulo_entry.get(),
            self.desc_textbox.get("1.0", "end-1c"),
            chamado_original.prioridade # Mantém a prioridade original
        )
        self.master_frame.on_show() 
        self.destroy()

    def desfazer_e_atualizar_ui(self):
        # CORREÇÃO: Chamamos o 'desfazer' do objeto Chamado original
        chamado_original = self.no_chamado_atual.chamado_completo
        if chamado_original.desfazer_alteracao():
            # Atualiza os campos de texto com os dados do Chamado original
            self.titulo_entry.delete(0, ctk.END)
            self.titulo_entry.insert(0, chamado_original.titulo)
            self.desc_textbox.delete("1.0", ctk.END)
            self.desc_textbox.insert("1.0", chamado_original.descricao)
            # Atualiza o label não-editável (se ele for um atributo da classe)
            # Se não for, a atualização na tela principal já resolve
            print("Alteração desfeita. Estado anterior restaurado.")
        
        self.atualizar_estado_botoes()
       
        self.master_frame.on_show() 

    def atualizar_estado_botoes(self):
        # CORREÇÃO: Acessa o histórico DENTRO do Chamado original
        chamado_original = self.no_chamado_atual.chamado_completo
        if len(chamado_original._historico_rascunhos) > 1:
            self.btn_desfazer.configure(state="normal")
        else:
            self.btn_desfazer.configure(state="disabled")

# --- POPUP DETALHES ATENDENTE ---
class PopupDetalhes(ctk.CTkToplevel):
    # O __init__ recebe um Nó
    def __init__(self, master, controller, no_chamado): # Renomeei para 'no_chamado'
        super().__init__(master)
        self.master_frame = master
        self.controller = controller
        # Guardamos o Nó que recebemos
        self.no_chamado_atual = no_chamado 
        # Criamos uma variável fácil para acessar o Chamado original dentro do Nó
        chamado_original = self.no_chamado_atual.chamado_completo

        # CORREÇÃO: Usar dados do Nó e do Chamado interno
        self.title(f"Detalhes do Chamado ID: {self.no_chamado_atual.id}"); self.geometry("700x550"); self.transient(master)
        
        ctk.CTkLabel(self, text="Título:", font=controller.fonte_corpo).pack(pady=(20, 5), padx=20, anchor="w")
        self.titulo_entry = ctk.CTkEntry(self, font=controller.fonte_corpo); self.titulo_entry.insert(0, chamado_original.titulo); self.titulo_entry.pack(padx=20, fill='x') # CORREÇÃO
        
        ctk.CTkLabel(self, text="Descrição:", font=controller.fonte_corpo).pack(pady=(15, 5), padx=20, anchor="w")
        self.desc_textbox = ctk.CTkTextbox(self, font=controller.fonte_pequena); self.desc_textbox.insert("1.0", chamado_original.descricao); self.desc_textbox.pack(padx=20, fill='both', expand=True) # CORREÇÃO
        
        ctk.CTkLabel(self, text="Prioridade (1-5):", font=controller.fonte_corpo).pack(pady=(15, 5))
        self.prioridade_var = ctk.StringVar(self, value=str(chamado_original.prioridade)); ctk.CTkOptionMenu(self, variable=self.prioridade_var, values=["1", "2", "3", "4", "5"]).pack() # CORREÇÃO

        btn_frame = ctk.CTkFrame(self, fg_color="transparent"); btn_frame.pack(pady=20)
        self.btn_desfazer = ctk.CTkButton(btn_frame, text="Desfazer", command=self.desfazer_e_atualizar_ui); self.btn_desfazer.pack(side="left", padx=5)
        self.atualizar_estado_botoes_desfazer()
        self.btn_relatorio_pdf = ctk.CTkButton(btn_frame, text="Gerar Relatório PDF", command=self.gerar_pdf); self.btn_relatorio_pdf.pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Salvar Alterações", command=self.salvar).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Resolver", command=self.resolver).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Remover", command=self.remover, fg_color="#D32F2F", hover_color="#B71C1C").pack(side="left", padx=5)

    def atualizar_estado_botoes_desfazer(self):
        # CORREÇÃO: Acessa o histórico DENTRO do Chamado original
        chamado_original = self.no_chamado_atual.chamado_completo
        if len(chamado_original._historico_rascunhos) > 1:
            self.btn_desfazer.configure(state="normal")
        else:
            self.btn_desfazer.configure(state="disabled")

    def salvar(self):
        # CORREÇÃO: Chamamos o 'atualizar' do objeto Chamado original
        chamado_original = self.no_chamado_atual.chamado_completo
        chamado_original.atualizar(self.titulo_entry.get(), self.desc_textbox.get("1.0", "end-1c"), self.prioridade_var.get())
        self.master_frame.on_show()
        self.destroy()

    def gerar_pdf(self):
        # CORREÇÃO: Usamos o ID do Nó e o método do Chamado original
        chamado_original = self.no_chamado_atual.chamado_completo
        nome_sugerido = f"relatorio_chamado_{self.no_chamado_atual.id}.pdf" # Usa o ID do Nó
        caminho_arquivo = filedialog.asksaveasfilename(initialfile=nome_sugerido, defaultextension=".pdf", filetypes=[("arquivos PDF", ".pdf"), ("Todos os arquivos", ",*")], title="Salvar PDF como")
        if caminho_arquivo:
            try:
                chamado_original.gerar_relatorio_pdf(caminho_arquivo) # Chama o método do Chamado
                print(f"PDF gerado com sucesso: {caminho_arquivo}")
            except Exception as e:
                print(f"ERRO ao gerar o PDF no caminho: {e}")
        else:
            print("geração de PDF cancelada pelo usuario")

    def desfazer_e_atualizar_ui(self):
        # CORREÇÃO: Chamamos o 'desfazer' do objeto Chamado original
        chamado_original = self.no_chamado_atual.chamado_completo
        if chamado_original.desfazer_alteracao():
            # Atualiza a interface com os dados do Chamado original
            self.titulo_entry.delete(0, "end")
            self.titulo_entry.insert(0, chamado_original.titulo)
            self.desc_textbox.delete("1.0", "end")
            self.desc_textbox.insert("1.0", chamado_original.descricao)
            self.prioridade_var.set(str(chamado_original.prioridade))
            print("Alteração desfeita. Estado anterior restaurado.")
        # Atualiza a lista principal também
        self.master_frame.on_show()
        # Atualiza o estado do botão
        self.atualizar_estado_botoes_desfazer() 

    def resolver(self):
        # CORREÇÃO: Chamamos o 'resolver' do objeto Chamado original
        chamado_original = self.no_chamado_atual.chamado_completo
        chamado_original.resolver()
        self.master_frame.on_show()
        self.destroy()

    def remover(self):
        global sistema_chamados
        # CORREÇÃO: Usamos a função 'remover' da árvore, passando o ID do Nó
        sistema_chamados.remover(self.no_chamado_atual.id) 
        self.master_frame.on_show()
        self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()