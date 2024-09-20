import jwt as jwt_d

from http import HTTPStatus
from flask import request
from flask_jwt_extended import JWTManager

from app.core.responses import AppResponse
from app.modules.integracoes.models import Authentication

jwt = JWTManager()


def register_authentication_hooks(app):
    @app.before_request
    def check_authentication():
        if request.endpoint not in ["auth.login", "auth.logout", "auth.generate_token"]:

            token_cookie = request.cookies.get("access_token_cookie")
            bearer_token = getattr(request.authorization, "token", None)

            try:
                if token_cookie:
                    decoded = jwt_d.decode(
                        token_cookie, app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
                    )
                elif bearer_token:
                    # Decodificar o token sem verificar a assinatura para pegar a chave de acesso
                    partial_decoded = jwt_d.decode(
                        bearer_token,
                        options={"verify_signature": False},
                        algorithms=["HS256"],
                    )

                    nome = partial_decoded.get("nome")
                    chave_acesso = partial_decoded.get("chave_acesso")

                    if not chave_acesso:
                        return (
                            AppResponse(
                                {"msg": "Token inválido, chave de acesso ausente"}
                            ),
                            HTTPStatus.UNAUTHORIZED,
                        )

                    authentication = Authentication.get_authentication(
                        nome, chave_acesso
                    )

                    decoded = jwt_d.decode(
                        bearer_token, authentication.secret_key, algorithms=["HS256"]
                    )
                else:
                    return (
                        AppResponse({"msg": "Token ausente"}),
                        HTTPStatus.UNAUTHORIZED,
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
