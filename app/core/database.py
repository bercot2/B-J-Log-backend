from typing import List

from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import fields

from app.core.schemas import DynamicModelSchema
from app.exceptions.exceptions import ExceptionNotFoundModelG

db = SQLAlchemy()
migrate = Migrate()


class ModelBase(db.Model):
    __abstract__ = True

    @classmethod
    def get_schema(cls, fields_list: List[str] = None, **kwargs):
        """Retorna o schema Marshmallow associado ao modelo"""

        class ModelSchema(DynamicModelSchema):
            def get_schema_only_fields(self, fields):
                fields = list(
                    filter(lambda field: self.fields.get(field.strip()), fields)
                )

                if fields:
                    return self.__class__(only=fields)

                return self

            class Meta:
                model = cls
                load_instance = True
                include_fk = True

        schema_instance = (
            ModelSchema(only=fields_list) if fields_list else ModelSchema()
        )

        for name_key, schema in kwargs.items():
            if schema:
                schema_instance.fields[name_key] = fields.Nested(schema)

        return schema_instance

    def insert(self):
        db.session.add(self)
        db.session.commit()

        return self


class Model:
    @staticmethod
    def set_model(model: ModelBase):
        g.model = model

    @staticmethod
    def get_model():
        model = g.get("model", None)

        if model:
            return model

        raise ExceptionNotFoundModelG

    @staticmethod
    def get_schema(fields_list: List[str] = None, **kwargs) -> ModelBase:
        model: ModelBase = g.get("model", None)

        if model:
            return model.get_schema(fields_list, **kwargs)


class Query:
    @staticmethod
    def set_query(query):
        g.query = query

    @staticmethod
    def get_queryset():
        return g.get("query", None)
