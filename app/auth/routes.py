from flask import Blueprint
from .models import TokenAcesso, TerceirosIntegracao

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
