from flask import request

from app.exceptions.exceptions import ExceptionNoDataFound


class Serializer:

    def __init__(self, schema, query, page=0, per_page=0) -> None:
        self.schema = schema
        self.query = query
        self.page = page
        self.per_page = per_page

    def is_paginate(self):
        self.page = int(request.args.get("page", 0))
        self.per_page = int(request.args.get("per_page", 0))

        return self.page > 0 and self.per_page > 0

    def serialize(self):
        if self.query.count() > 1:
            return self.schema.dump(self.query.all(), many=True)
        else:
            first_item = self.query.first()
            if first_item is None:
                raise ExceptionNoDataFound()
            return self.schema.dump(self.query.first())

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
    def transform(cls, schema, query):
        if not schema:
            raise ValueError("Schema é um parâmetro obrigatório")

        if not query:
            raise ValueError("Query é um parâmetro obrigatório")

        if query.count() == 0:
            raise ExceptionNoDataFound()

        serializer = cls(schema, query)

        if serializer.is_paginate():
            return serializer.paginate()

        return serializer.serialize()
