# Entrar com Login de ADM: Login: adm.Leonardo  -- Senha: leo1234
# Entrar com Login de Colaborador: Login: colab.Aline -- Senha: aline1234


from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_sqlalchemy import SQLAlchemy
import enum
import matplotlib.pyplot as plt
import io
import base64
from werkzeug.security import generate_password_hash, check_password_hash

# a linha abaixo é a minha variavel de aplicação
app = Flask(__name__)

app.secret_key = "admin" 

#a linha abaixo é a configuração do BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@127.0.0.1/OliviaModas'

# a linha abaixo instancia o BD
db = SQLAlchemy(app)

# Criando a Enumeração para a categoria
class CategoriaEnum(enum.Enum):
    ADM = "ADM"
    Colaborador = "Colaborador"

# Criando a Enumeração para a categoria dos produtos
class CategoriaProdutos(enum.Enum):
    Camisa = "Camisa"
    Short = "Short"
    Calça = "Calça"
    Tenis = "Tenis"
    Blusa = "Blusa"

class GeneroEnum(enum.Enum):
    M = "M"
    F = "F"

# a linha abaixo cria uma classe modelo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    categoria = db.Column(db.Enum(CategoriaEnum), nullable=False)
    login = db.Column(db.String(120), nullable=False)

    def __repr__(self): 
        return "<Name %r>"% self.nome

# a linha abaixo cria uma classe dos produtos
class Produtos(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tamanho = db.Column(db.String(10), nullable=False)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    categoria = db.Column(db.Enum(CategoriaProdutos), nullable=False)
    genero = db.Column(db.Enum(GeneroEnum), nullable=False)

    def __repr__(self): 
        return "<Produto %r>"% self.nome
    


# Redirecionamento automático para /inicio
@app.route('/')
def index():
    return redirect(url_for('mostrar'))  # Redireciona para a função "mostrar"

# Página de login
@app.route('/inicio')
def mostrar():
    return render_template("login.html")

@app.route('/principal', methods=["GET", "POST"])
def principal():
    query_estoque = request.args.get('query_estoque', '')
    query_alterar = request.args.get('query_alterar', '')

    if request.method == "POST":
        login = request.form.get("txtLogin")
        senha = request.form.get("txtSenha")

        if not login or not senha:
            return render_template("login.html", mensagem="Por favor, preencha o login e a senha.")

        usuario = Usuario.query.filter_by(login=login).first()  # Buscar pelo campo login
        print(f"Usuário encontrado: {login, senha}")  # Teste para ver se está encontrando o usuário correto

        if usuario:  # Verifica se encontrou o usuário
            if usuario.senha == senha:  # Comparação direta com a senha em texto simples
                session['usuario_id'] = usuario.id  
                print(f"Login bem-sucedido: {login}")
                return redirect(url_for('principal'))  # Redireciona se o login for correto
            else:
                return render_template("login.html", mensagem="Login ou senha incorretos.")  # Se a senha estiver errada
        else:
            return render_template("login.html", mensagem="Login ou senha incorretos.")  # Se não encontrar o usuário

    # Se for GET e o usuário NÃO estiver logado, redireciona para login
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar'))  
    
    # Inicializa a lista de produtos
    produtos_encontrados = Produtos.query.all()  # Carrega todos os produtos por padrão

    # Se houver pesquisa no estoque, filtrar apenas para essa seção
    if query_estoque:
        produtos_estoque = Produtos.query.filter(Produtos.nome.ilike(f"%{query_estoque}%")).all()
    else:
        produtos_estoque = Produtos.query.all()
  
    produtos = Produtos.query.all()
    print(f"Produtos encontrados: {produtos}")


    # Buscar todos os produtos primeiro
    todos_produtos = Produtos.query.all()

    produto_alterar = None
    if query_alterar:
        produto_alterar = Produtos.query.filter(Produtos.nome.ilike(f"%{query_alterar}%")).first()
        print(f"Produto encontrado para alteração: {produto_alterar}")  # Log para depuração

 
    # Buscar todos os produtos para exibição geral
    todos_produtos = Produtos.query.all()
 
    # Agrupar os produtos por categoria e somar as quantidades
    categorias = {}
    for produto in todos_produtos:  # <- Usamos 'todos_produtos' e não 'produtos'
        categoria = produto.categoria.value
        categorias[categoria] = categorias.get(categoria, 0) + produto.quantidade

    # Definir cores: vermelho se a quantidade for menor ou igual a 10, senão cor padrão
    cores = ['red' if quantidade <= 10 else '#FFEBCE' for quantidade in categorias.values()]

    # Criar o gráfico estilizado
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')  # Fundo branco, tamanho reduzido
    ax.bar(categorias.keys(), categorias.values(), color=cores, edgecolor="black", linewidth=1)
    
    # Personalizar texto e grid
    ax.set_xlabel("Itens", fontsize=10, color="black")
    ax.set_ylabel("Quantidade", fontsize=10, color="black")
    ax.grid(False)  # Isso desativa completamente a grade

    # **Remover possíveis marcações de eixos (ticks secundários que podem parecer pontilhados)**
    ax.tick_params(axis='both', which='both', length=0)  

    # Melhorar legibilidade do eixo X
    plt.xticks(rotation=20, fontsize=8, color="black")
    plt.yticks(fontsize=8, color="black")

    # Converter o gráfico para imagem base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight", transparent=True)
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return render_template("principal.html", img_base64=img_base64, produtos=produtos,todos_produtos=todos_produtos, produto_alterar=produto_alterar, produtos_encontrados=produtos_encontrados, produtos_estoque=produtos_estoque, CategoriaProdutos=CategoriaProdutos, GeneroEnum=GeneroEnum)

@app.route('/grafico_produtos_json')
def grafico_produtos_json():
    produtos = Produtos.query.all()
    categorias = {}
    for produto in produtos:
        categoria = produto.categoria.value
        categorias[categoria] = categorias.get(categoria, 0) + produto.quantidade

    return {"categorias": list(categorias.keys()), "quantidades": list(categorias.values())}

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)  # Remove o ID do usuário da sessão
    return redirect(url_for('mostrar'))

