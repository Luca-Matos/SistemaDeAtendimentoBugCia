# models.py
from datetime import datetime

# As classes Cliente e Atendente não mudam
class Cliente:
    def __init__(self, idCliente: int, nomeCliente: str, email: str):
        self.idCliente = idCliente
        self.nomeCliente = nomeCliente
        self.email = email

    def __str__(self):
        return f"Cliente: {self.nomeCliente}"

class Atendente:
    def __init__(self, idAtendente: int, nomeAtendente: str):
        self.idAtendente = idAtendente
        self.nomeAtendente = nomeAtendente

    def __str__(self):
        return f"Atendente: {self.nomeAtendente}"

class Chamado:
    _id_counter = 1

    # MUDANÇA: Adicionamos 'titulo' ao construtor
    def __init__(self, cliente_ou_atendente, titulo: str, descricao: str):
        self.idChamado = Chamado._id_counter
        Chamado._id_counter += 1
        
        self.requisitante = cliente_ou_atendente
        self.titulo = titulo # NOVO CAMPO
        self.descricao = descricao
        self.prioridade = 1
        self.status = "Aberto"
        self.dataAbertura = datetime.now()

    def resolver(self):
        self.status = "Resolvido"

    # MUDANÇA: O método de atualização agora aceita o novo título e descrição
    def atualizar(self, novo_titulo, nova_descricao, nova_prioridade):
        self.titulo = novo_titulo
        self.descricao = nova_descricao
        self.prioridade = int(nova_prioridade)

    # MUDANÇA: A representação em string agora mostra o título
    def __str__(self):
        return (f"ID: {self.idChamado} | Título: {self.titulo} | "
                f"Data: {self.dataAbertura.strftime('%d/%m/%Y %H:%M')} | "
                f"Prioridade: {self.prioridade} | Status: {self.status}")