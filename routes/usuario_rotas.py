from flask import Blueprint, request, jsonify, Response
from models.usuario import cadastrar_usuario, editar_usuario, buscar_usuario, deletar_usuario, buscar_todos_usuarios
from schemas.usuario_schema import UsuarioSchema
from flasgger import swag_from
import json

# Função auxiliar para gerar respostas JSON
def gerar_resposta_json(data, status_code=200):
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json', status=status_code)

# Criação de um Blueprint para as rotas de usuário
usuario_rotas = Blueprint('usuarios', __name__)

@usuario_rotas.route('/usuarios/cadastrar', methods=['POST'])
def cadastrar_usuario_bd():
    """
    Cadastrar um novo usuário
    ---
    tags:
      - Usuários
    consumes:
      - application/json
    parameters:
      - in: body
        name: corpo
        required: true
        schema:
          type: object
          required:
            - nome
            - endereco
            - email
            - telefone
          properties:
            nome:
              type: string
            endereco:
              type: string
            email:
              type: string
            telefone:
              type: string
    responses:
      201:
        description: Usuário cadastrado com sucesso
      400:
        description: Campos obrigatórios faltando ou usuário já cadastrado
    """
    dados = request.get_json(silent=True)

    if isinstance(dados, list):
        dados = dados[0]

    if not isinstance(dados, dict):
        return jsonify({'message': 'Dados inválidos!'}), 400

    nome = dados.get('nome')
    endereco = dados.get('endereco')
    email = dados.get('email')
    telefone = dados.get('telefone')

    if not all([nome, endereco, email, telefone]):
        return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

    novo_usuario = cadastrar_usuario(nome, endereco, email, telefone)
    if novo_usuario is None:
        return jsonify({'message': 'Usuário já cadastrado!'}), 400

    return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201

@usuario_rotas.route('/usuarios/editar/<int:id>', methods=['PUT'])
def editar_usuario_bd(id):
    """
    Editar um usuário existente
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: corpo
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
    responses:
      200:
        description: Usuário editado com sucesso
      404:
        description: Usuário não encontrado
    """
    dados = request.get_json(silent=True)

    if isinstance(dados, list):
        dados = dados[0]

    if not isinstance(dados, dict):
        return jsonify({'message': 'Dados inválidos!'}), 400

    nome = dados.get('nome')
    endereco = dados.get('endereco')
    email = dados.get('email')
    telefone = dados.get('telefone')

    if not all([nome, endereco, email, telefone]):
        return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

    usuario = editar_usuario(id, nome, endereco, email, telefone)
    if usuario:
        usuario_schema = UsuarioSchema()
        usuario_dict = usuario_schema.dump(usuario)
        return gerar_resposta_json(usuario_dict), 200

    return gerar_resposta_json({'message': 'Nenhum usuário encontrado'}, 404)

@usuario_rotas.route('/usuarios/buscar/<int:id>', methods=['GET'])
def buscar_usuario_bd(id):
    """
    Buscar um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Usuário encontrado
      404:
        description: Usuário não encontrado
    """
    usuario = buscar_usuario(id)
    if usuario:
        usuario_schema = UsuarioSchema()
        usuario_dict = usuario_schema.dump(usuario)
        return gerar_resposta_json(usuario_dict), 200

    return gerar_resposta_json({'message': 'Nenhum usuário encontrado'}, 404)

@usuario_rotas.route('/usuarios/deletar/<int:id>', methods=['DELETE'])
def deletar_usuario_bd(id):
    """
    Deletar um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Usuário deletado com sucesso
      404:
        description: Usuário não encontrado
    """
    usuario = buscar_usuario(id)

    if usuario:
        deletar_usuario(id)
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200

    return jsonify({'message': 'Usuário não encontrado'}), 404

@usuario_rotas.route('/usuarios/todos', methods=['GET'])
def buscar_todos_usuarios_bd():
    """
    Buscar todos os usuários (com filtros opcionais)
    ---
    tags:
      - Usuários
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
        description: Lista de usuários retornada
      404:
        description: Nenhum usuário encontrado
    """
    filtros = {}

    nome = request.args.get('nome')
    if nome:
        filtros['nome'] = nome.strip()

    endereco = request.args.get('endereco')
    if endereco:
        filtros['endereco'] = endereco.strip()

    email = request.args.get('email')
    if email:
        filtros['email'] = email.strip()

    telefone = request.args.get('telefone')
    if telefone:
        filtros['telefone'] = telefone.strip()

    usuarios = buscar_todos_usuarios(**filtros)
    if usuarios:
        usuario_schema = UsuarioSchema(many=True)
        return gerar_resposta_json(usuario_schema.dump(usuarios)), 200

    return gerar_resposta_json({'message': 'Nenhum usuário encontrado'}, 404)

@usuario_rotas.route('/usuarios/verificar', methods=['POST'])
def verificar_usuario_bd():
    """
    Verificar se um usuário já está cadastrado
    ---
    tags:
      - Usuários
    consumes:
      - application/json
    parameters:
      - in: body
        name: corpo
        required: true
        schema:
          type: object
          required:
            - nome
            - endereco
            - email
            - telefone
          properties:
            nome:
              type: string
            endereco:
              type: string
            email:
              type: string
            telefone:
              type: string
    responses:
      200:
        description: Usuário não encontrado
      400:
        description: Usuário já cadastrado
    """
    dados = request.get_json(silent=True)

    if isinstance(dados, list):
        dados = dados[0]

    if not isinstance(dados, dict):
        return gerar_resposta_json({'message': 'Dados inválidos!'}), 400

    nome = dados.get('nome', '')
    endereco = dados.get('endereco', '')
    email = dados.get('email', '')
    telefone = dados.get('telefone', '')

    usuarios = buscar_todos_usuarios(nome=nome, endereco=endereco, email=email, telefone=telefone)

    if usuarios:
        return gerar_resposta_json({'usuarioExistente': True, 'message': 'Usuário já cadastrado'}), 400

    return gerar_resposta_json({'usuarioExistente': False, 'message': 'Nenhum usuário encontrado'}, 200)


