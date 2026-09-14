from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), default='operador')

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    quantidade = db.Column(db.Integer, default=0)
    preco = db.Column(db.Float, default=0.0)
    estoque_minimo = db.Column(db.Integer, default=0)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    atualizado_em = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    categoria = db.relationship('Categoria', backref='produtos')

class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    tipo = db.Column(db.String(10))  # 'entrada' ou 'saida'
    quantidade = db.Column(db.Integer)
    motivo = db.Column(db.String(50))
    fornecedor = db.Column(db.String(100))
    destino = db.Column(db.String(100))
    documento = db.Column(db.String(50))
    custo_unitario = db.Column(db.Float, default=0.0)
    data = db.Column(db.DateTime, server_default=db.func.now())

    produto = db.relationship('Produto')