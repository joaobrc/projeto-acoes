from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class SchemaFundosII(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    sigla: str
    cnpj: str

    @field_validator('sigla')
    @classmethod
    def sigla_maiuscula(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator('cnpj')
    @classmethod
    def cnpj_nao_vazio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('CNPJ não pode ser vazio.')
        return v


class SchemaDocumentosFII(BaseModel):


    model_config = ConfigDict(from_attributes=True)

    id: int
    id_documento: str
    titulo: str
    tipo: str
    id_sigla_fundo: int
    data_entrega: datetime

    @field_validator('id_documento')
    @classmethod
    def id_documento_nao_vazio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('id_documento não pode ser vazio.')
        return v


class SchemaRelatorioFII(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    fundo: SchemaFundosII
    documentos: list[SchemaDocumentosFII]