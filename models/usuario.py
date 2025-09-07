import sqlite3
import os

# Caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, '..', 'databases')
DB_PATH = os.path.join(DB_DIR, 'dados_cliente.db')

# Garante que a pasta existe
os.makedirs(DB_DIR, exist_ok=True)


def conectar_bd():
    """Conecta ao banco de dados SQLite"""
    return sqlite3.connect(DB_PATH)


def criar_tabela():
    """Cria a tabela de usuários, se não existir"""
    with conectar_bd() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            endereco TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
        ''')


def usuario_existe(nome):
    """Verifica se um usuário já existe pelo nome"""
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE nome=?', (nome,))
        return cursor.fetchone() is not None


def cadastrar_usuario(nome, endereco, email, telefone):
    """Cadastra um novo usuário (não permite nomes duplicados)"""
    if usuario_existe(nome):
        return None
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (nome, endereco, email, telefone) VALUES (?, ?, ?, ?)',
            (nome, endereco, email, telefone)
        )
        conn.commit()
        return buscar_usuario(nome)


def editar_usuario(nome, endereco, email, telefone):
    """Edita os dados de um usuário pelo nome"""
    if not usuario_existe(nome):
        return None
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE usuarios SET endereco=?, email=?, telefone=? WHERE nome=?',
            (endereco, email, telefone, nome)
        )
        conn.commit()
        return buscar_usuario(nome)


def buscar_usuario(nome):
    """Busca um único usuário pelo nome"""
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nome=?', (nome,))
        usuario = cursor.fetchone()
        return {
            'id': usuario[0],
            'nome': usuario[1],
            'endereco': usuario[2],
            'email': usuario[3],
            'telefone': usuario[4]
        } if usuario else None


def deletar_usuario(nome):
    """Deleta um usuário pelo nome"""
    if not usuario_existe(nome):
        return False
    with conectar_bd() as conn:
        conn.execute('DELETE FROM usuarios WHERE nome=?', (nome,))
        conn.commit()
    return True


def buscar_todos_usuarios(nome='', endereco='', email='', telefone=''):
    """
    Lista todos os usuários, com filtros opcionais.
    Se os filtros forem passados, aplica busca por LIKE.
    """
    query = 'SELECT * FROM usuarios WHERE 1=1'
    params = []

    if nome:
        query += ' AND nome LIKE ?'
        params.append(f'%{nome}%')
    if endereco:
        query += ' AND endereco LIKE ?'
        params.append(f'%{endereco}%')
    if email:
        query += ' AND email LIKE ?'
        params.append(f'%{email}%')
    if telefone:
        query += ' AND telefone LIKE ?'
        params.append(f'%{telefone}%')

    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        usuarios = cursor.fetchall()
        return [
            {'id': u[0], 'nome': u[1], 'endereco': u[2], 'email': u[3], 'telefone': u[4]}
            for u in usuarios
        ]


