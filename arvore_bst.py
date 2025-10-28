# arvore_bst.py

# Importações limpas
import graphviz
from no import No  # Importa a classe No (apenas uma vez)

class ArvoreBST:
    """
    Esta classe define a estrutura da Árvore Binária de Busca (BST).
    Ela gerencia os 'No's e contém os métodos (ações) de 
    inserir, buscar, remover, listar e visualizar.
    """
    
    def __init__(self): # é o construtor que inicializa a árvore
        """Inicializa a árvore com a raiz vazia."""
        self.raiz = None #a raiz começa com none pq n tem nenhum nó por enquanto 

    # -----------------------------------------------------------------
    # --- MÉTODOS PRINCIPAIS (Inserir, Buscar, Remover) ---
    # -----------------------------------------------------------------

    def inserir(self, objeto_chamado_original):
        """Método público para inserir um novo chamado na árvore."""
        
        # 1. Cria o nó, passando o objeto 'Chamado' original e completo.
        novo_no = No(objeto_chamado_original)

        # 2. Verifica se a árvore está vazia
        if self.raiz is None:
            self.raiz = novo_no
        else:
            # 3. Se não, chama a função auxiliar para encontrar o local certo
            self._inserir_no(novo_no)

    def _inserir_no(self, novo_no): #Função auxiliar para inserir um novo nó na árvore
        """Método privado para encontrar a posição e inserir o nó."""
        
        atual = self.raiz # Começa a busca pela raiz

        while True: # Loop infinito que só para com 'break'
            if novo_no.id < atual.id: # Se o ID do novo nó for menor, vamos para a esquerda
                if atual.esquerda is None:
                    # Se não houver nó à esquerda, insere aqui
                    atual.esquerda = novo_no
                    break # Sai do loop
                else:
                    # Se houver, continua a busca pela sub-árvore esquerda
                    atual = atual.esquerda
            else:
                # Se o ID do novo nó for maior ou igual, vamos para a direita
                if atual.direita is None:
                    # Se não houver nó à direita, insere aqui
                    atual.direita = novo_no
                    break # Sai do loop
                else:
                    # Se houver, continua a busca pela sub-árvore direita
                    atual = atual.direita
                    
    def buscar(self, id_procurado):
        """Busca por um nó especifico na árvore usando o ID."""
        
        atual = self.raiz # Começa a busca sempre pela raiz

        while atual is not None:
            if id_procurado == atual.id:
                # 1. ACHAMOS!
                return atual

            elif id_procurado < atual.id:
                # 2. O ID procurado é MENOR, vai para a esquerda
                atual = atual.esquerda
            
            else:
                # 3. Se não é igual nem menor, só pode ser MAIOR
                atual = atual.direita
        
        # Se o loop 'while' terminar, significa que não encontramos o nó
        return None
    
    def remover(self, id_para_remover):
        """Método público para remover um nó, chama o auxiliar recursivo."""
        self.raiz = self._remover_no(self.raiz, id_para_remover)

    def _remover_no(self, no_atual, id_procurado):
        """Método 'ajudante' privado que procura o nó e o remove."""

        # PARTE 1: Encontrar o nó a ser removido (usando recursão)
        if no_atual is None:
            return no_atual

        if id_procurado < no_atual.id:
            no_atual.esquerda = self._remover_no(no_atual.esquerda, id_procurado)
        
        elif id_procurado > no_atual.id:
            no_atual.direita = self._remover_no(no_atual.direita, id_procurado)
        
        # Se achamos o nó (id_procurado == no_atual.id)
        else:
            # PARTE 2: LÓGICA DE REMOÇÃO 
            
            # Caso 1: Nó é uma folha (sem filhos)
            if no_atual.esquerda is None and no_atual.direita is None:
                return None # Simplesmente remove

            # Caso 2: Nó tem apenas um filho (direito)
            elif no_atual.esquerda is None:
                return no_atual.direita # O filho direito "sobe"

            # Caso 2: Nó tem apenas um filho (esquerdo)
            elif no_atual.direita is None:
                return no_atual.esquerda # O filho esquerdo "sobe"
            
            # Caso 3: Nó tem DOIS filhos
            else:
                # 1. Encontra o "substituto" (o menor nó da subárvore direita)
                substituto = self._encontrar_menor_no(no_atual.direita)

                # 2. Copia os dados do 'substituto' por cima dos dados do nó atual
                no_atual.id = substituto.id
                no_atual.chamado_completo = substituto.chamado_completo
                
                # 3. Remove o nó 'substituto' (que agora é duplicado) da subárvore direita
                no_atual.direita = self._remover_no(no_atual.direita, substituto.id)

        return no_atual

    def _encontrar_menor_no(self, no_atual):
        """Função 'ajudante' para encontrar o nó com o menor ID (sucessor em-ordem)."""
        # O menor nó está sempre o mais à esquerda possível
        while no_atual.esquerda is not None:
            no_atual = no_atual.esquerda
        return no_atual

    # -----------------------------------------------------------------
    # --- MÉTODOS DE LISTAGEM E CONTAGEM ---
    # -----------------------------------------------------------------

    def listar_em_ordem(self):
        """Método público que retorna uma LISTA de nós em ordem crescente de ID."""
        lista_ordenada = []
        self._listar_em_ordem_recursivo(self.raiz, lista_ordenada)
        return lista_ordenada

    def _listar_em_ordem_recursivo(self, no_atual, lista):
        """Método 'ajudante' privado que percorre a árvore (E-V-D)."""
        if no_atual is not None:
            # PASSO 1: VAI PARA A ESQUERDA
            self._listar_em_ordem_recursivo(no_atual.esquerda, lista)

            # PASSO 2: VISITA O NÓ ATUAL (adiciona à lista)
            lista.append(no_atual)

            # PASSO 3: VAI PARA A DIREITA
            self._listar_em_ordem_recursivo(no_atual.direita, lista)
            
    def listar_por_prioridade(self, prioridade_desejada):
        """Retorna uma lista de nós que correspondem a uma prioridade específica."""
        
        todos_os_nos = self.listar_em_ordem()
        lista_filtrada = []

        for no in todos_os_nos:
            # Verifica a prioridade DENTRO do 'chamado_completo'
            if no.chamado_completo.prioridade == prioridade_desejada:
                lista_filtrada.append(no)
        
        return lista_filtrada
    
    def get_node_count(self):
        """Conta o número total de nós na árvore."""
        
        # Função interna recursiva
        def _count_recursive(node):
            # Se o nó é nulo, conta 0
            if node is None:
                return 0
            # Senão, conta 1 (ele mesmo) + o da esquerda + o da direita
            return 1 + _count_recursive(node.esquerda) + _count_recursive(node.direita)
        
        # Inicia a contagem a partir da raiz
        return _count_recursive(self.raiz)

    # -----------------------------------------------------------------
    # --- MÉTODO DE VISUALIZAÇÃO (COM LÓGICA DINÂMICA) ---
    # -----------------------------------------------------------------
    
    def visualizar_arvore(self, appearance_mode='dark'):
        """
        Gera a imagem da árvore BST e a retorna como dados PNG (bytes).
        O tamanho dos nós diminui conforme a árvore cresce.
        """
        if self.raiz is None:
            print("INFO: Árvore está vazia. Nada para visualizar.")
            raise ValueError("A árvore está vazia. Adicione chamados primeiro.")
        
        # --- LÓGICA DE TAMANHO DINÂMICO ---
        total_nodes = self.get_node_count()
        
        # Define os parâmetros de dimensionamento
        base_font_size = 14  # Tamanho máximo da fonte (para < 5 nós)
        min_font_size = 8    # Tamanho mínimo da fonte (para árvores grandes)
        step = 5             # A cada X nós, o tamanho diminui
        reduction = 1        # Diminui Ypt por "step"

        # Calcula a redução. max(0, ...) garante que não seja negativo
        font_reduction = max(0, (total_nodes // step) * reduction)
        
        # Aplica a redução, mas não deixa ser menor que 'min_font_size'
        node_font_size = max(min_font_size, base_font_size - font_reduction)
        # Aresta um pouco menor que o nó, mas também não menor que o mínimo
        edge_font_size = max(min_font_size - 1, node_font_size - 2) 
        
        print(f"INFO: Total de nós: {total_nodes}. Tamanho da fonte calculado: {node_font_size}pt")
        # --- FIM DA LÓGICA DINÂMICA ---

        # --- ESTILIZAÇÃO (baseado no modo) ---
        if appearance_mode == 'dark':
            bg_color = "#2B2B2B"  # Cor de fundo escura do CTk
            node_color = "#343638" # Cor do nó
            text_color = "white"   # Cor do texto
            edge_color = "white"
        else: # modo 'light'
            bg_color = "#EBEBEB"   # Cor de fundo clara
            node_color = "#DDEFFF" # Azul claro para os nós
            text_color = "black"
            edge_color = "black"

        # 1. Cria o objeto Digraph
        dot = graphviz.Digraph(comment='Árvore de Chamados BST')
        dot.attr(dpi='150') # Mantém a alta DPI para qualidade
        dot.attr(bgcolor=bg_color)
        
        # --- MODIFICADO: usa as novas variáveis de tamanho ---
        dot.attr('node', 
                 shape='record', 
                 fontname='Arial', 
                 fontsize=str(node_font_size), # <-- USA A VARIÁVEL
                 style='filled', 
                 fillcolor=node_color,
                 fontcolor=text_color)
        dot.attr('edge', 
                 fontname='Arial', 
                 fontsize=str(edge_font_size), # <-- USA A VARIÁVEL
                 color=edge_color)
        # --- FIM DA MODIFICAÇÃO ---

        dot.attr(rankdir='TB') # Top-to-Bottom

        # 2. Função auxiliar interna para adicionar nós e arestas
        def add_nodes_edges(node):
            if node is None:
                return
            
            # Limpa o título para evitar erros do Graphviz com caracteres especiais
            titulo_limpo = str(node.chamado_completo.titulo[:25]).encode('utf-8', 'ignore').decode('utf-8')
            
            # Formata o label do nó no estilo "record"
            label_str = (f"{{ID: {str(node.id)} | "
                         f"{titulo_limpo}... | "
                         f"Prio: {str(node.chamado_completo.prioridade)}}}")
            
            dot.node(str(node.id), label=label_str)

            # 3. Conecta com os filhos (recursivamente)
            if node.esquerda:
                dot.edge(str(node.id), str(node.esquerda.id), label="< ID")
                add_nodes_edges(node.esquerda)
            
            if node.direita:
                dot.edge(str(node.id), str(node.direita.id), label=">= ID")
                add_nodes_edges(node.direita)

        # 5. Inicia a recursão a partir da raiz
        add_nodes_edges(self.raiz)

        try:
            # 6. GERA OS BYTES DA IMAGEM
            # Renderiza diretamente para a memória no formato PNG
            png_data = dot.pipe(format='png')
            
            # Retorna os dados brutos do PNG
            return png_data
        
        except graphviz.backend.execute.ExecutableNotFound:
            print("ERRO: Executável 'dot' do Graphviz não encontrado.")
            raise Exception("Graphviz (dot) não foi encontrado.\nVerifique a instalação e o PATH do sistema.")
        except Exception as e:
            print(f"ERRO ao renderizar a árvore: {e}")
            raise e # Lança o erro para o main.py pegar