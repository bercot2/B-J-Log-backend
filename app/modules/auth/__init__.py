import jwt as jwt_d

from http import HTTPStatus
from flask import Flask, request
from flask_jwt_extended import JWTManager

from app.core.responses import AppResponse
from app.modules.integracoes.models import Authentication

jwt = JWTManager()


def decode_token(token, secret_key=None, **kwargs):
    if not secret_key:
        return jwt_d.decode(token, algorithms=["HS256"], **kwargs)

    return jwt_d.decode(token, secret_key, algorithms=["HS256"], **kwargs)


def validate_bearer_token(bearer_token):
    partial_decoded = decode_token(bearer_token, options={"verify_signature": False})
    nome = partial_decoded.get("nome")
    chave_acesso = partial_decoded.get("chave_acesso")

    if not chave_acesso:
        return None, "Token inválido, chave de acesso ausente"

    authentication = Authentication.get_authentication(nome, chave_acesso)
    return decode_token(bearer_token, authentication.secret_key), None


def check_authentication(app: Flask):
    if request.endpoint in ["auth.login", "auth.logout", "auth.generate_token"]:
        return

    token_cookie = request.cookies.get("access_token_cookie")
    bearer_token = getattr(request.authorization, "token", None)

    try:
        if token_cookie:
            decoded = decode_token(token_cookie, app.config["JWT_SECRET_KEY"])
        elif bearer_token:
            decoded, error_message = validate_bearer_token(bearer_token)
            if error_message:
                return AppResponse({"msg": error_message}), HTTPStatus.UNAUTHORIZED
        else:
            return AppResponse({"msg": "Token ausente"}), HTTPStatus.UNAUTHORIZED
    except jwt_d.ExpiredSignatureError:
        return AppResponse({"msg": "Token expirado"}), HTTPStatus.UNAUTHORIZED
    except jwt_d.InvalidTokenError:
        return AppResponse({"msg": "Token inválido"}), HTTPStatus.UNAUTHORIZED


def register_authentication_hooks(app):
    @app.before_request
    def before_request():
        return check_authentication(app)
