from flask import request
from sqlalchemy.orm import Query
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.exceptions.exceptions import ExceptionNoDataFound, ExceptionSerializer


class Serializer:

    def __init__(self, schema=None, query=None, page=0, per_page=0, model=None) -> None:
        self.schema = schema
        self.query = query
        self.page = page
        self.per_page = per_page
        self.model = model

    def is_paginate(self):
        self.page = int(request.args.get("page", 0))
        self.per_page = int(request.args.get("per_page", 0))

        return self.page > 0 and self.per_page > 0

    def serialize(self):
        if self.model:
            return self.model.get_schema().dump(self.model)

        first_item = self.query.first()

        if first_item is None:
            raise ExceptionNoDataFound()

        if self.query.limit(2).count() > 1:
            return self.schema.dump(self.query.all(), many=True)

        return self.schema.dump(first_item, many=False)

    def paginate(self):
        paginated_query = self.query.paginate(
            page=self.page, per_page=self.per_page, error_out=False
        )

        serializer = self.schema.dump(paginated_query.items, many=True)

        response = {
            "page": paginated_query.page,
            "per_page": paginated_query.per_page,
            "total_pages": paginated_query.pages,
            "total_items": paginated_query.total,
            "items": serializer,
        }

        return response

    @classmethod
    def transform(cls, schema: SQLAlchemyAutoSchema, query: Query):
        if not schema:
            raise ExceptionSerializer(message="Schema é um parâmetro obrigatório")

        if not query:
            raise ExceptionSerializer(message="Query é um parâmetro obrigatório")

        if query.count() == 0:
            raise ExceptionNoDataFound()

        if request.args.get("fields", None):
            schema = schema.get_schema_only_fields(
                request.args.get("fields").split(",")
            )

        serializer = cls(schema, query)

        if serializer.is_paginate():
            return serializer.paginate()

        return serializer.serialize()
