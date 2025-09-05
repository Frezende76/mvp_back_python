from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from routes.usuario_rotas import usuario_rotas
from models.usuario import criar_tabela

app = Flask(__name__)
CORS(app)

# Inicializa tabela SQLite
criar_tabela()

# Template mínimo do Swagger
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Usuários",
        "description": "API para gerenciamento de usuários",
        "version": "1.0.0"
    }
}

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",   # JSON acessível
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/swagger",
    "swagger_ui": True,
    "specs_route": "/swagger/"   # <<< precisa da barra final
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Registra rotas
app.register_blueprint(usuario_rotas)

if __name__ == "__main__":
    app.run(debug=True)





