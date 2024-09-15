from flask import Blueprint, jsonify
from ..models import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuario')

@usuarios_bp.route('/', methods=['GET'])
def get_usuarios():
    # Exemplo de retorno
    return jsonify({'message': 'Lista de usuários'})

@usuarios_bp.route('/<int:id>', methods=['GET'])
def get_usuario(id):
    # Exemplo de retorno
    return jsonify({'message': f'Usuário {id}'})