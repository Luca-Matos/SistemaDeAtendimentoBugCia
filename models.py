# models.py
from datetime import datetime

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
    # Usamos um contador estático para garantir IDs únicos
    _id_counter = 1

    def __init__(self, cliente_ou_atendente, descricao: str):
        self.idChamado = Chamado._id_counter
        Chamado._id_counter += 1
        
        self.requisitante = cliente_ou_atendente
        self.descricao = descricao
        self.prioridade = 1  # Prioridade padrão
        self.status = "Aberto"  # Status pode ser "Aberto", "Resolvido"
        self.dataAbertura = datetime.now()

    def resolver(self):
        self.status = "Resolvido"
        print(f"Chamado {self.idChamado} resolvido.")

    # A remoção será tratada pela lista, mas a atualização fica aqui
    def atualizar(self, nova_descricao, nova_prioridade):
        self.descricao = nova_descricao
        self.prioridade = int(nova_prioridade)
        print(f"Chamado {self.idChamado} atualizado.")

    def __str__(self):
        return (f"ID: {self.idChamado} | Título: {self.descricao[:30]}... | "
                f"Data: {self.dataAbertura.strftime('%d/%m/%Y %H:%M')} | "
                f"Prioridade: {self.prioridade} | Status: {self.status}")