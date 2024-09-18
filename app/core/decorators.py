from functools import wraps
from typing import Callable, Literal, Type
from http import HTTPStatus

from flask import request, jsonify
from sqlalchemy_filters import apply_filters

from app.core.constants_config import FIELDS_LOOKUPS, ALL_FIELDS
from app.core.database import Model, ModelBase, Query
from app.core.enums import OperatorEnum
from app.exceptions.exceptions import ExceptionBadRequest


def filter_fields(
    base_model: Type[ModelBase] | Callable, search_fields: list | Literal["__all__"]
):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):

            Model.set_model(base_model)

            query = (
                base_model.query
                if issubclass(base_model, ModelBase)
                else base_model(**kwargs)
            )

            filter_args = {
                k: v for (k, v) in request.args.items() if k.__contains__("__")
            }

            filter_spec = []

            if filter_args:
                for k, v in filter_args.items():
                    field, lookup = k.split("__")
                    if search_fields == ALL_FIELDS or field in search_fields:
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
                                "value": v if not operator_like else f"%{v}%",
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