@app.route('/adicionar_produto', methods=["POST"])
def adicionar_produto():
    nome = request.form.get("nome")
    quantidade = request.form.get("quantidade")
    tamanho = request.form.get("tamanho")
    preco = request.form.get("preco")
    categoria = request.form.get("categoria")
    genero = request.form.get("genero")

    if not nome or not quantidade or not tamanho or not preco or not categoria or not genero:
        return redirect(url_for('principal', mensagem="Preencha todos os campos!"))

    try:
        novo_produto = Produtos(
            nome=nome,
            quantidade=int(quantidade),
            tamanho=tamanho,
            preco=float(preco),
            categoria=CategoriaProdutos[categoria], # Converte a string para enum
            genero=GeneroEnum[genero]
        )
        db.session.add(novo_produto)
        db.session.commit()
        return redirect(url_for('principal', mensagem="Produto adicionado com sucesso!"))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao adicionar produto: {e}"


@app.route('/alterar_produto', methods=["POST"])
def alterar_produto():
    id_produto = request.form.get("id")
    produto = Produtos.query.get(id_produto)

    if produto:
        produto.nome = request.form.get("nome")
        produto.quantidade = int(request.form.get("quantidade"))
        produto.tamanho = request.form.get("tamanho")
        produto.preco = float(request.form.get("preco"))
        produto.categoria = CategoriaProdutos[request.form.get("categoria")]

        db.session.commit()
        return redirect(url_for('principal', mensagem="Produto alterado com sucesso!"))
    else:
        return redirect(url_for('principal', mensagem="Produto não encontrado."))
    

@app.route('/deletar_produto', methods=["POST"])
def deletar_produto():
    id_produto = request.form.get("id")
    produto = Produtos.query.get(id_produto)

    if produto:
        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for('principal', mensagem="Produto deletado com sucesso!"))
    else:
        return redirect(url_for('principal', mensagem="Produto não encontrado."))

@app.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar'))  # Redireciona se o usuário não estiver logado

    usuario = Usuario.query.get(session['usuario_id'])  # Busca usuário logado no banco
    
    if not usuario:
        return redirect(url_for('logout'))  # Se o usuário não for encontrado, faz logout

    return render_template('perfil.html', usuario=usuario)

@app.route('/cadastrar_usuario', methods=["POST"])
def cadastrar_usuario():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar'))  # Se não estiver logado, volta para login

    usuario_logado = Usuario.query.get(session['usuario_id'])
    if usuario_logado.categoria.value != "ADM":
        return redirect(url_for('perfil'))  # Se não for ADM, não pode cadastrar

    nome = request.form.get("nome")
    email = request.form.get("email")
    telefone = request.form.get("telefone")
    senha = request.form.get("senha")
    categoria = request.form.get("categoria")

    if not nome or not email or not senha or not categoria:
        return redirect(url_for('perfil', mensagem="Preencha todos os campos!"))

    try:
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senha, 
            categoria=CategoriaEnum[categoria]
        )
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('perfil', mensagem="Usuário cadastrado com sucesso!"))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao cadastrar usuário: {e}"

if __name__ == '__main__':
    app.run(debug=True)

