import uuid
import secrets

from sqlalchemy import Boolean, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import ModelBase
from app.exceptions.exceptions import ExceptionNotFoundAuthentication


class Authentication(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    chave_acesso: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, default=str(uuid.uuid4())
    )
    secret_key: Mapped[str] = mapped_column(
        String, nullable=False, default=secrets.token_urlsafe(64)
    )
    pode_gerar_token: Mapped[bool] = mapped_column(Boolean, default=True)

    @classmethod
    def get_authentication(cls, nome, chave_acesso):
        authentication = cls.query.filter(
            func.upper(cls.nome) == nome.upper(), cls.chave_acesso == chave_acesso
        ).first()

        if authentication:
            return authentication

        raise ExceptionNotFoundAuthentication()
