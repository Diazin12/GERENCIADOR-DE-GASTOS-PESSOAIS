from models import criar_tabelas, buscar_usuario_por_id, salvar_usuario, buscar_usuario_por_email, listar_gastos_usuario, salvar_gasto, atualizar_gasto, buscar_gasto_por_id, excluir_gasto
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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

        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route('/dashboard', methods = ['GET'])
@login_required
def dashboard():
    gastos = listar_gastos_usuario(current_user.id)
    return render_template("dashboard.html", gastos = gastos)

@app.route('/logout', methods = ['POST'])
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.")
    return redirect(url_for("login"))

@app.route('/gastos/novo', methods = ['GET', 'POST'])
@login_required
def novo_gasto():
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        valor_texto = request.form.get('valor', '').strip()
        categoria = request.form.get('categoria', '').strip()
        data = request.form.get('data', '').strip()

        if descricao == '':
            flash("Digite uma descrição.")
            return render_template("form_gasto.html")

        if valor_texto == '':
            flash("Digite um valor.")
            return render_template("form_gasto.html")

        try:
            valor = float(valor_texto)
        except ValueError:
            flash("Digite um valor válido.")
            return render_template("form_gasto.html")

        if valor <= 0:
            flash("O valor precisa ser maior que zero.")
            return render_template("form_gasto.html")

        if categoria == '':
            flash("Selecione uma categoria.")
            return render_template("form_gasto.html")

        if data == '':
            flash("Digite uma data.")
            return render_template("form_gasto.html")

        salvo = salvar_gasto(
            descricao,
            valor,
            categoria,
            data,
            current_user.id
        )

        if not salvo:
            flash("Não foi possível salvar o gasto.")
            return render_template("form_gasto.html")

        flash("Gasto cadastrado com sucesso.")
        return redirect(url_for("dashboard"))

    return render_template("form_gasto.html")

@app.route('/gastos/editar/<int:gasto_id>', methods = ['GET', 'POST'])
@login_required
def editar_gasto(gasto_id):
    gasto = buscar_gasto_por_id(gasto_id, current_user.id)
    if gasto is None:
        flash("Gasto nao encontrado.")
        return redirect(url_for("dashboard"))

    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        valor_texto = request.form.get('valor', '').strip()
        categoria = request.form.get('categoria', '').strip()
        data = request.form.get('data', '').strip()
    
        if descricao == '':
            flash("Digite uma descrição.")
            return render_template("form_gasto.html", gasto=gasto)
    
        if valor_texto == '':
            flash("Digite um valor.")
            return render_template("form_gasto.html", gasto=gasto)
    
        try:
            valor = float(valor_texto)
        except ValueError:
            flash("Digite um valor válido.")
            return render_template("form_gasto.html", gasto=gasto)
    
        if valor <= 0:
            flash("O valor precisa ser maior que zero.")
            return render_template("form_gasto.html", gasto=gasto)
    
        if categoria == '':
            flash("Selecione uma categoria.")
            return render_template("form_gasto.html", gasto=gasto)
    
        if data == '':
            flash("Digite uma data.")
            return render_template("form_gasto.html", gasto=gasto)

        atualizado = atualizar_gasto(
            gasto_id,
            descricao,
            valor,
            categoria,
            data,
            current_user.id
        )

        if not atualizado:
            flash("Não foi possível atualizar o gasto.")
            return render_template("form_gasto.html", gasto=gasto)

        flash("Gasto atualizado com sucesso.")
        return redirect(url_for("dashboard"))
    

    return render_template("form_gasto.html", gasto=gasto)

@app.route('/gasto/excluir/<int:gasto_id>', methods = ['POST'])
@login_required
def remover_gasto(gasto_id):
    removido = excluir_gasto(gasto_id, current_user.id)

    if removido:
        flash("Gasto removido com sucesso!")
    else:
        flash("Gasto não encontrado ou não pertence a você.")

    return redirect(url_for("dashboard"))



if __name__ == '__main__':

    app.run(debug=True, port=5012)

