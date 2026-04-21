from httpx import Client
from projeto_acoes.model import FundosII, DocumentosFII
from projeto_acoes.schema import (
    SchemaFundosII,
    SchemaDocumentosFII,
    SchemaRelatorioFII,
)
from config.config import get_links_config
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
import filetype


class CadastroFundos:
    def __init__(self, db: Session = None):
        self.db: Session = db


    def _get_fundo_orm(self, sigla: str) -> FundosII:

        fundo = self.db.scalar(select(FundosII).where(FundosII.sigla == sigla))
        if not fundo:
            raise ValueError(f'Fundo com sigla {sigla} não encontrado.')
        return fundo

    def _get_documento_orm(self, id: int) -> DocumentosFII:

        documento = self.db.scalar(
            select(DocumentosFII).where(DocumentosFII.id == id)
        )
        if not documento:
            raise ValueError(f'Documento com ID {id} não encontrado.')
        return documento

    def _get_documentos_fundo_orm(self, fundo_id: int) -> list[DocumentosFII]:

        return self.db.scalars(
            select(DocumentosFII).where(
                DocumentosFII.id_sigla_fundo == fundo_id
            )
        ).all()

    def cadastrar_fundos(
        self,
        nome_fundo: str,
        sigla_fundo: str,
        cnpj_fundo: str,
    ) -> SchemaFundosII:

        fundo = FundosII(nome=nome_fundo, sigla=sigla_fundo, cnpj=cnpj_fundo)
        self.db.merge(fundo)
        self.db.commit()
        self.db.refresh(fundo)
        return SchemaFundosII.model_validate(fundo)

    def get_fundos(self) -> list[SchemaFundosII]:

        fundos = self.db.scalars(select(FundosII)).all()
        return [SchemaFundosII.model_validate(f) for f in fundos]

    def get_fundo_por_sigla(self, sigla: str) -> SchemaFundosII:

        return SchemaFundosII.model_validate(self._get_fundo_orm(sigla))

    def get_documento_por_id(self, id: int) -> SchemaDocumentosFII:

        return SchemaDocumentosFII.model_validate(self._get_documento_orm(id))

    def get_documentos_por_fundo(self, fundo_id: int) -> list[SchemaDocumentosFII]:

        documentos = self._get_documentos_fundo_orm(fundo_id)
        return [SchemaDocumentosFII.model_validate(d) for d in documentos]

    def get_relatorio_fundo(self, fundo_id: int) -> str:

        fundo = self.db.scalar(select(FundosII).where(FundosII.id == fundo_id))
        if not fundo:
            raise ValueError(f'Fundo com ID {fundo_id} não encontrado.')
        documentos = self._get_documentos_fundo_orm(fundo_id)
        relatorio = SchemaRelatorioFII.model_validate(
            {'fundo': fundo, 'documentos': documentos}
        )
        return relatorio.model_dump_json(indent=4)

    def get_documentos(self) -> list[SchemaDocumentosFII]:

        documentos = self.db.scalars(select(DocumentosFII)).all()
        return [SchemaDocumentosFII.model_validate(d) for d in documentos]

    def deletar_fundo(self, sigla: str) -> None:

        fundo = self._get_fundo_orm(sigla) 
        documentos = self._get_documentos_fundo_orm(fundo.id)  
        for documento in documentos:
            self.db.delete(documento)
        self.db.delete(fundo)
        self.db.commit()



class RelatorioFii(CadastroFundos):
    def __init__(
        self, db: Session, sigla_fundo: str, data_inicial: str, data_final: str
    ):
        super().__init__(db)
        self.sigla_fundo = sigla_fundo
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.params = {
            'd': '1',
            's': '0',
            'l': '15',
            'o[0][dataEntrega]': 'desc',
            'idCategoriaDocumento': '0',
            'idTipoDocumento': '0',
            'idEspecieDocumento': '0',
            'isSession': 'false',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        }
        self.get_links = get_links_config()


    def _tratar_resposta(self, fundo_id: int, response):
        dados_documentos = []
        dados = response.json()
        try:
            for item in dados.get('data', []):
                doc_data = {
                    'id_documento': str(item.get('id')),
                    'tipo': item.get('tipoDocumento'),
                    'titulo': item.get('descricaoFundo'),
                    'data_entrega': datetime.strptime(
                        item.get('dataEntrega'), '%d/%m/%Y %H:%M'
                    ),
                }
                doc_data['id_sigla_fundo'] = fundo_id
                print(
                    f'Processando documento: {doc_data["titulo"]} ({doc_data["tipo"]})'
                )
                dados_documentos.append(doc_data)

                documento_existente = self.db.scalar(
                    select(DocumentosFII).where(
                        DocumentosFII.id_documento
                        == doc_data['id_documento']
                    )
                )

                if not documento_existente:
                    documento = DocumentosFII(**doc_data)
                    self.db.add(documento)
                    self.db.commit()
                else:
                    print(
                        f'Documento {doc_data["id_documento"]} já existe, pulando...'
                    )
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f'Erro ao obter dados: {self.sigla_fundo}') from e
        return dados_documentos

    def dados_pagina_fundos(self):
        
        with Client(timeout=None, headers=self.headers, follow_redirects=True) as cliente:
            abrir_gerenciador = self.get_links.get_fnet_cookies()
            cliente.get(abrir_gerenciador)
            fundo = self._get_fundo_orm(sigla=self.sigla_fundo)  # ORM: precisa de .cnpj e .id
            data_inicio_fmt = self.data_inicial.strftime('%Y-%m-%d') if hasattr(self.data_inicial, 'strftime') else self.data_inicial
            data_fim_fmt = self.data_final.strftime('%Y-%m-%d') if hasattr(self.data_final, 'strftime') else self.data_final

            self.params.update(
                {
                    'cnpj': fundo.cnpj,
                    'cnpjFundo': fundo.cnpj,
                    'dataInicio': data_inicio_fmt,
                    'dataFim': data_fim_fmt,
                }
            )

            url = self.get_links.get_fnet_consulta_url()
            response = cliente.get(url, params=self.params)
            response.raise_for_status()
        return self._tratar_resposta(fundo_id=fundo.id, response=response)

    def baixar_documento(self, id: int) -> str:
        documento = self._get_documento_orm(id=id)  # ORM: precisa de .id_documento e .tipo
        url_download = self.get_links.get_fnet_download_url()
        params = {'id': documento.id_documento}

        with Client(timeout=None, headers=self.headers, follow_redirects=True) as cliente:
            abrir_gerenciiador = self.get_links.get_fnet_cookies()
            cliente.get(abrir_gerenciiador)
            response = cliente.get(url_download, params=params)
            response.raise_for_status()
            dados = response.content
            file_type = filetype.guess(dados)
            if not file_type:
                file_type = ('xml')
            else:
                file_type = file_type.extension
            filename = f'{self.sigla_fundo}_{documento.tipo.replace(" ", "_")}.{file_type}'
            with open(filename, 'wb') as file:
                file.write(dados)
            return filename

