import jwt

from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from flask import Blueprint, jsonify, session, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    set_access_cookies,
    verify_jwt_in_request,
)

from app.modules.cadastros.models import Usuario
from app.modules.integracoes.models import Authentication
from app.core.functions import check_password, is_email
from app.core.responses import AppResponse
from app.serializer import Serializer

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/generate-token")
def generate_token():
    authentication = Authentication.get_authentication(
        request.json.get("nome", None), request.json.get("chave_acesso", None)
    )

    payload = {
        "nome": authentication.nome,
        "chave_acesso": authentication.chave_acesso,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(payload, authentication.secret_key, algorithm="HS256")

    session["integration_token"] = {
        "token": token,
        "authentication": Serializer(model=authentication).serialize(),
    }

    return AppResponse({"token": token}), HTTPStatus.OK


@auth_bp.post("/login")
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if is_email(username):
        user = Usuario.query.filter_by(email=username).first()
    else:
        user = Usuario.query.filter_by(username=username).first()

    # Validação do usuário
    if not (user and check_password(password, user.password)):
        response = AppResponse({"msg": "Usuário ou senha inválidos"})

        response.delete_cookie("access_token")
        response.delete_cookie("access_token_cookie")
        response.delete_cookie("csrf_access_token")

        return (
            response,
            HTTPStatus.UNAUTHORIZED,
        )

    session["user"] = user.get_schema(
        fields_list=["id", "nome", "email", "username", "is_staff", "is_superuser"]
    ).dump(user)
    session["user_empresas"] = [
        empresa.get_schema().dump(empresa) for empresa in user.empresas
    ]

    # Gera o token JWT
    access_token = create_access_token(identity=user.id)

    response = AppResponse({"token": access_token})
    set_access_cookies(response, access_token)

    return response, HTTPStatus.OK


@auth_bp.post("/logout")
def logout():
    response = AppResponse({"msg": "Logout bem-sucedido"})

    response.delete_cookie("access_token")
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("csrf_access_token")

    return response, HTTPStatus.OK


@auth_bp.get("/protected")
@jwt_required()
def protected():
    jwt = get_jwt()

    if jwt.get("csrf") == request.headers.get("X-CSRF-TOKEN", None):
        return AppResponse({"mesage": "Acesso Válido"}), HTTPStatus.OK
    else:
        return AppResponse({"mesage": "Acesso Inválido"}), HTTPStatus.UNAUTHORIZED
