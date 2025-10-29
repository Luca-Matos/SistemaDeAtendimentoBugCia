# Precisei criar esse arquivo para definir o que é cada nó da árvore. no nosso caso, um nó vai guardar os dados de um chamado e também ter os ponteiros para os nós filhos (esquerda e direita)

#relembrando rapidinho que esse self. é a referencia ao próprio objeto que esta sendo criado, ou seja, cada vez que eu criar um novo nó, esse self vai ser diferente, pq vai ser um novo nó que eu estou criando. 
class No:
    
    # o _init_ recebe o objeto 'Chamado' ORIGINAL e COMPLETO.
    def __init__(self, objeto_chamado_original):
        
        # dados do nó
        
        # ID unica do chamado,usado para montar e organizar a nossa árvore, funciona como uma etiqueta
        # Nós copiamos o ID para cá para que a árvore (arvore_bst.py)
        # possa fazer a busca rápida (if no.id < atual.id)
        self.id = objeto_chamado_original.idChamado 
        
        # Guardamos o objeto 'Chamado' original e completo
        # Agora temos acesso a TUDO: .titulo, .descricao, .prioridade
        # e, o mais importante, a PILHA de rascunhos (.desfazer_alteracao())
        self.chamado_completo = objeto_chamado_original
        
        # (As linhas self.cliente, self.titulo, etc. foram removidas
        # porque agora elas estão DENTRO do 'self.chamado_completo')

        #ponteiros da Árvore 
        # Começam como None, pois um novo nó ainda não está conectado a ninguém
        self.esquerda = None  #vai apontar para um nó cujo ID é menor que o ID do nó atual
        self.direita = None  #vai apontar para um nó cujo ID é maior que o ID do nó atual
        # essas duas linhas acima são as que fazem a ligação entre os nós, conectando a árvore e eles se baseiam nos valores dos ids para se organizarem!!! 
        self.altura = 1  # altura do nó na árvore, começa em 1 para contar o próprio nó

    def __str__(self):
        # Função auxiliar para facilitar a impressão do nó durante os testes
        return f"ID: {self.id} ({self.chamado_completo.titulo})"
    
# fim da classe no

#esse código é um molde para criar um objeto
# Ele guarda o ID (para a árvore) e o objeto 'Chamado' completo 
#para o "Desfazer" e o 'main.py' funcionarem
# As duas últimas linhas self são os ponteiros que vão se conectar aos outros nós da árvore