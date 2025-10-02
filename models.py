# models.py
"""
Define as classes de modelo de dados para a aplicação HelpDesk:
- Cliente: Representa o usuário que abre um chamado.
- Atendente: Representa o funcionário que atende ao chamado.
- Chamado: Representa o ticket de suporte, com sua lógica de negócio,
           incluindo o histórico de alterações para a função 'desfazer'
           e rastreamento para o relatório PDF.
"""
from datetime import datetime
from collections import deque
import copy
from fpdf import FPDF


# --- CLASSES DE ENTIDADE ---

class Cliente:
    """Representa um cliente no sistema."""

    def __init__(self, idCliente: int, nomeCliente: str, email: str):
        self.idCliente = idCliente
        self.nomeCliente = nomeCliente
        self.email = email

    def __str__(self):
        return f"Cliente: {self.nomeCliente}"


class Atendente:
    """Representa um atendente no sistema."""

    def __init__(self, idAtendente: int, nomeAtendente: str):
        self.idAtendente = idAtendente
        self.nomeAtendente = nomeAtendente

    def __str__(self):
        return f"Atendente: {self.nomeAtendente}"


# --- CLASSE PRINCIPAL DE NEGÓCIO ---

class Chamado:
    """
    Representa um chamado (ticket) de suporte no sistema.
    Gerencia seu próprio histórico de alterações para a funcionalidade de 'desfazer'
    e para a geração de relatórios.
    """
    _id_counter = 1

    def __init__(self, cliente_ou_atendente, titulo: str, descricao: str):
        self.idChamado = Chamado._id_counter
        Chamado._id_counter += 1
        self.requisitante = cliente_ou_atendente
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = 1
        self.status = "Aberto"
        self.dataAbertura = datetime.now()
        self.ultimo_editor = cliente_ou_atendente

        # NOVO: Adiciona o controle de versão.
        self.versao = 1

        self._historico_alteracoes = []
        self._historico_rascunhos = deque(maxlen=20)
        self.salvar_rascunho()
        self._registrar_alteracao("Chamado criado")

    def _registrar_alteracao(self, detalhe: str):
        data = datetime.now()
        self._historico_alteracoes.append({'data': data, 'detalhes': detalhe})

    # NOVO: Método para registrar a visualização pelo atendente.
    def registrar_visualizacao(self, ator):
        """Registra no histórico que um atendente visualizou o chamado."""
        if isinstance(ator, Atendente):
            self._registrar_alteracao(f"Chamado visualizado por: {ator.nomeAtendente}")

    def resolver(self, ator):
        if self.status != "Resolvido":
            self.salvar_rascunho()
            self.status = "Resolvido"
            self.ultimo_editor = ator
            self.versao += 1  # Incrementa a versão
            self._registrar_alteracao(f"Status alterado para '{self.status}'")

    def atualizar(self, novo_titulo, nova_descricao, nova_prioridade, ator):
        self.salvar_rascunho()
        alteracoes_detectadas = []

        if isinstance(ator, Cliente):
            if self.titulo != novo_titulo:
                alteracoes_detectadas.append(f"Título alterado para: '{novo_titulo}'")
                self.titulo = novo_titulo
            if self.descricao != nova_descricao:
                preview = nova_descricao[:100].strip().replace('\n', ' ') + ('...' if len(nova_descricao) > 100 else '')
                alteracoes_detectadas.append(f"Descrição alterada para: '{preview}'")
                self.descricao = nova_descricao

        elif isinstance(ator, Atendente):
            try:
                nova_prioridade_int = int(nova_prioridade)
                if self.prioridade != nova_prioridade_int:
                    alteracoes_detectadas.append(
                        f"Prioridade alterada de '{self.prioridade}' para '{nova_prioridade_int}'")
                    self.prioridade = nova_prioridade_int
            except (ValueError, TypeError):
                print(
                    f"Erro: valor de prioridade inválido ('{nova_prioridade}'). Nenhuma alteração de prioridade foi feita.")

        if alteracoes_detectadas:
            self._registrar_alteracao(", ".join(alteracoes_detectadas))
            self.ultimo_editor = ator
            self.versao += 1  # Incrementa a versão

    def gerar_relatorio_pdf(self, nome_arquivo="relatorio_chamado.pdf"):
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Relatório de Alterações do Chamado', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 5, f'ID: {self.idChamado} | Título: {self.titulo} | Versão: {self.versao}', 0, 1, 'L')
        req_nome = self.requisitante.nomeCliente if hasattr(self.requisitante, 'nomeCliente') else str(
            self.requisitante)
        pdf.cell(0, 5, f'Requisitante: {req_nome} | Status Atual: {self.status}', 0, 1, 'L')
        pdf.cell(0, 5, f'Data Abertura: {self.dataAbertura.strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'L')
        pdf.cell(0, 5, '-' * 50, 0, 1, 'C')
        COL_DATA, COL_DETALHES, LINE_HEIGHT = 40, 150, 7
        pdf.set_fill_color(200, 220, 255);
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(COL_DATA, LINE_HEIGHT, 'Data e Hora', 1, 0, 'C', 1)
        pdf.cell(COL_DETALHES, LINE_HEIGHT, 'Detalhes da Alteração', 1, 1, 'C', 1)
        pdf.set_font('Arial', '', 10)
        for registro in self._historico_alteracoes:
            data_formatada = registro['data'].strftime("%d/%m/%Y %H:%M:%S")
            detalhes = registro['detalhes']
            y_inicial = pdf.get_y()
            pdf.set_x(pdf.get_x() + COL_DATA)
            pdf.multi_cell(COL_DETALHES, 6, detalhes, 1, 'L', 0)
            y_final = pdf.get_y()
            altura_usada = y_final - y_inicial
            pdf.set_xy(pdf.l_margin, y_inicial)
            pdf.cell(COL_DATA, altura_usada, data_formatada, 1, 0, 'L', 0)
            pdf.set_xy(pdf.l_margin, y_final)
        pdf.output(nome_arquivo, 'F')

    def salvar_rascunho(self):
        rascunho = copy.copy(self)
        self._historico_rascunhos.append(rascunho)

    def desfazer_alteracao(self, ator):
        if isinstance(ator, Cliente) and isinstance(self.ultimo_editor, Atendente):
            print("AVISO: Clientes não podem desfazer alterações feitas por atendentes.")
            return False
        if len(self._historico_rascunhos) > 1:
            estado_para_reverter = self._historico_rascunhos.pop()
            self.titulo = estado_para_reverter.titulo
            self.descricao = estado_para_reverter.descricao
            self.prioridade = estado_para_reverter.prioridade
            self.status = estado_para_reverter.status
            self.ultimo_editor = estado_para_reverter.ultimo_editor
            if (self.versao > 1):
                self.versao -= 1
            self._registrar_alteracao("Alteração desfeita")
            return True
        return False

    def __str__(self):
        return (f"ID: {self.idChamado} | Título: {self.titulo} | "
                f"Data: {self.dataAbertura.strftime('%d/%m/%Y %H:%M')} | "
                f"Prioridade: {self.prioridade} | Status: {self.status}")