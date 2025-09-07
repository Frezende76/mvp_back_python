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
    description: Retorna a lista de usuários. Aceita filtros opcionais por query string.
    parameters:
      - name: nome
        in: query
        type: string
        required: false
        description: Filtrar por nome (LIKE)
      - name: endereco
        in: query
        type: string
        required: false
        description: Filtrar por endereço (LIKE)
      - name: email
        in: query
        type: string
        required: false
        description: Filtrar por email (LIKE)
      - name: telefone
        in: query
        type: string
        required: false
        description: Filtrar por telefone (LIKE)
    responses:
      200:
        description: Lista de usuários retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              endereco:
                type: string
              email:
                type: string
              telefone:
                type: string
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
    description: Cadastra um novo usuário. O campo 'nome' é único.
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
            - endereco
            - email
            - telefone
    responses:
      201:
        description: Usuário cadastrado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            endereco:
              type: string
            email:
              type: string
            telefone:
              type: string
      400:
        description: Usuário já existe ou dados inválidos
    """
    dados = request.get_json()
    if not dados or not all(k in dados for k in ('nome', 'endereco', 'email', 'telefone')):
        return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

    novo_usuario = cadastrar_usuario(dados['nome'], dados['endereco'], dados['email'], dados['telefone'])
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
        description: Nome do usuário
    responses:
      200:
        description: Usuário encontrado
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            endereco:
              type: string
            email:
              type: string
            telefone:
              type: string
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
        description: Nome do usuário a ser atualizado
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
        schema:
          type: object
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
        description: Nome do usuário a ser removido
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






