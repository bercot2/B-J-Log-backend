import jwt as jwt_d

from http import HTTPStatus
from flask import request
from flask_jwt_extended import JWTManager

from app.core.responses import AppResponse

jwt = JWTManager()


def register_authentication_hooks(app):
    @app.before_request
    def check_authentication():
        if request.endpoint not in ["auth.login", "auth.logout"]:

            token = request.cookies.get("access_token_cookie")

            if token:
                try:
                    decoded = jwt_d.decode(
                        token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
                    )
                except jwt_d.ExpiredSignatureError:
                    return (
                        AppResponse({"msg": "Token expirado"}),
                        HTTPStatus.UNAUTHORIZED,
                    )
                except jwt_d.InvalidTokenError:
                    return (
                        AppResponse({"msg": "Token inválido"}),
                        HTTPStatus.UNAUTHORIZED,
                    )
            else:
                return AppResponse({"msg": "Token ausente"}), HTTPStatus.UNAUTHORIZED
