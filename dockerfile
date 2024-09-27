# Use a imagem base do Python
FROM python:3.11-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie o código do backend para o container
COPY . .

# Exponha a porta 8000 (ou a porta que seu app usa)
EXPOSE 5000

# Comando para rodar o servidor Python (exemplo usando Flask ou FastAPI)
CMD ["flask", "run"]
