# linked_list.py
from models import Chamado

# O "Nó" ou "Elo" da nossa lista. Cada nó guarda um chamado e a referência para o próximo.
class Node:
    def __init__(self, chamado: Chamado):
        self.chamado = chamado
        self.proximo = None

# A Lista Encadeada em si, que gerencia os nós.
class SistemaDeAtendimento:
    def __init__(self):
        self.head = None # O início da lista (o primeiro chamado)
        self._tamanho = 0

    def adicionarChamado(self, chamado: Chamado):
        """ Adiciona um chamado no FINAL da lista. """
        novo_node = Node(chamado)
        if not self.head:
            self.head = novo_node
        else:
            atual = self.head
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_node
        self._tamanho += 1

    def removerChamado(self, id_chamado_para_remover: int):
        """ Remove um chamado da lista pelo seu ID. """
        if not self.head:
            return False

        # Caso especial: o chamado a ser removido é o primeiro
        if self.head.chamado.idChamado == id_chamado_para_remover:
            self.head = self.head.proximo
            self._tamanho -= 1
            return True

        # Procura o chamado na lista
        anterior = self.head
        atual = self.head.proximo
        while atual:
            if atual.chamado.idChamado == id_chamado_para_remover:
                anterior.proximo = atual.proximo # "Pula" o nó atual
                self._tamanho -= 1
                return True
            anterior = atual
            atual = atual.proximo
        
        return False # Não encontrou o chamado

    def to_list(self):
        """ Converte a lista encadeada para uma lista Python comum para facilitar a ordenação. """
        chamados = []
        atual = self.head
        while atual:
            chamados.append(atual.chamado)
            atual = atual.proximo
        return chamados

    def listarPorOrdemDeChegada(self):
        """ A ordem natural da lista encadeada já é a ordem de chegada. """
        return self.to_list()

    def listarPorPrioridade(self):
        """ Retorna uma NOVA lista ordenada por prioridade. """
        chamados = self.to_list()
        # Ordena pela prioridade (maior primeiro) e depois pela data (mais antigo primeiro)
        chamados.sort(key=lambda c: (-c.prioridade, c.dataAbertura))
        return chamados
    
    def __len__(self):
        return self._tamanho