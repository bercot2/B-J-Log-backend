from http import HTTPStatus

from flask import jsonify


class ExceptionBase(Exception):
    def __init__(
        self,
        message="Erro interno no servidor",
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
        *args: object
    ) -> None:
        self.message = message
        self.status_code = status_code

        super().__init__(*args)

    def return_exception(self):
        return jsonify({"error": self.message}), self.status_code


class ExceptionNoDataFound(ExceptionBase):
    """Exceção levantada quando nenhum dado é encontrado na consulta."""

    def __init__(
        self,
        message="Dados não encontrados",
        status_code: HTTPStatus = HTTPStatus.NOT_FOUND,
        *args: object
    ):
        super().__init__(message, status_code, *args)


class ExceptionBadRequest(ExceptionBase):
    """Exceção levantada quando ocorre um erro no request da transação."""

    def __init__(
        self,
        message="Erro na requisição",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
        *args: object
    ):
        super().__init__(message, status_code, *args)


class ExceptionNotFoundAuthentication(ExceptionBase):
    """Exceção levantada quando Token enviado não é encontrado no banco de dados"""

    def __init__(
        self,
        message="Chave de Acesso inválido ou não identificado no banco de dados",
        status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED,
        *args: object
    ):
        super().__init__(message, status_code, *args)


class ExceptionNotFoundModelG(ExceptionBase):
    """Exceção levantada quando o Model na variável G do Flask não é encontrada"""

    def __init__(
        self,
        message="Model não encontrado!",
        status_code: HTTPStatus = HTTPStatus.NOT_FOUND,
        *args: object
    ):
        super().__init__(message, status_code, *args)


class ExceptionSerializer(ExceptionBase):
    """Exceção levantada referente aos erros no serializer"""

    def __init__(
        self,
        message=None,
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
        *args: object
    ):
        super().__init__(message, status_code, *args)
