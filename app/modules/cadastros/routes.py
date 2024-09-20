from flask import Blueprint
from .Views import usuarios

cadastros_bp = Blueprint('cadastros', __name__, url_prefix='/cadastros')

cadastros_bp.register_blueprint(usuarios.usuarios_bp)