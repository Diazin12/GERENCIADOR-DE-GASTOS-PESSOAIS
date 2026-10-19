from models import criar_tabelas, buscar_usuario_por_id, salvar_usuario
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager
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

if __name__ == '__main__':
    app.run(debug=True, port=5012)

