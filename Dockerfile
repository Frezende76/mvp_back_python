# Usa imagem oficial do Python
FROM python:3.10-slim

# Define diretório de trabalho no container
WORKDIR /app

# Copia arquivos do projeto para dentro do container
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão do Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
