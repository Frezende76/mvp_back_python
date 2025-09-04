from marshmallow import Schema, fields, validate


# Define a classe de esquema para validação e 
# serialização de dados do usuário
class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True) # 'id' será apenas para leitura. Não será exigido no processo de entrada
    nome = fields.Str(required=True) # 'nome' é obrigatório e será uma string
    endereco = fields.Str(required=True) # 'endereco' é obrigatório e será uma string
    email = fields.Email(required=True) # 'email' é obrigatório e deve ser um e-mail válido
    # Definindo uma expressão regular para validar o formato do telefone
    telefone = fields.Str(required=True, validate=validate.Regexp(r'^\(\d{2}\) \d{4,5}-\d{4}$', error="Telefone inválido. Formato esperado: (XX) XXXX-XXXX ou (XX) XXXXX-XXXX"))

    class Meta:
        # Garantir que os campos sejam serializados na ordem que você define
        ordered = True