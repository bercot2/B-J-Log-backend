from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, set_access_cookies

from app.cadastros.models import Usuario
from app.core.functions import check_password, hash_password, is_email
from app.core.responses import AppResponse

# from .models import TokenAcesso, TerceirosIntegracao

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if is_email(username):
        user = Usuario.query.filter_by(email=username).first()
    else:
        user = Usuario.query.filter_by(username=username).first()

    # Validação do usuário
    if not (user and check_password(password, user.password)):
        return (
            AppResponse({"msg": "Usuário ou senha inválidos"}),
            HTTPStatus.UNAUTHORIZED,
        )

    # Gera o token JWT
    access_token = create_access_token(identity=username)

    response = AppResponse({"token": access_token})
    set_access_cookies(response, access_token)

    return response, HTTPStatus.OK


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = AppResponse({"msg": "Logout bem-sucedido"})

    response.delete_cookie("access_token")
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("csrf_access_token")

    return response, HTTPStatus.OK
