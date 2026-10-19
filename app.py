from models import criar_tabelas, buscar_usuario_por_id
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


if __name__ == '__main__':
    app.run(debug=True, port=5012)