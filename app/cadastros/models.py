from sqlalchemy import Boolean, DateTime, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import ModelBase


class Usuario(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
