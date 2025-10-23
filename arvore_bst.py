# arvore_bst.py

# Importamos a classe no, pois a nossa árvore vai criar e gerenciar objetos dessa classe
from no import No

class ArvoreBST:

    #esta classe define a estrutura da ÁrvODE Binária de Busca 
    
    #no.py = O molde do Nó
    # main.py = Cria a pasta de dados (Chamado)
    # arvore_bst.py: Define a classe ArvoreBST, que gerencia os nós e contém os métodos (ações) de inserir, buscar e listar

    
    def __init__(self): # é o construtor que inicializa a árvore
        
        self.raiz = None #a raiz começa com none pq n tem nenhum nó por enquanto 
        

   
    # Ela recebe o objeto 'Chamado' original e completo.
    def inserir(self, objeto_chamado_original):

        #Método público para inserir um novo chamado, este é o método que será chamado pelo arquivo principal (modern_main.py)para guardar um novo chamado na árvore
        
        # 1. Cria o nó, passando o objeto 'Chamado' original e completo.
        #(O 'no.py' vai extrair o ID e guardar o 'Chamado' original)
        novo_no = No(objeto_chamado_original)

        # 2. Verifica se a árvore está vazia
        if self.raiz is None:
            # se estiver vazia, o novo nó se torna a raiz
            self.raiz = novo_no
        else:
            # se não estiver vazia, nós vamos precisar de uma função 'ajudante' para encontrar o lugar certo para inserir o novo nó, lembrando que a árvore deve estar sempre ordenada e no nosso caso é analisando o id do chamado
            self._inserir_no(novo_no) #essa é a função ajudante que faz o trabalho pesado de encontrar o lugar certo para o novo nó(esquerda ou direita)

    def _inserir_no(self, novo_no): #Função auxiliar para inserir um novo nó na árvore
        
        # Começamos pela raiz
        atual = self.raiz #isso aqui é uma variavel temporária que vai ajudar a gente a navegar pela árvore, é a sinalização de que a busca vai começar da raiz 

        while True: #loop infinito que só vai parar quando a gente encontrar o lugar certo para inserir o novo nó
            if novo_no.id < atual.id: # se o ID do novo nó for menor, vamos para a esquerda
                if atual.esquerda is None:
                    # se for menor e não houver outro nó entao inserimos o novo nó aqui
                    atual.esquerda = novo_no #é como uma confirmação o novo nó fica aqui
                    break
                else:
                    # se já houver um próximo nó à esquerda,  então continuamos a busca de um lugar vazio
                    atual = atual.esquerda
            else:
                # se o ID do novo nó for maior ou igual, vamos para a direita
                if atual.direita is None:
                    # se não houver um próximo nó à direita, inserimos o novo nó aqui
                    atual.direita = novo_no #confirmação de novo
                    break
                else:
                    # se já houver um próximo nó à direita, continuamos a busca
                    atual = atual.direita
                    
    def buscar(self, id_procurado):
        #busca por um nó especifico na árvore usando o ID.Retorna o objeto nó se encontrar, ou None se não encontrar
        # Começamos a busca sempre pela raiz!!! 
        atual = self.raiz

        #o loop continua enquanto 'atual' não for None...
        while atual is not None:
            
            # 1. ACHAMOS!
            if id_procurado == atual.id:
                return atual

            # 2. O ID procurado é MENOR que o ID do nó atual
            elif id_procurado < atual.id:
                atual = atual.esquerda
            
            # 3. Se não é igual nem menor, só pode ser MAIOR
            else:
                atual = atual.direita
        
        #se o loop 'while' terminar, significa que não encontramos o nó
        return None
    
    def listar_em_ordem(self):
    
        
        
        #método público que retorna uma LISTA de nós em ordem crescente de ID
        
        lista_ordenada = []
        self._listar_em_ordem_recursivo(self.raiz, lista_ordenada)
        return lista_ordenada

    def _listar_em_ordem_recursivo(self, no_atual, lista):
        #método 'ajudante' privado que percorre a árvore recursivamente
        if no_atual is not None:
            
            # PASSO 1: VAI PARA A ESQUERDA
            self._listar_em_ordem_recursivo(no_atual.esquerda, lista)

            # PASSO 2: VISITA O NÓ ATUAL
            lista.append(no_atual)

            # PASSO 3: VAI PARA A DIREITA
            self._listar_em_ordem_recursivo(no_atual.direita, lista)
        
    def remover(self, id_para_remover):
        #método público para remover um nó

        self.raiz = self._remover_no(self.raiz, id_para_remover)

    def _remover_no(self, no_atual, id_procurado):
        #método 'ajudante' privado que procura o nó e o remove

        #  PARTE 1: encontrar o nó p ser removido
        if no_atual is None:
            return no_atual

        if id_procurado < no_atual.id:
            no_atual.esquerda = self._remover_no(no_atual.esquerda, id_procurado)
        
        elif id_procurado > no_atual.id:
            no_atual.direita = self._remover_no(no_atual.direita, id_procurado)
        
        #se achamos o nó
        else:
            #PARTE 2: LÓGICA DE REMOÇÃO 
            
            
            if no_atual.esquerda is None and no_atual.direita is None:
                return None 

            elif no_atual.esquerda is None:
                return no_atual.direita 

            elif no_atual.direita is None:
                return no_atual.esquerda 
            
           
            else:
                # 1. Encontra o "substituto" (do menor nó na subárvore direita)
                substituto = self._encontrar_menor_no(no_atual.direita)

                # 2. Copia os dados do 'substituto' por cima dos dados do nó que queremos remover
                # AGORA SÓ PRECISA COPIAR O ID E O OBJETO COMPLETO
                no_atual.id = substituto.id
                no_atual.chamado_completo = substituto.chamado_completo
                # 3. Remove o nó 'substituto' da subárvore direita
                no_atual.direita = self._remover_no(no_atual.direita, substituto.id)

        return no_atual

    def _encontrar_menor_no(self, no_atual):
       #Função 'ajudante' para encontrar o nó com o menor ID
    
        while no_atual.esquerda is not None:
            no_atual = no_atual.esquerda
        
        return no_atual
    
    def listar_por_prioridade(self, prioridade_desejada):

        #método público para encontrar todos os nós que correspondem a uma prioridade específica e retornar uma lista com esses nós
        
        # 1. Pega a lista COMPLETA de todos os nós 
        todos_os_nos = self.listar_em_ordem()
        
        # 2. Cria uma lista vazia
        lista_filtrada = []

        # 3. Percorre a lista completa, nó por nó
        for no in todos_os_nos:
            
            # 4. Verifica se a prioridade do nó atual é a que queremos.
            #Agora precisamos olhar DENTRO do 'chamado_completo'
            if no.chamado_completo.prioridade == prioridade_desejada:
                
                # 5. Se for, adiciona o nó na nossa lista filtrada.
                lista_filtrada.append(no)
        
        # 6. Retorna a nova lista
        return lista_filtrada