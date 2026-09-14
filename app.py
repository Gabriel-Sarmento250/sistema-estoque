from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Usuario, Categoria, Produto, Movimentacao
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'troque-essa-chave'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Categorias que vêm por padrão
CATEGORIAS_PADRAO = [
    'Eletrodomésticos',
    'Eletrônicos',
    'Alimentos',
    'Bebidas',
    'Móveis',
    'Roupas',
    'Calçados',
    'Higiene e Limpeza',
    'Papelaria',
    'Ferramentas',
    'Brinquedos',
    'Automotivo',
    'Pet Shop',
    'Outros',
]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('index'))
        flash('Email ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# ---------- CATEGORIAS ----------
@app.route('/categorias')
@login_required
def categorias():
    lista = Categoria.query.order_by(Categoria.nome).all()
    return render_template('categorias.html', categorias=lista)

@app.route('/categorias/nova', methods=['POST'])
@login_required
def nova_categoria():
    nome = request.form['nome']
    if nome.strip():
        db.session.add(Categoria(nome=nome))
        db.session.commit()
        flash('Categoria cadastrada!')
    return redirect(url_for('categorias'))

@app.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    cat = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        cat.nome = request.form['nome']
        db.session.commit()
        flash('Categoria atualizada!')
        return redirect(url_for('categorias'))
    return render_template('editar_categoria.html', categoria=cat)

@app.route('/categorias/excluir/<int:id>')
@login_required
def excluir_categoria(id):
    cat = Categoria.query.get_or_404(id)

    # Verifica se tem produtos vinculados
    if cat.produtos:
        flash(f'Não é possível excluir "{cat.nome}": há {len(cat.produtos)} produto(s) vinculado(s).')
        return redirect(url_for('categorias'))

    db.session.delete(cat)
    db.session.commit()
    flash(f'Categoria "{cat.nome}" excluída!')
    return redirect(url_for('categorias'))

# ---------- PRODUTOS ----------
@app.route('/produtos')
@login_required
def produtos():
    lista = Produto.query.order_by(Produto.nome).all()
    cats = Categoria.query.order_by(Categoria.nome).all()
    return render_template('produtos.html', produtos=lista, categorias=cats)

@app.route('/produtos/novo', methods=['POST'])
@login_required
def novo_produto():
    nome = request.form['nome']
    categoria_id = request.form.get('categoria_id') or None
    quantidade = int(request.form.get('quantidade') or 0)
    preco = float(request.form.get('preco') or 0)
    estoque_minimo = int(request.form.get('estoque_minimo') or 0)

    if nome.strip():
        p = Produto(
            nome=nome,
            categoria_id=categoria_id,
            quantidade=quantidade,
            preco=preco,
            estoque_minimo=estoque_minimo
        )
        db.session.add(p)
        db.session.commit()
        flash('Produto cadastrado!')
    return redirect(url_for('produtos'))

@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    p = Produto.query.get_or_404(id)
    cats = Categoria.query.order_by(Categoria.nome).all()

    if request.method == 'POST':
        p.nome = request.form['nome']
        p.categoria_id = request.form.get('categoria_id') or None
        p.quantidade = int(request.form.get('quantidade') or 0)
        p.preco = float(request.form.get('preco') or 0)
        p.estoque_minimo = int(request.form.get('estoque_minimo') or 0)
        db.session.commit()
        flash('Produto atualizado!')
        return redirect(url_for('produtos'))

    return render_template('editar_produto.html', produto=p, categorias=cats)

@app.route('/produtos/excluir/<int:id>')
@login_required
def excluir_produto(id):
    p = Produto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Produto excluído!')
    return redirect(url_for('produtos'))

# ---------- ENTRADA ----------
@app.route('/entrada', methods=['GET', 'POST'])
@login_required
def entrada():
    produtos_lista = Produto.query.order_by(Produto.nome).all()
    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])
        quantidade = int(request.form['quantidade'])
        motivo = request.form.get('motivo', 'Compra')
        fornecedor = request.form.get('fornecedor', '')
        documento = request.form.get('documento', '')
        custo = float(request.form.get('custo_unitario') or 0)

        if quantidade > 0:
            p = Produto.query.get_or_404(produto_id)
            p.quantidade += quantidade

            if custo > 0:
                p.preco = custo

            mov = Movimentacao(
                produto_id=produto_id,
                tipo='entrada',
                quantidade=quantidade,
                motivo=motivo,
                fornecedor=fornecedor,
                documento=documento,
                custo_unitario=custo
            )
            db.session.add(mov)
            db.session.commit()
            flash(f'Entrada de {quantidade} un. de "{p.nome}" registrada!')
        return redirect(url_for('entrada'))

    movs = Movimentacao.query.filter_by(tipo='entrada').order_by(Movimentacao.data.desc()).limit(20).all()
    return render_template('entrada.html', produtos=produtos_lista, movimentacoes=movs)

