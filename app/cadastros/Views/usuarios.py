from http import HTTPStatus
from flask import Blueprint
from app.core.database import Model, Query
from app.core.decorators import filter_fields
from app.core.responses import AppResponse
from app.serializer import Serializer
from ..models import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuario')


@usuarios_bp.get("/")
@filter_fields(Usuario, "__all__")
def get_usuarios():
    serializer = Serializer.transform(Model.get_schema(), Query.get_queryset())

    return AppResponse(serializer), HTTPStatus.OK
