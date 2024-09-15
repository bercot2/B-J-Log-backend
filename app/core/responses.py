import json

from collections import OrderedDict
from typing import List
from flask import Response


class AppResponse(Response):
    def __init__(
        self, object: List[OrderedDict] | OrderedDict, *args, **kwargs
    ) -> None:
        mimetype = "application/json"
        json_data = json.dumps(object, ensure_ascii=False)

        super().__init__(json_data, mimetype=mimetype, *args, **kwargs)
