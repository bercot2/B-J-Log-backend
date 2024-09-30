import jwt as jwt_d

from http import HTTPStatus
from flask import Flask, request, session
from flask_jwt_extended import JWTManager

from app.core.responses import AppResponse
from app.modules.integracoes.models import Authentication

jwt = JWTManager()


def decode_token(token, secret_key=None, **kwargs):
    return jwt_d.decode(token, secret_key, algorithms=["HS256"], **kwargs)


def validate_bearer_token(bearer_token):
    integration_token = session.get("integration_token", None)

    if not integration_token:
        return (
            None,
            "Autenticação falhou: o token não foi gerado antes da tentativa de acesso.",
        )

    if integration_token["token"] != bearer_token:
        return None, "Token inválido, utilize o último token gerado!"

    authentication = Authentication(**session["integration_token"]["authentication"])

    return decode_token(bearer_token, authentication.secret_key), None


def check_authentication(app: Flask):
    if request.endpoint in [
        "auth.login",
        "auth.logout",
        "auth.generate_token",
        "auth.protected",
    ]:
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
