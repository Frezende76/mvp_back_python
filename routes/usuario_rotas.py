from flask import Blueprint, request, jsonify
from models.usuario import cadastrar_usuario, editar_usuario, buscar_usuario, deletar_usuario, buscar_todos_usuarios

usuario_rotas = Blueprint('usuarios', __name__)

# Listar todos usuários / criar novo usuário
@usuario_rotas.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        filtros = {k: v for k, v in request.args.items()}
        usuarios = buscar_todos_usuarios(**filtros)
        return jsonify(usuarios), 200 if usuarios else 404

    if request.method == 'POST':
        dados = request.get_json()
        if not dados or not all(k in dados for k in ('nome','endereco','email','telefone')):
            return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

        novo_usuario = cadastrar_usuario(dados['nome'], dados['endereco'], dados['email'], dados['telefone'])
        if novo_usuario is None:
            return jsonify({'message': 'Usuário já cadastrado!'}), 400

        return jsonify(novo_usuario), 201

# Consultar, editar e deletar por ID
@usuario_rotas.route('/usuarios/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def usuario_id(id):
    usuario = buscar_usuario(id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    if request.method == 'GET':
        return jsonify(usuario), 200

    if request.method == 'PUT':
        dados = request.get_json()
        if not dados or not all(k in dados for k in ('nome','endereco','email','telefone')):
            return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400
        atualizado = editar_usuario(id, dados['nome'], dados['endereco'], dados['email'], dados['telefone'])
        return jsonify(atualizado), 200

    if request.method == 'DELETE':
        deletar_usuario(id)
        return jsonify({'message': 'Usuário deletado com sucesso!'}), 200

