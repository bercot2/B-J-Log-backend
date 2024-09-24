from typing import List
from sqlalchemy import Boolean, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload
from app.core.database import ModelBase


class Usuario(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    empresas: Mapped[List["Empresa"]] = relationship(
        "Empresa", secondary="usuario_empresa", back_populates="usuarios"
    )

    @staticmethod
    def get_user_empresa(**kwargs):
        query = Usuario.query.select_from(Usuario).options(joinedload(Usuario.empresas))

        return query


class Empresa(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cnpj: Mapped[str] = mapped_column(String(14), nullable=False)
    razao_social: Mapped[str] = mapped_column(String(200), nullable=False)
    nome_fantasia: Mapped[str] = mapped_column(String(200), nullable=True)
    inscricao_estadual: Mapped[str] = mapped_column(String(20), nullable=True)
    inscricao_municipal: Mapped[str] = mapped_column(String(20), nullable=True)
    setor_atividade: Mapped[str] = mapped_column(String(100), nullable=True)
    data_fundacao: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    logotipo: Mapped[str] = mapped_column(String(255), nullable=True)
    observacoes: Mapped[str] = mapped_column(Text, nullable=True)

    id_matriz: Mapped[int] = mapped_column(ForeignKey("empresa.id"), nullable=True)
    id_regime_tributario: Mapped[int] = mapped_column(
        ForeignKey("regime_tributario.id"), nullable=False
    )

    enderecos: Mapped[List["EmpresaEndereco"]] = relationship(
        "EmpresaEndereco", back_populates="empresa"
    )

    contatos: Mapped[List["EmpresaContato"]] = relationship(
        "EmpresaContato", back_populates="empresa"
    )

    usuarios: Mapped[List["Usuario"]] = relationship(
        "Usuario", secondary="usuario_empresa", back_populates="empresas"
    )


class RegimeTributario(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    descricao: Mapped[str] = mapped_column(String(50), nullable=False)


class Contato(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    contato_principal: Mapped[str] = mapped_column(String(200), nullable=False)

    empresas: Mapped[List["EmpresaContato"]] = relationship(
        "EmpresaContato", back_populates="contato"
    )


class Endereco(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    logradouro: Mapped[str] = mapped_column(String(255), nullable=False)
    numero: Mapped[str] = mapped_column(String(10), nullable=False)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)
    cep: Mapped[str] = mapped_column(String(8), nullable=False)

    empresas: Mapped[List["EmpresaEndereco"]] = relationship(
        "EmpresaEndereco", back_populates="endereco"
    )


class EmpresaEndereco(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_empresa: Mapped[int] = mapped_column(ForeignKey("empresa.id"))
    id_endereco: Mapped[int] = mapped_column(ForeignKey("endereco.id"))

    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="enderecos")
    endereco: Mapped["Endereco"] = relationship("Endereco", back_populates="empresas")


class EmpresaContato(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_empresa: Mapped[int] = mapped_column(ForeignKey("empresa.id"))
    id_contato: Mapped[int] = mapped_column(ForeignKey("contato.id"))

    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="contatos")
    contato: Mapped["Contato"] = relationship("Contato", back_populates="empresas")


class UsuarioEmpresa(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_empresa: Mapped[int] = mapped_column(ForeignKey("empresa.id"))
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
