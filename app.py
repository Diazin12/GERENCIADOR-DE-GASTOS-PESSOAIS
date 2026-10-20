from models import criar_tabelas, buscar_usuario_por_id, salvar_usuario, buscar_usuario_por_email
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.secret_key = 'paquito1@#'

criar_tabelas()

@login_manager.user_loader
def carregar_usuario(id_usuario):
    return buscar_usuario_por_id(id_usuario)

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get('nome', '').strip()
        if nome == '':
            flash("Digite um nome de usuario!")
            return render_template("cadastro.html")

        email = request.form.get('email', '').strip()
        if email == '':
            flash("Digite um email.")
            return render_template("cadastro.html")

        senha = request.form.get('senha', '')
        if senha == '':
            flash("Digite uma senha.")
            return render_template("cadastro.html")

        senha_hash = generate_password_hash(senha)
        salvo = salvar_usuario(nome, email, senha_hash)

        if not salvo:
            flash("Esse e-mail já está cadastrado.")
            return render_template("cadastro.html")
        
        flash("Conta criada com sucesso.")
    
    return render_template("cadastro.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":

        email = request.form.get('email', '').strip()
        if email == '':
            flash("Digite um email.")
            return render_template("login.html")

        senha = request.form.get('senha', '')
        if senha == '':
            flash("Digite uma senha.")
            return render_template("login.html")

        usuario = buscar_usuario_por_email(email)

        if not usuario:
            flash("Conta não encontrada.")
            return render_template("login.html")

        if not check_password_hash(usuario.senha_hash, senha):
            flash("Senha incorreta.")
            return render_template("login.html")

        login_user(usuario)
        flash("Login realizado com sucesso.")

    return render_template("login.html")

app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")


if __name__ == '__main__':
    app.run(debug=True, port=5012)

