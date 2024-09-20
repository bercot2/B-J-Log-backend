from http import HTTPStatus
from flask import Blueprint, request

from app.core.responses import AppResponse
from app.serializer import Serializer

from .models import Authentication

integracoes_bp = Blueprint("integracoes", __name__, url_prefix="/integracoes")


@integracoes_bp.post("/cadastrar-terceiro")
def cadastrar_integracao_terceiro():
    body = request.json.copy()

    if nome := body.get("nome", None):
        authentication = Authentication.query.filter_by(nome=nome).first()

        if not authentication:
            authentication = Authentication(**body).insert()

            return AppResponse(Serializer(model=authentication)), HTTPStatus.CREATED
        else:
            return (
                AppResponse({"message": f"Chave de Acesso já existente para {nome}"}),
                HTTPStatus.CONFLICT,
            )

    return (
        AppResponse({"message": "Não encontrado a key 'nome' no body da request"}),
        HTTPStatus.BAD_REQUEST,
    )
