from functools import wraps
from typing import Callable, Literal, Type

from flask import request
from sqlalchemy_filters import apply_filters

from app.core.constants_config import FIELDS_LOOKUPS, ALL_FIELDS
from app.core.database import Model, ModelBase, Query
from app.core.enums import OperatorEnum
from app.exceptions.exceptions import ExceptionBadRequest


def queryset(
    base_model: Type[ModelBase],
    filter_fields: list | Literal["__all__"],
    override_query: Callable = None,
):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):

            Model.set_model(base_model)

            if not override_query:
                query = base_model.query
            else:
                query = override_query(**kwargs)

            filter_args = {
                key: value
                for (key, value) in request.args.items()
                if key.__contains__("__")
            }

            filter_spec = []

            if filter_args:
                for key, value in filter_args.items():
                    field, lookup = key.split("__")
                    if filter_fields == ALL_FIELDS or field in filter_fields:
                        operator_like = (
                            True
                            if FIELDS_LOOKUPS[lookup]
                            in [
                                OperatorEnum.LIKE.value,
                                OperatorEnum.ILIKE.value,
                                OperatorEnum.NOT_LIKE.value,
                            ]
                            else False
                        )

                        filter_spec.append(
                            {
                                "field": field,
                                "op": FIELDS_LOOKUPS[lookup],
                                "value": value if not operator_like else f"%{value}%",
                            }
                        )

                try:
                    filtered_query = apply_filters(query, filter_spec)
                except Exception as e:
                    raise ExceptionBadRequest(str(e))

                Query.set_query(filtered_query)
            else:
                Query.set_query(query)

            return func(*args, **kwargs)

        return decorated

    return wrapper
