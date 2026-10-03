# 📦 Sistema de Estoque

Sistema web de controle de estoque desenvolvido em **Flask (Python)** como trabalho de faculdade.

## ✨ Funcionalidades

- Autenticação de usuário (login)
- Cadastro de produtos
- Listagem de itens em estoque
- Entrada e baixa de produtos
- Edição e remoção de produtos
- Persistência em banco de dados

## 🛠️ Tecnologias

- **Python** — linguagem principal
- **Flask** — framework web
- **SQLAlchemy** — ORM para banco de dados
- **SQLite** — banco de dados
- **HTML + CSS** — interface (templates Jinja2)

## 📁 Estrutura do projeto

\`\`\`
sistema-estoque/
├── app.py              # Aplicação principal (rotas Flask)
├── models.py           # Modelos do banco de dados
├── templates/          # Templates HTML
└── .gitignore
\`\`\`

## ⚙️ Como rodar o projeto

### Pré-requisitos
- Python 3.8+ instalado

### Passo a passo

\`\`\`bash
# Clone o repositório
git clone https://github.com/Gabriel-Sarmento250/sistema-estoque.git

# Entre na pasta
cd sistema-estoque

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode a aplicação
python app.py
\`\`\`

Acesse em: `http://localhost:5000`

## 🔑 Acesso para teste

Para testar o sistema, utilize as credenciais abaixo:

| Campo | Valor |
|-------|-------|
| **E-mail** | `admin@admin.com` |
| **Senha** | `123` |

> ⚠️ Credenciais apenas para fins de demonstração/teste.

## 👤 Autor

**Gabriel Sarmento Visconti**
- 🎓 Estudante de Análise e Desenvolvimento de Sistemas
- 💼 [LinkedIn](https://www.linkedin.com/in/gabriel-sarmento-visconti)
- 📧 gabrielsarmentovisconti@gmail.com
