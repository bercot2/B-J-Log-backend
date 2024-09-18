from typing import List

from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.exceptions.exceptions import ExceptionNoDataFound

db = SQLAlchemy()
migrate = Migrate()


class ModelBase(db.Model):
    __abstract__ = True

    @classmethod
    def get_schema(cls, fields: List[str] = None):
        """Retorna o schema Marshmallow associado ao modelo"""

        class ModelSchema(SQLAlchemyAutoSchema):
            class Meta:
                model = cls
                load_instance = True
                include_fk = True

        if fields:
            return ModelSchema(only=fields)

        return ModelSchema()


class Model:
    @staticmethod
    def set_model(model: ModelBase):
        g.model = model

    @staticmethod
    def get_schema(fields: List[str] = None) -> ModelBase:
        model: ModelBase = g.get("model", None)

        if model:
            return model.get_schema(fields)


class Query:
    @staticmethod
    def set_query(query):
        g.query = query

    @staticmethod
    def get_queryset():
        return g.get("query", None)


class DynamicSchema:

    @staticmethod
    def get(query):
        """
        Cria um schema dinâmico com base nas colunas retornadas por uma consulta SQLAlchemy.
        """
        # Executa a consulta para obter o primeiro resultado e inspecionar as colunas
        first_result = query.limit(1).all()
        if not first_result:
            raise ExceptionNoDataFound()

        # Usa o primeiro resultado para inferir os campos
        first_item = first_result[0]

        # Cria um dicionário para armazenar os campos do schema
        fields_dict = {}

        for column_name in first_item.__table__.columns.keys():
            column_value = getattr(first_item, column_name)

            # Determina o tipo de campo para o Marshmallow
            if isinstance(column_value, int):
                field_type = fields.Int()
            elif isinstance(column_value, float):
                field_type = fields.Float()
            elif isinstance(column_value, str):
                field_type = fields.Str()
            elif isinstance(column_value, bool):
                field_type = fields.Bool()
            elif isinstance(column_value, bytes):
                field_type = fields.Raw()
            elif isinstance(column_value, list):
                field_type = fields.List(fields.Raw())
            elif isinstance(column_value, dict):
                field_type = fields.Dict(keys=fields.Str(), values=fields.Raw())
            else:
                field_type = fields.Raw()  # Tipo genérico para tipos não mapeados

            fields_dict[column_name] = field_type

        # Cria e retorna o schema dinâmico
        DynamicSchemaFromQuery = type("DynamicSchemaFromQuery", (Schema,), fields_dict)

        return DynamicSchemaFromQuery()
