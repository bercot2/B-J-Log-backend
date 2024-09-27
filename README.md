# B-J-Log

# Rodar aplicação BackEnd em produção

- waitress-serve --host=0.0.0.0 --port=5000 wsgi:app

# Rodar migrate

- flask db migrate -m "descricao do migrate"
- flask db upgrade
- flask db downgrade [#version]

# Comandos Docker

- Fazer build:

  - docker-compose build

- Fazer build específica:

  - docker-compose build <nome-do-servico>

- Subir imagem do docker gerada anteriormente

  - docker-compose up

- Subir Containers com a imagem gerada anteriormente
  - docker run -d -p 8080:5000 b-j-log-backend
