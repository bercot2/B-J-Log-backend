from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from ..core.database import ModelBase


class TokenAcesso(ModelBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(255), unique=True, nullable=False)
    descricao = Column(String(255), nullable=True)
    data_criacao = Column(DateTime, default=func.now())
    data_expiracao = Column(DateTime, nullable=True)
    ativo = Column(Boolean, default=True)

    id_terceiro = Column(Integer, ForeignKey("terceiros_integracao.id"), nullable=False)


class TerceirosIntegracao(ModelBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False)
