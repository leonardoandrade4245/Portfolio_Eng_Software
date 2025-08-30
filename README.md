# Portfólio Engenharia de Software

  O Olivia Modas é um sistema web para gerenciamento de estoque e controle de produtos desenvolvido com Python (Flask) e MySQL.
Ele oferece uma interface intuitiva para administradores e colaboradores, com diferentes níveis de acesso e gráficos dinâmicos para monitorar o estoque

Funcionalidades

    * Gerenciamento de Usuários
      - Login seguro com níveis de acesso (Administrador e Colaborador).
      - Cadastro de novos usuários (apenas ADM).
      - Edição e visualização de perfil.
      - Logout seguro.

Controle de Estoque
  * Adicionar, editar e excluir produtos.
  * Campos: nome, quantidade, tamanho, preço, categoria, gênero.
  * Pesquisa rápida de produtos por nome.
  * Listagem detalhada do estoque.

Dashboard e Relatórios
  * Gráfico dinâmico mostrando produtos por categoria.
  * Estoques baixos (≤ 10 itens) destacados em vermelho.
  * Informações em tempo real sobre o estoque.

instalação e Execução
  1. Clonar Repositório
     - git clone https://github.com/seu-usuario/OliviaModas.git
cd OliviaModas
  2. Criai Ambiente Virtual
   - python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
  3. Instalar Dependências
    - pip install -r requirements.txt
  4. Executar o Sistema
    -  python app.py

Autror,
Leonardo Andrade Almeida
