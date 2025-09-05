from flask import Blueprint, request, jsonify
from models.usuario import cadastrar_usuario, editar_usuario, buscar_usuario, deletar_usuario, buscar_todos_usuarios

usuario_rotas = Blueprint('usuarios', __name__)

@usuario_rotas.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    """
    Lista todos os usuários ou cadastra um novo usuário
    ---
    get:
      summary: Lista todos os usuários
      responses:
        200:
          description: Lista de usuários
          content:
            application/json:
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
    post:
      summary: Cria um novo usuário
      requestBody:
        required: true
        content:
          application/json:
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
          description: Usuário criado com sucesso
        400:
          description: Erro de validação ou usuário duplicado
    """
    if request.method == 'GET':
        filtros = {k: v for k, v in request.args.items()}
        usuarios = buscar_todos_usuarios(**filtros)
        return jsonify(usuarios), 200

    if request.method == 'POST':
        dados = request.get_json()
        if not dados or not all(k in dados for k in ('nome','endereco','email','telefone')):
            return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

        novo_usuario = cadastrar_usuario(dados['nome'], dados['endereco'], dados['email'], dados['telefone'])
        if novo_usuario is None:
            return jsonify({'message': 'Usuário já cadastrado!'}), 400

        return jsonify(novo_usuario), 201


@usuario_rotas.route('/usuarios/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def usuario_id(id):
    """
    Consulta, atualiza ou deleta usuário por ID
    ---
    get:
      summary: Consulta usuário por ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Usuário encontrado
        404:
          description: Usuário não encontrado
    put:
      summary: Atualiza usuário por ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
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
        200:
          description: Usuário atualizado com sucesso
        400:
          description: Dados inválidos
    delete:
      summary: Deleta usuário por ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Usuário deletado com sucesso
        404:
          description: Usuário não encontrado
    """
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
