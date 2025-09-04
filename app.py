from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from routes.usuario_rotas import usuario_rotas
from models.usuario import criar_tabela

app = Flask(__name__, static_url_path='/flasgger_static')

# Template básico do Swagger
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Usuários",
        "description": "Documentação da API para gerenciamento de usuários.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"]
}

# Configuração do Swagger, com UI e remoção do footer via JavaScript injetado
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/swagger/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "swagger_ui": True,
    "specs_route": "/swagger/",
    
}

Swagger(app, config=swagger_config, template=swagger_template)

# CORS para rotas
CORS(app, resources={r"/usuarios/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Accept"]
}})

# Inicializações
criar_tabela()
app.register_blueprint(usuario_rotas)

if __name__ == '__main__':
    app.run(debug=True)
