# Use a imagem base do Python
FROM python:3.11

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie o código do backend para o container
COPY . .

EXPOSE 5000

# Comando para rodar o servidor usando Waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "wsgi:app"]
