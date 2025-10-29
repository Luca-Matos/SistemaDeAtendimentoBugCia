# arvore_bst.py

# Importações limpas
import graphviz
from no import No  # Importa a classe No (agora com 'altura')

class ArvoreBST:
    """
    Esta classe define a estrutura da Árvore Binária de Busca (BST)
    AUTO-BALANCEÁVEL (usando a lógica AVL).
    Ela gerencia os 'No's e contém os métodos (ações) de
    inserir, buscar, remover, listar e visualizar.
    """

    def __init__(self): # é o construtor que inicializa a árvore
        """Inicializa a árvore com a raiz vazia."""
        self.raiz = None #a raiz começa com none pq n tem nenhum nó por enquanto

    # -----------------------------------------------------------------
    # --- MÉTODOS AUXILIARES PARA AVL (Altura e Balanceamento) ---
    # -----------------------------------------------------------------

    def _get_altura(self, no):
        """Retorna a altura de um nó (ou 0 se o nó for None)."""
        if no is None:
            return 0 # Um nó inexistente (None) tem altura 0 por definição
        return no.altura # Retorna o valor guardado no atributo 'altura' do Nó

    def _get_fator_balanceamento(self, no):
        """Calcula o fator de balanceamento de um nó."""
        if no is None:
            return 0
        # Fator = Altura da Subárvore Esquerda - Altura da Subárvore Direita
        # Um fator > 1 significa desbalanceado para a esquerda.
        # Um fator < -1 significa desbalanceado para a direita.
        # Um fator 0, 1 ou -1 significa balanceado.
        return self._get_altura(no.esquerda) - self._get_altura(no.direita)

    def _atualizar_altura(self, no):
        """Recalcula e atualiza a altura de um nó baseado na altura MÁXIMA dos seus filhos."""
        if no is not None:
             # A nova altura é 1 (nível do próprio nó) + a maior altura entre os dois filhos
            no.altura = 1 + max(self._get_altura(no.esquerda), self._get_altura(no.direita))

    # -----------------------------------------------------------------
    # --- MÉTODOS DE ROTAÇÃO AVL ---
    # -----------------------------------------------------------------

    def _rotacao_direita(self, z):
        r"""Executa uma rotação simples à direita na subárvore com raiz z.
           Usada para corrigir desbalanceamento Esquerda-Esquerda (LL) ou Esquerda-Direita (LR, após uma rotação esquerda no filho).
              z                            y       <-- Nova Raiz
             / \                          / \
            y   T4  -> Rotação Direita -> x   z     <-- z desce
           / \                          / \ / \
          x   T3                       T1 T2T3 T4
         / \
        T1  T2
        """
        print(f"INFO AVL: Rotação Direita em Nó ID {z.id}") # Debug
        y = z.esquerda  # 'y' é o filho esquerdo de 'z'
        T3 = y.direita # 'T3' é a subárvore direita de 'y' (que ficará à esquerda de 'z')

        # Realiza a rotação (troca as conexões dos ponteiros)
        y.direita = z  # 'y' agora aponta para 'z' à sua direita
        z.esquerda = T3  # 'z' agora aponta para 'T3' à sua esquerda

        # Atualiza as alturas dos nós que mudaram de posição
        # IMPORTANTE: Atualiza 'z' (que desceu) PRIMEIRO, pois sua altura depende de T3 e T4
        self._atualizar_altura(z)
        # IMPORTANTE: Atualiza 'y' (que subiu) DEPOIS, pois sua altura depende da nova altura de 'z'
        self._atualizar_altura(y)

        # Retorna a nova raiz da subárvore que foi rotacionada ('y')
        return y

    def _rotacao_esquerda(self, y):
        r"""Executa uma rotação simples à esquerda na subárvore com raiz y.
           Usada para corrigir desbalanceamento Direita-Direita (RR) ou Direita-Esquerda (RL, após uma rotação direita no filho).
            y                            z       <-- Nova Raiz
           / \                          / \
          T1  z   -> Rotação Esquerda -> y   x     <-- y desce
             / \                        / \ / \
            T2  x                      T1 T2T3 T4
               / \
              T3 T4
        """
        print(f"INFO AVL: Rotação Esquerda em Nó ID {y.id}") # Debug
        z = y.direita # 'z' é o filho direito de 'y'
        T2 = z.esquerda # 'T2' é a subárvore esquerda de 'z' (que ficará à direita de 'y')

        # Realiza a rotação
        z.esquerda = y # 'z' agora aponta para 'y' à sua esquerda
        y.direita = T2 # 'y' agora aponta para 'T2' à sua direita

        # Atualiza as alturas
        # IMPORTANTE: Atualiza 'y' (que desceu) PRIMEIRO, pois sua altura depende de T1 e T2
        self._atualizar_altura(y)
        # IMPORTANTE: Atualiza 'z' (que subiu) DEPOIS, pois sua altura depende da nova altura de 'y'
        self._atualizar_altura(z)

        # Retorna a nova raiz da subárvore que foi rotacionada ('z')
        return z

    # -----------------------------------------------------------------
    # --- MÉTODO INSERIR (MODIFICADO PARA AVL) ---
    # -----------------------------------------------------------------

    def inserir(self, objeto_chamado_original):
        """Método público para inserir um novo chamado na árvore AVL."""
        # Chama a função auxiliar recursiva para inserir E balancear
        # O resultado (a nova raiz da árvore, possivelmente rotacionada) é salvo.
        self.raiz = self._inserir_avl(self.raiz, objeto_chamado_original)

    def _inserir_avl(self, no_atual, objeto_chamado_original):
        """Função auxiliar recursiva para inserir e balancear (AVL)."""

        # PASSO 1: Inserção Normal da BST (Recursiva)
        # Se chegamos a um ponto vazio (None) na árvore, criamos o novo nó aqui.
        if no_atual is None:
            print(f"INFO AVL: Inserindo ID {objeto_chamado_original.idChamado}") # Debug
            # Cria o nó usando o construtor do 'no.py' (que já define altura=1)
            return No(objeto_chamado_original) # Retorna o novo nó criado para ser conectado pelo pai

        # Decide para qual lado descer recursivamente com base no ID
        if objeto_chamado_original.idChamado < no_atual.id:
            # Chama recursivamente para a esquerda. O resultado (a raiz da subárvore esquerda,
            # possivelmente modificada pelo balanceamento) é reconectado.
            no_atual.esquerda = self._inserir_avl(no_atual.esquerda, objeto_chamado_original)
        elif objeto_chamado_original.idChamado > no_atual.id:
            # Chama recursivamente para a direita e reconecta.
            no_atual.direita = self._inserir_avl(no_atual.direita, objeto_chamado_original)
        else:
            # ID duplicado. Em BSTs padrão, não fazemos nada.
            print(f"AVISO AVL: ID {objeto_chamado_original.idChamado} já existe. Inserção ignorada.") # Debug
            return no_atual # Retorna o nó atual sem modificação

        # === INÍCIO DA LÓGICA AVL PÓS-INSERÇÃO ===
        # Esta parte é executada DEPOIS que a inserção ocorreu em alguma subárvore abaixo
        # e a chamada recursiva retornou, subindo de volta para este 'no_atual'.

        # PASSO 2: Atualizar a Altura do nó atual
        # A altura pode ter mudado porque um novo nó foi adicionado abaixo dele.
        self._atualizar_altura(no_atual)

        # PASSO 3: Calcular o Fator de Balanceamento deste nó
        balance = self._get_fator_balanceamento(no_atual)
        print(f"INFO AVL: Verificando Nó {no_atual.id}, Altura: {no_atual.altura}, Balance: {balance}") # Debug

        # PASSO 4: Verificar Desbalanceamento (se balance > 1 ou < -1) e Aplicar Rotações

        # --- CASOS DE DESBALANCEAMENTO À ESQUERDA ---
        if balance > 1:
            # Para decidir entre LL e LR, olhamos para onde o novo nó foi inserido
            # (ou equivalentemente, o fator de balanceamento do filho esquerdo)
            
            # Subcaso Esquerda-Esquerda (LL)
            # O desbalanceamento foi causado por inserção na subárvore ESQUERDA do filho ESQUERDO.
            # Condição: O fator do filho esquerdo é >= 0 (ou seja, não pende para a direita)
            if self._get_fator_balanceamento(no_atual.esquerda) >= 0:
                print(f"INFO AVL: Detectado LL em {no_atual.id}. Rotacionando...") # Debug
                # Corrigimos com uma única Rotação Direita no nó atual.
                return self._rotacao_direita(no_atual)
            
            # Subcaso Esquerda-Direita (LR)
            # O desbalanceamento foi causado por inserção na subárvore DIREITA do filho ESQUERDO.
            # Condição: O fator do filho esquerdo é < 0 (pende para a direita)
            else:
                print(f"INFO AVL: Detectado LR em {no_atual.id}. Rotacionando...") # Debug
                # Corrigimos com duas rotações:
                # 1. Rotação Esquerda no FILHO ESQUERDO.
                no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
                # 2. Rotação Direita no NÓ ATUAL.
                return self._rotacao_direita(no_atual)

        # --- CASOS DE DESBALANCEAMENTO À DIREITA ---
        if balance < -1:
            # Para decidir entre RR e RL, olhamos o fator de balanceamento do filho direito.

            # Subcaso Direita-Direita (RR)
            # O desbalanceamento foi causado por inserção na subárvore DIREITA do filho DIREITO.
            # Condição: O fator do filho direito é <= 0 (não pende para a esquerda)
            if self._get_fator_balanceamento(no_atual.direita) <= 0:
                print(f"INFO AVL: Detectado RR em {no_atual.id}. Rotacionando...") # Debug
                # Corrigimos com uma única Rotação Esquerda no nó atual.
                return self._rotacao_esquerda(no_atual)
            
            # Subcaso Direita-Esquerda (RL)
            # O desbalanceamento foi causado por inserção na subárvore ESQUERDA do filho DIREITO.
            # Condição: O fator do filho direito é > 0 (pende para a esquerda)
            else:
                print(f"INFO AVL: Detectado RL em {no_atual.id}. Rotacionando...") # Debug
                # Corrigimos com duas rotações:
                # 1. Rotação Direita no FILHO DIREITO.
                no_atual.direita = self._rotacao_direita(no_atual.direita)
                # 2. Rotação Esquerda no NÓ ATUAL.
                return self._rotacao_esquerda(no_atual)

        # Se não houve desbalanceamento (balance entre -1 e 1), retorna o nó atual
        # (com sua altura possivelmente atualizada) para a chamada recursiva anterior.
        return no_atual

    # -----------------------------------------------------------------
    # --- MÉTODO REMOVER (MODIFICADO PARA AVL) ---
    # -----------------------------------------------------------------

    def remover(self, id_para_remover):
        """Método público para remover um nó da árvore AVL."""
        # Chama a função auxiliar recursiva para remover E balancear
        # O resultado (a nova raiz da árvore, possivelmente rotacionada) é salvo.
        self.raiz = self._remover_avl(self.raiz, id_para_remover)

    def _remover_avl(self, no_atual, id_procurado):
        """Função auxiliar recursiva para remover e balancear (AVL)."""

        # PARTE 1: Busca e Remoção Normal da BST (Recursiva)

        # Caso base da busca: Nó não encontrado
        if no_atual is None:
            print(f"AVISO AVL: ID {id_procurado} não encontrado para remoção.") # Debug
            return no_atual # Retorna None, nada a fazer

        # Continua a busca recursivamente
        if id_procurado < no_atual.id:
            no_atual.esquerda = self._remover_avl(no_atual.esquerda, id_procurado)
        elif id_procurado > no_atual.id:
            no_atual.direita = self._remover_avl(no_atual.direita, id_procurado)
        else:
            # NÓ ENCONTRADO! Aplica a lógica de remoção BST
            print(f"INFO AVL: Removendo ID {id_procurado}...") # Debug

            # Caso 1 ou 2: Nó com 0 ou 1 filho
            if no_atual.esquerda is None:
                temp = no_atual.direita # Guarda o filho direito (pode ser None)
                print(f"INFO AVL: Remoção Caso 1/2 (sem filho esquerdo). Substituto é Nó ID {temp.id if temp else 'None'}.") # Debug
                # Ao retornar temp, o pai do no_atual se conectará a ele.
                # O no_atual é efetivamente removido (não fazemos 'del' ou 'None' aqui).
                return temp # Retorna o substituto (filho direito ou None)
            elif no_atual.direita is None:
                temp = no_atual.esquerda # Guarda o filho esquerdo
                print(f"INFO AVL: Remoção Caso 1/2 (sem filho direito). Substituto é Nó ID {temp.id if temp else 'None'}.") # Debug
                return temp # Retorna o substituto (filho esquerdo)

            # Caso 3: Nó com 2 filhos
            print(f"INFO AVL: Remoção Caso 3 (dois filhos) em Nó ID {no_atual.id}.") # Debug
            # Encontra o sucessor em-ordem (menor nó da subárvore direita)
            substituto = self._encontrar_menor_no(no_atual.direita)
            print(f"INFO AVL: Sucessor encontrado: ID {substituto.id}") # Debug
            # Copia os dados do substituto para o nó atual (sobrescreve o nó a ser removido)
            no_atual.id = substituto.id
            no_atual.chamado_completo = substituto.chamado_completo
            # Remove recursivamente o nó substituto da subárvore direita.
            # A chamada recursiva _remover_avl cuidará do balanceamento lá embaixo.
            print(f"INFO AVL: Chamando remoção recursiva para o sucessor ID {substituto.id} na subárvore direita.") # Debug
            no_atual.direita = self._remover_avl(no_atual.direita, substituto.id)
            # O nó 'no_atual' agora contém os dados do substituto e a subárvore direita
            # está corrigida (sem o substituto original e balanceada).

        # === INÍCIO DA LÓGICA AVL PÓS-REMOÇÃO ===
        # Esta parte é executada DEPOIS que a remoção ocorreu em alguma subárvore abaixo
        # OU depois que os dados foram copiados no Caso 3.

        # Se a árvore/subárvore ficou vazia após a remoção (caso do último nó que foi removido e era Caso 1/2)
        # O 'return temp' nos casos 1/2 já tratou isso, mas checamos de novo por segurança
        if no_atual is None:
             return no_atual # Retorna None

        # PASSO 1: Atualizar a Altura do nó atual
        # A altura pode ter mudado porque um nó foi removido abaixo dele.
        self._atualizar_altura(no_atual)

        # PASSO 2: Calcular o Fator de Balanceamento
        balance = self._get_fator_balanceamento(no_atual)
        print(f"INFO AVL: Verificando Nó {no_atual.id} pós-remoção, Altura: {no_atual.altura}, Balance: {balance}") # Debug

        # PASSO 3: Verificar Desbalanceamento (se balance > 1 ou < -1) e Aplicar Rotações
        # A lógica aqui é um pouco diferente da inserção, pois o desbalanceamento
        # pode vir da subárvore oposta à remoção. Precisamos checar o fator dos FILHOS.

        # --- CASOS DE DESBALANCEAMENTO À ESQUERDA (balance > 1) ---
        if balance > 1:
            # Para decidir entre LL e LR, olhamos o fator de balanceamento do FILHO ESQUERDO.
            # Subcaso Esquerda-Esquerda (LL): O filho esquerdo não pende para a direita (fator >= 0).
            if self._get_fator_balanceamento(no_atual.esquerda) >= 0:
                print(f"INFO AVL: Detectado LL pós-remoção em {no_atual.id}. Rotacionando...") # Debug
                return self._rotacao_direita(no_atual)
            # Subcaso Esquerda-Direita (LR): O filho esquerdo pende para a direita (fator < 0).
            else:
                print(f"INFO AVL: Detectado LR pós-remoção em {no_atual.id}. Rotacionando...") # Debug
                no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda) # Rotação Esquerda no filho
                return self._rotacao_direita(no_atual) # Rotação Direita no atual

        # --- CASOS DE DESBALANCEAMENTO À DIREITA (balance < -1) ---
        if balance < -1:
            # Para decidir entre RR e RL, olhamos o fator de balanceamento do FILHO DIREITO.
            # Subcaso Direita-Direita (RR): O filho direito não pende para a esquerda (fator <= 0).
            if self._get_fator_balanceamento(no_atual.direita) <= 0:
                print(f"INFO AVL: Detectado RR pós-remoção em {no_atual.id}. Rotacionando...") # Debug
                return self._rotacao_esquerda(no_atual)
            # Subcaso Direita-Esquerda (RL): O filho direito pende para a esquerda (fator > 0).
            else:
                print(f"INFO AVL: Detectado RL pós-remoção em {no_atual.id}. Rotacionando...") # Debug
                no_atual.direita = self._rotacao_direita(no_atual.direita) # Rotação Direita no filho
                return self._rotacao_esquerda(no_atual) # Rotação Esquerda no atual

        # Se não houve desbalanceamento, retorna o nó atual (com altura atualizada)
        # para a chamada recursiva anterior conectar corretamente.
        return no_atual


    # -----------------------------------------------------------------
    # --- MÉTODOS DE BUSCA, LISTAGEM, CONTAGEM (NÃO MUDARAM PARA AVL) ---
    # -----------------------------------------------------------------

    def buscar(self, id_procurado):
        """Busca por um nó especifico na árvore usando o ID."""
        atual = self.raiz
        while atual is not None:
            if id_procurado == atual.id:
                return atual
            elif id_procurado < atual.id:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def _encontrar_menor_no(self, no_atual):
        """Função 'ajudante' para encontrar o nó com o menor ID."""
        # Necessário para o Caso 3 da remoção
        while no_atual.esquerda is not None:
            no_atual = no_atual.esquerda
        return no_atual

    def listar_em_ordem(self):
        """Método público que retorna uma LISTA de nós em ordem crescente de ID."""
        lista_ordenada = []
        self._listar_em_ordem_recursivo(self.raiz, lista_ordenada)
        return lista_ordenada

    def _listar_em_ordem_recursivo(self, no_atual, lista):
        """Método 'ajudante' privado que percorre a árvore (E-C-D)."""
        if no_atual is not None:
            self._listar_em_ordem_recursivo(no_atual.esquerda, lista)
            lista.append(no_atual)
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
        # Usado pela função de visualização para ajustar o tamanho
        def _count_recursive(node):
            if node is None: return 0
            return 1 + _count_recursive(node.esquerda) + _count_recursive(node.direita)
        return _count_recursive(self.raiz)

    # -----------------------------------------------------------------
    # --- MÉTODO DE VISUALIZAÇÃO (Graphviz - Adicionado Altura/Balance) ---
    # -----------------------------------------------------------------

    def visualizar_arvore(self, appearance_mode='dark'):
        """Gera a imagem da árvore BST/AVL e a retorna como dados PNG (bytes)."""
        if self.raiz is None:
            print("INFO: Árvore está vazia. Nada para visualizar.")
            raise ValueError("A árvore está vazia. Adicione chamados primeiro.")

        total_nodes = self.get_node_count()
        base_font_size = 14; min_font_size = 8; step = 5; reduction = 1
        font_reduction = max(0, (total_nodes // step) * reduction)
        node_font_size = max(min_font_size, base_font_size - font_reduction)
        edge_font_size = max(min_font_size - 1, node_font_size - 2)
        print(f"INFO: Total de nós: {total_nodes}. Tamanho da fonte calculado: {node_font_size}pt")

        if appearance_mode == 'dark':
            bg_color = "#2B2B2B"; node_color = "#343638"; text_color = "white"; edge_color = "white"
        else: # modo 'light'
            bg_color = "#EBEBEB"; node_color = "#DDEFFF"; text_color = "black"; edge_color = "black"

        dot = graphviz.Digraph(comment='Árvore de Chamados AVL')
        dot.attr(dpi='150', bgcolor=bg_color, rankdir='TB') # DPI alto para qualidade
        dot.attr('node', shape='record', fontname='Arial', fontsize=str(node_font_size), style='filled', fillcolor=node_color, fontcolor=text_color)
        dot.attr('edge', fontname='Arial', fontsize=str(edge_font_size), color=edge_color)

        def add_nodes_edges(node):
            if node is None: return

            # Limpa o título para evitar erros no Graphviz
            titulo_limpo = str(node.chamado_completo.titulo[:25]).encode('utf-8', 'ignore').decode('utf-8')

            # --- MODIFICAÇÃO AVL: MOSTRAR ALTURA E FATOR DE BALANCEAMENTO ---
            altura = self._get_altura(node)
            fb = self._get_fator_balanceamento(node)
            label_str = (f"{{ID: {str(node.id)} (H:{altura}|B:{fb}) | " # Mostra H=altura, B=fator
                         f"{titulo_limpo}... | "
                         f"Prio: {str(node.chamado_completo.prioridade)}}}")
            # --- FIM DA MODIFICAÇÃO ---

            dot.node(str(node.id), label=label_str)

            # Conecta com os filhos recursivamente
            if node.esquerda:
                dot.edge(str(node.id), str(node.esquerda.id), label="< ID")
                add_nodes_edges(node.esquerda)

            if node.direita:
                dot.edge(str(node.id), str(node.direita.id), label=">= ID") # Label >= pois inserção trata igual como direita
                add_nodes_edges(node.direita)

        # Inicia a recursão a partir da raiz
        add_nodes_edges(self.raiz)

        try:
            # Renderiza diretamente para a memória no formato PNG
            png_data = dot.pipe(format='png')
            return png_data # Retorna os bytes da imagem
        except graphviz.backend.execute.ExecutableNotFound:
            print("ERRO GRANDE: Executável 'dot' do Graphviz não encontrado.")
            raise Exception("Graphviz (dot) não foi encontrado.\nVerifique a instalação e o PATH do sistema.")
        except Exception as e:
            print(f"ERRO GRANDE ao renderizar a árvore: {e}")
            raise e

