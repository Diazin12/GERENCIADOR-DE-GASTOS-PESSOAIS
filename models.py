#Banco de Dados
import sqlite3
import os
from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, nome, email, senha_hash):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    @classmethod
    def from_tupla(cls, tupla):
        return cls(*tupla)

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "gastos.db")

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def buscar_usuario_por_id(id_usuario):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, nome, email, senha_hash FROM usuario WHERE id = ?",
            (id_usuario,)
        )
        
        usuario = cursor.fetchone()

        if usuario is None:
            return None

        return Usuario.from_tupla(usuario)

    finally:
        conexao.close()

def salvar_usuario(nome, email, senha_hash):
    conexao = None
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuario (nome, email, senha_hash) VALUES (?, ?, ?)",
                           (nome, email, senha_hash)
                           )
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        if conexao is not None:
            conexao.close()

def buscar_usuario_por_email(email):
    conexao = None
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, senha_hash FROM usuario WHERE email = ?",
                           (email,)
                           )
            usuario = cursor.fetchone()

            if usuario is None:
                return None

            return Usuario.from_tupla(usuario)

    finally:
        if conexao is not None:
            conexao.close()


def listar_gastos_usuario(id_usuario):
    conexao = None
    try:
        with conectar() as conexao:
            cursor  = conexao.cursor()
            cursor.execute(
                """
                SELECT id, descricao, valor, categoria, data 
                FROM gastos
                WHERE usuario_id = ?
                ORDER BY data DESC
                """,
                (id_usuario,)
            )
            gastos = cursor.fetchall()
            return gastos

    finally:
        if conexao is not None:
            conexao.close()

def salvar_gasto(descricao, valor, categoria, data, usuario_id):
    conexao = None
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO gastos (descricao, valor, categoria, data, usuario_id) VALUES (?, ?, ?, ?, ?)",
                (descricao, valor, categoria, data, usuario_id)
            )

            return True
        
    except sqlite3.IntegrityError:
        return False
    
    finally:
        if conexao is not None:
            conexao.close()

def atualizar_gasto(gasto_id, descricao, valor, categoria, data, usuario_id):
    conexao = conectar()

    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            UPDATE gastos
            SET descricao = ?, valor = ?, categoria = ?, data = ?
            WHERE id = ? AND usuario_id = ?
            """,
            (descricao, valor, categoria, data, gasto_id, usuario_id)
        )
        conexao.commit()
        return cursor.rowcount > 0

    finally:
        if conexao is not None:
            conexao.close()

def buscar_gasto_por_id(gasto_id, usuario_id):
    conexao = conectar()

    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT id, descricao, valor, categoria, data
            FROM gastos
            WHERE id = ? AND usuario_id = ?
            """,
            (gasto_id, usuario_id)
        )

        return cursor.fetchone()

    finally:
        if conexao is not None:
            conexao.close()

def excluir_gasto(gasto_id, usuario_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM gastos WHERE id = ? AND usuario_id = ?",
                       (gasto_id, usuario_id)
                       )
        conexao.commit()
        return cursor.rowcount > 0

    finally:
        conexao.close()
        
def criar_tabelas():
    conexao = None
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gastos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT NOT NULL,
                data TEXT NOT NULL,
                usuario_id INTEGER NOT NULL REFERENCES usuario(id)
                )
            """)
            return True

    finally:
        if conexao is not None:
            conexao.close()
