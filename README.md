# B-J-Log

# Rodar aplicação BackEnd em produção

- waitress-serve --host=0.0.0.0 --port=5000 wsgi:app

# Rodar migrate

- flask db migrate -m "descricao do migrate"
- flask db upgrade
- flask db downgrade [#version]

# Comandos Docker

-Fazer build:
    - docker-compose up --build

-Fazer build específica:
    - docker-compose up --build backend
    - docker-compose up --build frontend

- Subir Containers com a imagem gerada anteriormente
    - docker run -d -p 8080:5000 b-j-log-backend
    - docker run -d -p 8081:3000 b-j-log-frontend
