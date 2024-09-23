from http import HTTPStatus
from flask import Blueprint, request
from app.core.database import Model, Query
from app.core.decorators import queryset
from app.core.functions import hash_password
from app.core.responses import AppResponse
from app.serializer import Serializer
from ..models import Empresa, Usuario, UsuarioEmpresa

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.get("/")
@queryset(
    base_model=Usuario, override_query=Usuario.get_user_empresa, filter_fields="__all__"
)
def get_usuarios():
    serializer = Serializer.transform(
        schema=Model.get_schema(
            fields_list=["id", "nome", "email"],
            empresa=Empresa.get_schema(fields_list=["id", "cnpj", "razao_social"]),
        ),
        query=Query.get_queryset(),
    )

    return AppResponse(serializer), HTTPStatus.OK


@usuarios_bp.post("/")
def post_usuarios():
    body = request.json.copy()

    body["password"] = hash_password(body.get("password", None)).decode("utf-8")

    if body["username"] and body["password"]:
        user = Usuario(**body).insert()

        return AppResponse(Serializer(model=user)), HTTPStatus.CREATED

    return AppResponse({"message": "Usuário não cadastrado"}), HTTPStatus.NOT_FOUND
