# B-J-Log

# Rodar aplicação BackEnd em produção
- waitress-serve --host=0.0.0.0 --port=5000 wsgi:app

# Rodar migrate
- flask db migrate -m "descricao do migrate"
- flask db upgrade
- flask db downgrade [#version]
