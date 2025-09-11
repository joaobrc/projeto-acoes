from sqlalchemy.orm import Mapped, registry


registro_tabelas = registry()

@registro_tabelas.mapped_as_dataclass
class FundosII:
    
    __tablename__ = 'fundos_imobiliarios'
    
    id: Mapped[int] = registro_tabelas.mapped_column(primary_key=True)
    nome: Mapped[str]
    sigla: Mapped[str] = registro_tabelas.mapped_column(unique=True)
    cnpj: Mapped[str]
    
    def __repr__(self):
        return f"<FundoImobiliario(nome='{self.nome}', sigla='{self.sigla}', cnpj='{self.cnpj}')>"


@registro_tabelas.mapped_as_dataclass
class Acoes:
    
    __tablename__ = 'acoes'
    
    id: Mapped[int] = registro_tabelas.mapped_column(primary_key=True)
    nome: Mapped[str]
    sigla: Mapped[str] = registro_tabelas.mapped_column(unique=True)
    cnpj: Mapped[str]

    def __repr__(self):
        return f"<Acao(nome='{self.nome}', sigla='{self.sigla}', cnpj='{self.cnpj}')>"


@registro_tabelas.mapped_as_dataclass
class Documentos:
    
    __tablename__ = 'documentos'
    
    id: Mapped[int] = registro_tabelas.mapped_column(primary_key=True)
    id_documento: Mapped[str] = registro_tabelas.mapped_column(unique=True)
    titulo: Mapped[str]
    sigla: Mapped[str]
    id_sigla_fundo: Mapped[int] = registro_tabelas.mapped_column(
        registro_tabelas.ForeignKey('fundos_imobiliarios.id')
    )
    id_sigla_acao: Mapped[int] = registro_tabelas.mapped_column(
        registro_tabelas.ForeignKey('acoes.id')
    )
    dada_entrega: Mapped[str]
    
