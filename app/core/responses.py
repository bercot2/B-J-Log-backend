import json

from collections import OrderedDict
from typing import List
from flask import Response

from app.serializer import Serializer


class AppResponse(Response):

    def __init__(
        self, object: List[OrderedDict] | OrderedDict | Serializer, *args, **kwargs
    ) -> None:
        mimetype = "application/json"

        if isinstance(object, Serializer):
            object = object.serialize()

        json_data = json.dumps(object, ensure_ascii=False)

        super().__init__(json_data, mimetype=mimetype, *args, **kwargs)
