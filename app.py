from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from routes.usuario_rotas import usuario_rotas
from models.usuario import criar_tabela

app = Flask(__name__)
CORS(app)

# Swagger básico
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Usuários",
        "description": "API para gerenciamento de usuários",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"]
}

Swagger(app, template=swagger_template)

# Inicialização da tabela e rotas
criar_tabela()
app.register_blueprint(usuario_rotas)

if __name__ == '__main__':
    app.run(debug=True)


