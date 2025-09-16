from httpx import Client
from src.projeto_acoes.model import FundosII, Acoes, DocumentosFII
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime


class CadastroFundos:
    def __init__(self, db: Session = None):
        self.db: Session = db

    def cadastrar_fundos(
        self,
        nome_fundo: str,
        sigla_fundo: str,
        cnpj_fundo: str,
    ):
        fundo = FundosII(nome=nome_fundo, sigla=sigla_fundo, cnpj=cnpj_fundo)
        self.db.add(fundo)
        self.db.commit()
        self.db.refresh(fundo)
        return fundo

    def get_fundos(self):
        return self.db.scalars(select(FundosII)).all()

    def get_fundo_por_sigla(self, sigla: str):
        fundo = self.db.scalar(select(FundosII).where(FundosII.sigla == sigla))
        if not fundo:
            raise ValueError(f'Fundo com sigla {sigla} não encontrado.')
        return fundo


class RelatorioFii:
    def __init__(
        self, db: Session, sigla_fundo: str, data_inicial: str, data_final: str
    ):
        self.db = db
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
            'isSession': 'true',
        }
        self.cliente = Client()

    def _tratar_resposta(self, fundo_id: int, response):
        if response.status_code != 200:
            raise Exception(f'Erro na requisição: {response.status_code}')
        else:
            dados_documentos = []
            dados = response.json()

            try:
                for item in dados.get('data', []):
                    doc_data = {
                        'id_documento': str(item.get('id')),
                        'descricao': item.get('tipoDocumento'),
                        'titulo': item.get('descricaoFundo'),
                        'data_entrega': datetime.strptime(
                            item.get('dataEntrega'), '%d/%m/%Y %H:%M'
                        ),
                    }
                    doc_data['id_sigla_fundo'] = fundo_id
                    dados_documentos.append(doc_data)
                    # Save to DB with relationship
                    documento = DocumentosFII(**doc_data)

                    self.db.merge(documento)  # Use merge to avoid duplicates
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                raise e
            finally:
                self.db.close()

            return dados_documentos

    def dados_pagina_fundos(self):
        try:
            fundos = CadastroFundos(self.db)
            fundo = fundos.get_fundo_por_sigla(sigla=self.sigla_fundo)
            self.params.update(
                {
                    'cnpj': fundo.cnpj,
                    'cnpjFundo': fundo.cnpj,
                    'dataInicio': self.data_inicial,
                    'dataFim': self.data_final,
                }
            )

            url = 'https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados'
            response = self.cliente.get(url, params=self.params)
            response.raise_for_status()

            return self._tratar_resposta(fundo_id=fundo.id, response=response)
        except ValueError as e:
            raise ValueError(f'Erro ao obter dados: {e}')
        finally:
            self.cliente.close()
            self.db.close()
