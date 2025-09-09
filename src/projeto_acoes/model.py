from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class FundosImobiliarios(Base):
    __tablename__ = 'fundos_imobiliarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sigla = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    setor = Column(String)
    cnpj = Column(String, unique=True, nullable=False)
    data_criacao = Column(Date)

    # Relationship with documents
    documentos = relationship("Documento", back_populates="fundo_relacionado")

    def __repr__(self):
        return f"<FundoImobiliario(sigla='{self.sigla}', nome='{self.nome}', setor='{self.setor}', cnpj='{self.cnpj}', data_criacao='{self.data_criacao}')>"

class Acoes(Base):
    __tablename__ = 'acoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sigla = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    setor = Column(String)
    data_criacao = Column(Date)

    # Relationship with documents
    documentos = relationship("Documento", back_populates="acao_relacionada")

    def __repr__(self):
        return f"<Acao(sigla='{self.sigla}', nome='{self.nome}', setor='{self.setor}', data_criacao='{self.data_criacao}')>"

class Documento(Base):
    __tablename__ = 'documentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_documento = Column(String, unique=True, nullable=False)
    descricao = Column(String, nullable=False)
    fundo = Column(String, nullable=False)
    
    # Foreign keys - nullable to allow document to belong to either fund or stock
    fundo_id = Column(Integer, ForeignKey('fundos_imobiliarios.id'), nullable=True)
    acao_id = Column(Integer, ForeignKey('acoes.id'), nullable=True)
    
    # Relationships
    fundo_relacionado = relationship("FundosImobiliarios", back_populates="documentos")
    acao_relacionada = relationship("Acoes", back_populates="documentos")

    def __repr__(self):
        return f"<Documento(id_documento='{self.id_documento}', descricao='{self.descricao}', fundo='{self.fundo}')>"
