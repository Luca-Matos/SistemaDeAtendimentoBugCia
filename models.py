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
# REMOVIDO: from fpdf import FPDF (Movido para onde é usado, se necessário)
# A importação do FPDF só é necessária se 'gerar_relatorio_pdf' for realmente usada.
# Se não for, pode ser removida para simplificar. Se for, precisa estar aqui
# ou dentro da função que a usa (melhor prática). Vamos deixar aqui por enquanto.
try:
    from fpdf import FPDF
except ImportError:
    print("AVISO: Biblioteca FPDF não encontrada. Geração de PDF desabilitada.")
    print("Execute: pip install fpdf")
    FPDF = None # Define como None para verificações posteriores


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

        # Histórico para o relatório PDF (data e o que foi alterado)
        self._historico_alteracoes = []

        # Inicializa uma deque para armazenar o histórico de estados (pilha para desfazer).
        self._historico_rascunhos = deque(maxlen=20) # Limita o histórico a 20 passos

        # Salva o estado inicial como uma CÓPIA PROFUNDA para segurança.
        self.salvar_rascunho()

        # Registra a criação como a primeira alteração no histórico de LOG
        self._registrar_alteracao("Chamado criado")

    def _registrar_alteracao(self, detalhe: str):
        """Método interno para registrar uma alteração com timestamp no log."""
        data = datetime.now()
        self._historico_alteracoes.append({
            'data': data,
            'detalhes': detalhe
        })
        print(f"LOG Chamado ID {self.idChamado}: {detalhe} em {data.strftime('%Y-%m-%d %H:%M:%S')}") # Debug no terminal

    def resolver(self):
        """Altera o status do chamado para 'Resolvido'."""
        if self.status != "Resolvido":
            # Salva rascunho ANTES de mudar o status
            self.salvar_rascunho()
            self.status = "Resolvido"
            self._registrar_alteracao(f"Status alterado para '{self.status}'")

    def atualizar(self, novo_titulo, nova_descricao, nova_prioridade):
        """
        Atualiza os dados do chamado, salva o estado anterior no histórico de rascunhos,
        e registra as alterações detalhadas no log.
        """
        # 1. Salva o estado ATUAL (antes da mudança) no histórico de rascunhos (pilha).
        self.salvar_rascunho()

        alteracoes_detectadas = [] # Lista para guardar as mudanças desta atualização

        # --- RASTREAMENTO DE ALTERAÇÕES DETALHADAS ---
        # Compara cada campo com o novo valor e registra a mudança se houver.

        # Título
        if self.titulo != novo_titulo:
            alteracoes_detectadas.append(f"Título alterado de '{self.titulo}' para '{novo_titulo}'")
            self.titulo = novo_titulo # Aplica a mudança

        # Descrição
        if self.descricao != nova_descricao:
            preview_antigo = self.descricao[:50].strip().replace('\n', ' ') + ('...' if len(self.descricao) > 50 else '')
            preview_novo = nova_descricao[:50].strip().replace('\n', ' ') + ('...' if len(nova_descricao) > 50 else '')
            alteracoes_detectadas.append(f"Descrição alterada de '{preview_antigo}' para '{preview_novo}'")
            self.descricao = nova_descricao # Aplica a mudança

        # Prioridade
        try:
            nova_prioridade_int = int(nova_prioridade)
            if self.prioridade != nova_prioridade_int:
                alteracoes_detectadas.append(f"Prioridade alterada de '{self.prioridade}' para '{nova_prioridade_int}'")
                self.prioridade = nova_prioridade_int # Aplica a mudança
        except (ValueError, TypeError):
            print(f"AVISO: valor de prioridade inválido ('{nova_prioridade}') recebido para Chamado ID {self.idChamado}. Mantendo valor anterior '{self.prioridade}'.")
            # Não adiciona ao log se a prioridade não mudou ou foi inválida

        # Se alguma alteração foi detectada, registra no log _historico_alteracoes
        if alteracoes_detectadas:
            # Junta todas as alterações detectadas em uma única string para o log
            log_detalhe = ", ".join(alteracoes_detectadas)
            self._registrar_alteracao(log_detalhe)
        else:
            print(f"INFO: Tentativa de atualização no Chamado ID {self.idChamado}, mas nenhum dado foi alterado.")

    def gerar_relatorio_pdf(self, nome_arquivo="relatorio_chamado.pdf"):
        """Gera um relatório em PDF com o histórico de alterações."""

        if FPDF is None:
            raise ImportError("Biblioteca FPDF não encontrada. Não é possível gerar PDF.")

        # Configuração inicial do PDF
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font('Arial', '', 10) # Define fonte padrão cedo

        # Título do Relatório
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Relatório de Alterações do Chamado', 0, 1, 'C')
        pdf.ln(5) # Espaço após título

        # Informações do Chamado (com tratamento de erro para atributos)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 7, f'ID do Chamado: {getattr(self, "idChamado", "N/A")}', 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f'Título: {getattr(self, "titulo", "N/A")}', 0, 1, 'L')

        req_nome = "N/A"
        if hasattr(self, 'requisitante'):
            req_nome = getattr(self.requisitante, 'nomeCliente', str(self.requisitante))
        pdf.cell(0, 6, f'Requisitante: {req_nome}', 0, 1, 'L')
        pdf.cell(0, 6, f'Status Atual: {getattr(self, "status", "N/A")}', 0, 1, 'L')
        try:
            data_abertura_str = self.dataAbertura.strftime("%d/%m/%Y %H:%M:%S")
        except:
            data_abertura_str = "Data inválida"
        pdf.cell(0, 6, f'Data Abertura: {data_abertura_str}', 0, 1, 'L')
        pdf.ln(5) # Espaço antes da tabela

        # Tabela de Histórico
        pdf.set_font('Arial', 'B', 10)
        pdf.set_fill_color(220, 220, 220) # Cinza claro
        col_width_data = 40
        col_width_detalhes = pdf.w - pdf.l_margin - pdf.r_margin - col_width_data # Largura restante
        line_height = 7

        pdf.cell(col_width_data, line_height, 'Data e Hora', border=1, ln=0, align='C', fill=True)
        pdf.cell(col_width_detalhes, line_height, 'Detalhes da Alteração', border=1, ln=1, align='C', fill=True)

        pdf.set_font('Arial', '', 9) # Fonte menor para detalhes
        pdf.set_fill_color(255, 255, 255) # Fundo branco para linhas
        fill = False # Alternar cor de linha (opcional)

        # Usamos reversed() para mostrar o mais recente primeiro (opcional)
        if hasattr(self, '_historico_alteracoes') and self._historico_alteracoes:
            for registro in reversed(self._historico_alteracoes):
                try:
                    data_formatada = registro.get('data', datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
                except:
                    data_formatada = "Data inválida"
                detalhes = registro.get('detalhes', 'N/A')

                # MultiCell para detalhes que podem quebrar linha
                y_before = pdf.get_y()
                pdf.set_x(pdf.l_margin + col_width_data) # Posição X da segunda coluna
                pdf.multi_cell(col_width_detalhes, line_height / 1.5, detalhes, border='LR', align='L', fill=fill) # Borda só Left/Right
                y_after = pdf.get_y()
                line_height_used = y_after - y_before

                # Desenha a célula da data com a altura correta
                pdf.set_xy(pdf.l_margin, y_before)
                pdf.cell(col_width_data, line_height_used, data_formatada, border='LR', ln=0, align='L', fill=fill)

                # Desenha a borda inferior para ambas as células
                pdf.set_y(y_after) # Garante que estamos na posição correta Y
                pdf.set_x(pdf.l_margin)
                pdf.cell(col_width_data + col_width_detalhes, 0, '', border='T', ln=1) # Borda Top que fecha a linha

                fill = not fill # Alterna cor (se quiser)
        else:
            pdf.cell(col_width_data + col_width_detalhes, line_height, 'Nenhum histórico de alteração registrado.', border=1, ln=1, align='C')

        # Salva o PDF
        try:
            pdf.output(nome_arquivo, 'F')
        except Exception as e:
            print(f"ERRO ao salvar o PDF '{nome_arquivo}': {e}")
            raise IOError(f"Não foi possível salvar o PDF em '{nome_arquivo}'. Verifique as permissões.") from e


    def salvar_rascunho(self):
        """Cria uma cópia do estado atual e a adiciona à pilha de histórico (_historico_rascunhos)."""
        try:
            # Usamos copy.deepcopy() para garantir que listas internas (como _historico_alteracoes)
            # não sejam compartilhadas entre os rascunhos, o que poderia causar erros no 'desfazer'.
            rascunho = copy.deepcopy(self)
            # Remove o rascunho mais antigo se a pilha estiver cheia (maxlen)
            self._historico_rascunhos.append(rascunho)
            print(f"INFO: Rascunho salvo para Chamado ID {self.idChamado}. Total rascunhos: {len(self._historico_rascunhos)}") # Debug
        except Exception as e:
            print(f"ERRO ao salvar rascunho para Chamado ID {self.idChamado}: {e}")

    def desfazer_alteracao(self):
        """
        Restaura o chamado para o estado anterior da pilha de rascunhos.
        Retorna True se bem-sucedido, False caso contrário.
        """
        # Só pode desfazer se houver pelo menos 2 estados: o atual e um anterior.
        if hasattr(self, '_historico_rascunhos') and len(self._historico_rascunhos) > 1:
            try:
                # 1. Remove e descarta o estado MAIS RECENTE (que é uma cópia do estado ATUAL antes do 'desfazer')
                self._historico_rascunhos.pop()
                # 2. Pega o estado ANTERIOR que agora está no topo da pilha
                estado_para_reverter = self._historico_rascunhos[-1] # Pega o último sem remover

                # 3. Restaura os atributos do objeto atual com os valores do estado anterior.
                #    Usamos getattr para segurança caso algum atributo falte no rascunho antigo.
                self.titulo = getattr(estado_para_reverter, 'titulo', self.titulo)
                self.descricao = getattr(estado_para_reverter, 'descricao', self.descricao)
                self.prioridade = getattr(estado_para_reverter, 'prioridade', self.prioridade)
                self.status = getattr(estado_para_reverter, 'status', self.status)
                # Outros atributos como 'requisitante' e 'dataAbertura' geralmente não mudam,
                # então não precisamos restaurá-los, a menos que sua lógica permita.

                # O _historico_alteracoes NÃO é desfeito, ele é um log permanente.
                # Registramos a ação de desfazer no log:
                self._registrar_alteracao("Alteração desfeita (estado anterior restaurado)")

                print(f"INFO: Desfazer aplicado para Chamado ID {self.idChamado}. Rascunhos restantes: {len(self._historico_rascunhos)}") # Debug
                return True  # Sucesso
            except IndexError:
                print(f"ERRO: Tentativa de acessar rascunho inválido ao desfazer Chamado ID {self.idChamado}.")
                # Se deu erro, tentamos adicionar o estado atual de volta para consistência
                self.salvar_rascunho()
                return False # Falha
            except Exception as e:
                 print(f"ERRO inesperado ao desfazer Chamado ID {self.idChamado}: {e}")
                 return False # Falha
        else:
            print(f"AVISO: Não há mais estados para desfazer no Chamado ID {self.idChamado}.")
            return False 



    def __str__(self):
        """Retorna uma representação em string legível do chamado."""
        try:
            data_str = self.dataAbertura.strftime('%d/%m/%Y %H:%M')
        except:
            data_str = "Data inválida"
        return (f"ID: {getattr(self, 'idChamado', 'N/A')} | Título: {getattr(self, 'titulo', 'N/A')} | "
                f"Data: {data_str} | "
                f"Prioridade: {getattr(self, 'prioridade', 'N/A')} | Status: {getattr(self, 'status', 'N/A')}")

# --- FIM DO ARQUIVO models.py ---
