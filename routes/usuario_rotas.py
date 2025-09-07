from flask import Blueprint, request, jsonify
from models.usuario import (
    cadastrar_usuario,
    editar_usuario,
    buscar_usuario,
    deletar_usuario,
    buscar_todos_usuarios
)

usuario_rotas = Blueprint('usuarios', __name__)

# -------------------------
# LISTAR TODOS OS USUÁRIOS
# -------------------------
@usuario_rotas.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """
    Listar todos os usuários
    ---
    tags:
      - Usuários
    description: Retorna todos os usuários cadastrados. Aceita filtros opcionais.
    parameters:
      - name: nome
        in: query
        type: string
        required: false
      - name: endereco
        in: query
        type: string
        required: false
      - name: email
        in: query
        type: string
        required: false
      - name: telefone
        in: query
        type: string
        required: false
    responses:
      200:
        description: Lista de usuários retornada com sucesso
    """
    filtros = {k: v for k, v in request.args.items()}
    usuarios = buscar_todos_usuarios(**filtros)
    return jsonify(usuarios), 200

# -------------------------
# CADASTRAR UM USUÁRIO
# -------------------------
@usuario_rotas.route('/usuarios', methods=['POST'])
def cadastrar_usuario_endpoint():
    """
    Cadastrar um usuário
    ---
    tags:
      - Usuários
    description: Cadastra um novo usuário. Se o nome já existir, os campos serão preenchidos automaticamente com os dados existentes.
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            endereco:
              type: string
            email:
              type: string
            telefone:
              type: string
          required:
            - nome
    responses:
      201:
        description: Usuário cadastrado com sucesso
      400:
        description: Usuário já existe ou dados inválidos
    """
    dados = request.get_json()
    if not dados or 'nome' not in dados:
        return jsonify({'message': 'Nome é obrigatório!'}), 400

    nome = dados['nome']
    existente = buscar_usuario(nome)

    if existente:
        endereco = existente['endereco']
        email = existente['email']
        telefone = existente['telefone']
    else:
        if not all(k in dados for k in ('endereco', 'email', 'telefone')):
            return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400
        endereco = dados['endereco']
        email = dados['email']
        telefone = dados['telefone']

    novo_usuario = cadastrar_usuario(nome, endereco, email, telefone)
    if novo_usuario is None:
        return jsonify({'message': 'Usuário já cadastrado!'}), 400

    return jsonify(novo_usuario), 201

# -------------------------
# CONSULTAR POR NOME
# -------------------------
@usuario_rotas.route('/usuarios/<string:nome>', methods=['GET'])
def consultar_usuario(nome):
    """
    Consultar um usuário
    ---
    tags:
      - Usuários
    description: Retorna os dados de um usuário pelo nome.
    parameters:
      - name: nome
        in: path
        type: string
        required: true
    responses:
      200:
        description: Usuário encontrado
      404:
        description: Usuário não encontrado
    """
    usuario = buscar_usuario(nome)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    return jsonify(usuario), 200

# -------------------------
# EDITAR POR NOME
# -------------------------
@usuario_rotas.route('/usuarios/<string:nome>', methods=['PUT'])
def editar_usuario_endpoint(nome):
    """
    Editar um usuário
    ---
    tags:
      - Usuários
    description: Atualiza endereço, email e telefone do usuário identificado pelo nome.
    consumes:
      - application/json
    parameters:
      - name: nome
        in: path
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            endereco:
              type: string
            email:
              type: string
            telefone:
              type: string
          required:
            - endereco
            - email
            - telefone
    responses:
      200:
        description: Usuário atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Usuário não encontrado
    """
    usuario = buscar_usuario(nome)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    dados = request.get_json()
    if not dados or not all(k in dados for k in ('endereco', 'email', 'telefone')):
        return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

    atualizado = editar_usuario(nome, dados['endereco'], dados['email'], dados['telefone'])
    return jsonify(atualizado), 200

# -------------------------
# DELETAR POR NOME
# -------------------------
@usuario_rotas.route('/usuarios/<string:nome>', methods=['DELETE'])
def deletar_usuario_endpoint(nome):
    """
    Deletar um usuário
    ---
    tags:
      - Usuários
    description: Remove um usuário do sistema pelo nome.
    parameters:
      - name: nome
        in: path
        type: string
        required: true
    responses:
      200:
        description: Usuário deletado com sucesso
      404:
        description: Usuário não encontrado
    """
    usuario = buscar_usuario(nome)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    deletar_usuario(nome)
    return jsonify({'message': 'Usuário deletado com sucesso!'}), 200












