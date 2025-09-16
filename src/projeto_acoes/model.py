from sqlalchemy.orm import Mapped, registry, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime

registro_tabelas = registry()


@registro_tabelas.mapped_as_dataclass
class FundosII:
    __tablename__ = 'fundos_imobiliarios'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    nome: Mapped[str]
    sigla: Mapped[str] = mapped_column(unique=True)
    cnpj: Mapped[str]

    def __repr__(self):
        return f"<FundoImobiliario(nome='{self.nome}', sigla='{self.sigla}', cnpj='{self.cnpj}')>"


@registro_tabelas.mapped_as_dataclass
class Acoes:
    __tablename__ = 'acoes'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    nome: Mapped[str]
    sigla: Mapped[str] = mapped_column(unique=True)
    cnpj: Mapped[str]

    def __repr__(self):
        return f"<Acao(nome='{self.nome}', sigla='{self.sigla}', cnpj='{self.cnpj}')>"


@registro_tabelas.mapped_as_dataclass
class DocumentosFII:
    __tablename__ = 'documentos'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    id_documento: Mapped[str] = mapped_column(unique=True)
    titulo: Mapped[str]
    descricao: Mapped[str]
    id_sigla_fundo: Mapped[int] = mapped_column(
        ForeignKey('fundos_imobiliarios.id'), nullable=True
    )
    data_entrega: Mapped[datetime]
