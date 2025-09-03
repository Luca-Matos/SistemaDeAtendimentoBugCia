Central de Suporte Bug & Cia

Um sistema de suporte com interface gráfica moderna e responsiva para gerenciamento de chamados de suporte técnico, desenvolvido com Python e a biblioteca CustomTkinter.

Sobre o Projeto: 

Este projeto implementa uma solução de suporte que permite a interação de dois tipos de usuários: Clientes e Atendentes. Clientes podem abrir e visualizar seus chamados, enquanto os Atendentes possuem uma visão completa para gerenciar, priorizar, editar e resolver os chamados de toda a fila.
A aplicação utiliza uma estrutura de dados de fila (deque) para gerenciar os chamados, permitindo uma manipulação eficiente das solicitações de suporte.

Funcionalidades Principais:

Sistema de Login: Distinção de perfis entre Cliente e Atendente.

Painel do Cliente: Permite ao cliente criar novos chamados e visualizar o status dos chamados já abertos.

Painel do Atendente:Visualização da fila de chamados em um carrossel.

Ordenação da lista de chamados por ordem de chegada ou por prioridade.

Edição completa dos detalhes de um chamado (título, descrição, prioridade).

Possibilidade de reordenar manualmente os chamados na fila (arrastar e soltar simulado por cliques).

Resolução e remoção de chamados.

Interface Gráfica Moderna: Desenvolvida com CustomTkinter para um visual agradável e profissional, com tema escuro.

Tecnologias Utilizadas
Linguagem: Python 3
Interface Gráfica: Custom Tkinter

Instruções de Compilação e Preparação: Como o projeto é feito em Python, não há uma etapa de "compilação" tradicional. O processo consiste em preparar o ambiente e instalar as bibliotecas necessárias (dependências).

Pré-requisitos
Python 3.8 ou superior instalado.

Passos para a Instalação :
Clone o repositório:
git clone 
cd seu-repositorio

Crie e ative um ambiente virtual (Recomendado): (Isso isola as dependências do seu projeto e evita conflitos com outros projetos Python.)
No Windows:
python -m venv venv
.\venv\Scripts\activate

Instale a dependência principal: O projeto utiliza a biblioteca CustomTkinter. Use o seguinte comando para instalá-la:

pip install customtkinter

Instruções de Execução: 
Com o ambiente virtual ativado e a dependência instalada, execute o arquivo principal para iniciar a aplicação:
python main.py


A janela do sistema será aberta, começando pela tela de login.
Exemplos de Entrada e Saída:

A seguir, exemplos de como interagir com o sistema (entrada) e o que esperar como resultado (saída).
1. Login no Sistema
Entrada:
Execute o programa.
Na tela de login, digite atendente no campo "Usuário".
Digite atendente no campo "Senha".
Clique no botão "Login".
Saída: A tela de login desaparece e o "Painel do Atendente" é exibido, mostrando a fila de chamados e as ferramentas de gerenciamento.
2. Criando um Novo Chamado (Visão do Cliente)
Entrada:
Faça login como cliente (usuário: cliente, senha: cliente).
No Painel do Cliente, clique no botão "Novo Chamado".
Na janela que se abre, preencha o "Título do Chamado" (ex: Email não envia) e a "Descrição Detalhada" (ex: A caixa de saída está cheia e não consigo enviar novas mensagens.).
Clique em "Salvar Chamado".
Saída: A janela de novo chamado se fecha e a lista "Meus Chamados" no painel do cliente é atualizada, exibindo o chamado recém-criado.
3. Alterando a Prioridade de um Chamado (Visão do Atendente)
Entrada:
Faça login como atendente.
Use os botões < Anterior e Próximo > para navegar até o chamado desejado no carrossel.
Clique em "Detalhes/Editar".
Na janela de detalhes, altere a "Prioridade" de 1 para 5.
Clique em "Salvar Alterações".

Saída: A janela de detalhes se fecha. A lista de chamados é atualizada. Se você ordenar a fila por "Prioridade", o chamado alterado aparecerá no topo da lista.
Estrutura dos Arquivos

├── main.py             # Arquivo principal, contém a lógica da interface e execução
└── models.py           # Define as classes de dados (Cliente, Atendente, Chamado)


Referências e Inspirações
Este documento foi elaborado a partir da análise e inspiração de diversos READMEs de alta qualidade da comunidade. Agradecemos aos seguintes projetos pelos excelentes exemplos que nos guiaram na criação de uma documentação clara e completa:
Abblix OIDC Server
README Template by dbader
Readme Template by iuricode
Template para Readme.md (Gist)
Dashboard Suporte
Awesome README Template
README Template by Microverse

