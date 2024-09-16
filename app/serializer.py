from collections import OrderedDict
from sqlalchemy.orm import class_mapper
from flask import request

from app.exceptions.exceptions import ExceptionNoDataFound


class Serializer:

    def __init__(self, query, page=0, per_page=0) -> None:
        self.query = query
        self.page = page
        self.per_page = per_page

    def model_to_dict(self, model):
        """Converte um objeto SQLAlchemy em um dicionário."""
        class_model = type(model)

        columns = ["id"] + [
            c.key for c in class_mapper(class_model).columns if c.key != "id"
        ]
        return OrderedDict((c, getattr(model, c)) for c in columns)

    def is_paginate(self):
        self.page = int(request.args.get("page", 0))
        self.per_page = int(request.args.get("per_page", 0))

        if self.page > 0 and self.per_page > 0:
            return True

        return False

    def serialize(self):
        if self.query.count() > 1:
            return [self.model_to_dict(model) for model in self.query.all()]
        else:
            return self.model_to_dict(self.query.first())

    def paginate(self):
        paginated_query = self.query.paginate(
            page=self.page, per_page=self.per_page, error_out=False
        )

        serializer = [self.model_to_dict(model) for model in paginated_query.items]

        response = {
            "page": paginated_query.page,
            "per_page": paginated_query.per_page,
            "total_pages": paginated_query.pages,
            "total_items": paginated_query.total,
            "items": serializer,
        }

        return response

    @classmethod
    def transform(cls, query):
        if query.count() == 0:
            raise ExceptionNoDataFound()

        serializer = cls(query)

        if serializer.is_paginate():
            return serializer.paginate()

        return serializer.serialize()