# ---------- SAÍDA ----------
@app.route('/saida', methods=['GET', 'POST'])
@login_required
def saida():
    produtos_lista = Produto.query.order_by(Produto.nome).all()
    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])
        quantidade = int(request.form['quantidade'])
        motivo = request.form.get('motivo', 'Venda')
        destino = request.form.get('destino', '')

        p = Produto.query.get_or_404(produto_id)
        if quantidade > 0 and quantidade <= p.quantidade:
            p.quantidade -= quantidade

            mov = Movimentacao(
                produto_id=produto_id,
                tipo='saida',
                quantidade=quantidade,
                motivo=motivo,
                destino=destino
            )
            db.session.add(mov)
            db.session.commit()
            flash(f'Saída de {quantidade} un. de "{p.nome}" registrada!')

            if p.quantidade <= p.estoque_minimo:
                flash(f'⚠️ Atenção: "{p.nome}" está com estoque baixo ({p.quantidade} un.)!')
        else:
            flash('Quantidade inválida ou estoque insuficiente!')
        return redirect(url_for('saida'))

    movs = Movimentacao.query.filter_by(tipo='saida').order_by(Movimentacao.data.desc()).limit(20).all()
    return render_template('saida.html', produtos=produtos_lista, movimentacoes=movs)

# ---------- EXCLUIR MOVIMENTAÇÃO (com estorno) ----------
@app.route('/movimentacao/excluir/<int:id>')
@login_required
def excluir_movimentacao(id):
    mov = Movimentacao.query.get_or_404(id)
    p = Produto.query.get_or_404(mov.produto_id)

    # Estorno: entrada subtrai do estoque, saída soma de volta
    if mov.tipo == 'entrada':
        if p.quantidade < mov.quantidade:
            flash(f'Não é possível excluir: estoque atual ({p.quantidade}) é menor que a entrada ({mov.quantidade}).')
            return redirect(request.referrer or url_for('entrada'))
        p.quantidade -= mov.quantidade
    else:  # saida
        p.quantidade += mov.quantidade

    db.session.delete(mov)
    db.session.commit()
    flash(f'Movimentação de {mov.tipo} excluída e estoque estornado!')
    return redirect(request.referrer or url_for('entrada'))

# ---------- CONSULTA ----------
@app.route('/consulta')
@login_required
def consulta():
    busca = request.args.get('busca', '').strip()
    cat_id = request.args.get('categoria_id', '')

    query = Produto.query
    if busca:
        query = query.filter(Produto.nome.ilike(f'%{busca}%'))
    if cat_id:
        query = query.filter(Produto.categoria_id == int(cat_id))

    lista = query.order_by(Produto.nome).all()
    cats = Categoria.query.order_by(Categoria.nome).all()
    return render_template('consulta.html', produtos=lista, categorias=cats, busca=busca, cat_id=cat_id)

# ---------- INICIALIZA BANCO + ADMIN ----------
@app.cli.command('init-db')
def init_db():
    db.create_all()

    # Cria usuário admin
    if not Usuario.query.filter_by(email='admin@admin.com').first():
        admin = Usuario(
            nome='Admin',
            email='admin@admin.com',
            senha=generate_password_hash('123'),
            tipo='admin'
        )
        db.session.add(admin)
        print('Usuário admin criado.')

    # Cria categorias padrão
    criadas = 0
    for nome_cat in CATEGORIAS_PADRAO:
        if not Categoria.query.filter_by(nome=nome_cat).first():
            db.session.add(Categoria(nome=nome_cat))
            criadas += 1

    db.session.commit()
    print(f'Banco criado! Login: admin@admin.com / 123')
    print(f'{criadas} categorias padrão adicionadas.')