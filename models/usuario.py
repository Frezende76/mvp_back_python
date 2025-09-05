import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, '..', 'databases')
DB_PATH = os.path.join(DB_DIR, 'dados_cliente.db')

os.makedirs(DB_DIR, exist_ok=True)

def conectar_bd():
    return sqlite3.connect(DB_PATH)

def criar_tabela():
    with conectar_bd() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL
        )''')

def usuario_existe(nome, endereco, email, telefone):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id FROM usuarios WHERE nome=? AND endereco=? AND email=? AND telefone=?',
            (nome, endereco, email, telefone)
        )
        return cursor.fetchone() is not None

def cadastrar_usuario(nome, endereco, email, telefone):
    if usuario_existe(nome, endereco, email, telefone):
        return None
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (nome, endereco, email, telefone) VALUES (?, ?, ?, ?)',
            (nome, endereco, email, telefone)
        )
        conn.commit()
        return buscar_usuario(cursor.lastrowid)

def editar_usuario(id, nome, endereco, email, telefone):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE usuarios SET nome=?, endereco=?, email=?, telefone=? WHERE id=?',
            (nome, endereco, email, telefone, id)
        )
        conn.commit()
        return buscar_usuario(id)

def buscar_usuario(id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id=?', (id,))
        usuario = cursor.fetchone()
        return {
            'id': usuario[0],
            'nome': usuario[1],
            'endereco': usuario[2],
            'email': usuario[3],
            'telefone': usuario[4]
        } if usuario else None

def deletar_usuario(id):
    with conectar_bd() as conn:
        conn.execute('DELETE FROM usuarios WHERE id=?', (id,))
        conn.commit()

def buscar_todos_usuarios(nome='', endereco='', email='', telefone=''):
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

