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
import copy  # Importa o módulo 'copy' para criar cópias de objetos.
from fpdf import FPDF  # NOVO: Importa a biblioteca de geração de PDF


# --- CLASSES DE ENTIDADE ---

class Cliente:
    """Representa um cliente no sistema."""

    def __init__(self, idCliente: int, nomeCliente: str, email: str):
        """Inicializa um objeto Cliente."""
        self.idCliente = idCliente
        self.nomeCliente = nomeCliente
        self.email = email

    def __str__(self):
        """Retorna uma representação em string do cliente."""
        return f"Cliente: {self.nomeCliente}"


class Atendente:
    """Representa um atendente no sistema."""

    def __init__(self, idAtendente: int, nomeAtendente: str):
        """Inicializa um objeto Atendente."""
        self.idAtendente = idAtendente
        self.nomeAtendente = nomeAtendente

    def __str__(self):
        """Retorna uma representação em string do atendente."""
        return f"Atendente: {self.nomeAtendente}"


# --- CLASSE PRINCIPAL DE NEGÓCIO ---

class Chamado:
    """
    Representa um chamado (ticket) de suporte no sistema.
    Gerencia seu próprio histórico de alterações para a funcionalidade de 'desfazer'
    e para a geração de relatórios.
    """
    # Variável de classe para garantir que cada chamado tenha um ID único.
    _id_counter = 1

    def __init__(self, cliente_ou_atendente, titulo: str, descricao: str):
        """Inicializa um novo objeto Chamado."""
        # Atribui o ID único e incrementa o contador para o próximo chamado.
        self.idChamado = Chamado._id_counter
        Chamado._id_counter += 1

        # Atributos básicos do chamado.
        self.requisitante = cliente_ou_atendente
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = 1  # Prioridade padrão.
        self.status = "Aberto"
        self.dataAbertura = datetime.now()

        # NOVO: Histórico para o relatório PDF (data e o que foi alterado)
        self._historico_alteracoes = []

        # Inicializa uma deque (fila de duas pontas) para armazenar o histórico de estados.
        self._historico_rascunhos = deque(maxlen=20)

        # Salva o estado inicial como uma CÓPIA.
        self.salvar_rascunho()

        # NOVO: Registra a criação como a primeira alteração
        self._registrar_alteracao("Chamado criado")

    def _registrar_alteracao(self, detalhe: str):
        """Método interno para registrar uma alteração com timestamp."""
        data = datetime.now()
        self._historico_alteracoes.append({
            'data': data,
            'detalhes': detalhe
        })

    def resolver(self):
        """Altera o status do chamado para 'Resolvido'."""
        if self.status != "Resolvido":
            self.status = "Resolvido"
            # NOVO: Registra a alteração de status
            self._registrar_alteracao(f"Status alterado para '{self.status}'")

    def atualizar(self, novo_titulo, nova_descricao, nova_prioridade):
        """
        Atualiza os dados do chamado e salva o estado anterior no histórico.
        Registra as alterações detalhadas para o relatório PDF.
        """
        # 1. Salva o estado ATUAL (antes da mudança) no histórico.
        self.salvar_rascunho()

        alteracoes_detectadas = []

        # --- RASTREAMENTO DE ALTERAÇÕES DETALHADAS ---

        # Título
        if self.titulo != novo_titulo:
            alteracoes_detectadas.append(f"Título alterado para: '{novo_titulo}'")

        # Descrição (AGORA MOSTRA O NOVO CONTEÚDO)
        if self.descricao != nova_descricao:
            # Limita a nova descrição para 100 caracteres no registro do histórico (para o PDF)
            novo_texto_preview = nova_descricao[:100].strip().replace('\n', ' ') + (
                '...' if len(nova_descricao) > 100 else '')

            # Adiciona a nova descrição formatada ao log
            alteracoes_detectadas.append(f"Descrição alterada para: '{novo_texto_preview}'")

        # Prioridade
        try:
            nova_prioridade_int = int(nova_prioridade)
            if self.prioridade != nova_prioridade_int:
                alteracoes_detectadas.append(f"Prioridade alterada de '{self.prioridade}' para '{nova_prioridade_int}'")
            self.prioridade = nova_prioridade_int
        except (ValueError, TypeError):
            print(f"Erro: valor de prioridade inválido ('{nova_prioridade}'). Mantendo valor anterior.")

        if alteracoes_detectadas:
            # 2. REGISTRA NO LOG
            self._registrar_alteracao(", ".join(alteracoes_detectadas))

        # 3. APLICA AS NOVAS INFORMAÇÕES
        self.titulo = novo_titulo
        self.descricao = nova_descricao

    # =========================================================================
    # FUNÇÃO DE GERAÇÃO DE RELATÓRIO PDF (Mantida da implementação anterior)
    # =========================================================================
    def gerar_relatorio_pdf(self, nome_arquivo="relatorio_chamado.pdf"):
        """Gera um relatório em PDF com o histórico de alterações."""

        # Configuração inicial do PDF
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Título do Relatório
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Relatório de Alterações do Chamado', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 5, f'ID: {self.idChamado} | Título: {self.titulo}', 0, 1, 'L')
        # Determina se é Cliente ou outro requisitante para impressão
        req_nome = self.requisitante.nomeCliente if hasattr(self.requisitante, 'nomeCliente') else str(
            self.requisitante)
        pdf.cell(0, 5, f'Requisitante: {req_nome} | Status Atual: {self.status}', 0, 1, 'L')
        pdf.cell(0, 5, f'Data Abertura: {self.dataAbertura.strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'L')
        pdf.cell(0, 5, '-' * 50, 0, 1, 'C')

        # Definição das colunas e altura da linha
        COL_DATA = 40  # Largura da coluna Data/Hora
        COL_DETALHES = 150  # Largura da coluna Detalhes
        LINE_HEIGHT = 7

        # Cabeçalho da Tabela
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font('Arial', 'B', 10)

        pdf.cell(COL_DATA, LINE_HEIGHT, 'Data e Hora', 1, 0, 'C', 1)
        pdf.cell(COL_DETALHES, LINE_HEIGHT, 'Detalhes da Alteração', 1, 1, 'C', 1)

        # Inserção dos Dados
        pdf.set_font('Arial', '', 10)

        for registro in reversed(self._historico_alteracoes):
            data_formatada = registro['data'].strftime("%d/%m/%Y %H:%M:%S")
            detalhes = registro['detalhes']

            # 1. Salva a posição inicial Y para o alinhamento
            y_inicial = pdf.get_y()

            # 2. Escreve os detalhes da alteração (MultiCell para quebra de linha)
            # Avança o X para a coluna de detalhes
            pdf.set_x(pdf.get_x() + COL_DATA)
            pdf.multi_cell(COL_DETALHES, 6, detalhes, 1, 'L', 0)

            # 3. Determina a altura que a MultiCell usou e calcula o Y final
            y_final = pdf.get_y()
            altura_usada = y_final - y_inicial

            # 4. Redesenha a célula de Data/Hora com a altura correta (para as bordas)
            # Volta para a posição X da primeira coluna e Y inicial
            pdf.set_xy(pdf.l_margin, y_inicial)
            pdf.cell(COL_DATA, altura_usada, data_formatada, 1, 0, 'L', 0)

            # 5. Avança o cursor para a próxima linha
            pdf.set_xy(pdf.l_margin, y_final)

            # Saída do PDF
        pdf.output(nome_arquivo, 'F')

    def salvar_rascunho(self):
        """
        Cria uma cópia superficial do estado atual do chamado e a adiciona à
        pilha de histórico.
        """
        # `copy.copy()` cria um novo objeto Chamado e copia os valores dos atributos.
        # Isso é fundamental para evitar o problema de salvar apenas uma referência
        # ao objeto, o que invalidaria o histórico.
        rascunho = copy.copy(self)
        self._historico_rascunhos.append(rascunho)

    def desfazer_alteracao(self):
        """
        Restaura o chamado para o estado anterior, se houver um no histórico.
        Retorna True se a operação foi bem-sucedida, False caso contrário.
        """
        # Só é possível desfazer se houver mais de um estado (o atual + pelo menos um anterior).
        if len(self._historico_rascunhos) > 1:
            # 1. Remove o estado mais recente (o rascunho ANTERIOR à última mudança)
            # e armazena o rascunho que foi removido.
            estado_para_reverter = self._historico_rascunhos.pop()

            # Restaura os atributos do objeto atual com os valores do estado anterior.
            self.titulo = estado_para_reverter.titulo
            self.descricao = estado_para_reverter.descricao
            self.prioridade = estado_para_reverter.prioridade
            self.status = estado_para_reverter.status
            # Nota: O _historico_alteracoes não é desfeito

            return True  # Informa que a operação foi um sucesso.

        return False  # Informa que não há mais estados para desfazer.

    def __str__(self):
        """Retorna uma representação em string legível do chamado."""
        return (f"ID: {self.idChamado} | Título: {self.titulo} | "
                f"Data: {self.dataAbertura.strftime('%d/%m/%Y %H:%M')} | "
                f"Prioridade: {self.prioridade} | Status: {self.status}")