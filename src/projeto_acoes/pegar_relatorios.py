from httpx import Client
from src.projeto_acoes.database import SessionLocal, create_tables
from src.projeto_acoes.model import Documento, FundosImobiliarios


class CadastroFundos:
    def __init__(self):
        self.db = SessionLocal()
        create_tables()
        pass

    def cadastrar_fundos(
        self,
        nome_fundo: str,
        sigla_fundo: str,
        cnpj_fundo: str,
    ):
        fundo = FundosImobiliarios(
            nome=nome_fundo,
            sigla=sigla_fundo,
            cnpj=cnpj_fundo
        )
        self.db.add(fundo)
        self.db.commit()
        self.db.refresh(fundo)
        return fundo

    def get_fundos(self):
        return self.db.query(FundosImobiliarios).all()

    def get_fundo_por_sigla(self, sigla: str):
        fundo = (
            self.db.query(FundosImobiliarios)
            .filter(FundosImobiliarios.sigla == sigla)
            .first()
        )
        if not fundo:
            raise ValueError(f'Fundo com sigla {sigla} não encontrado.')
        return fundo


class RelatorioFii:
    def __init__(self, sigla_fundo: str, data_inicial: str, data_final: str):
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
        self.db = SessionLocal()
        self.cliente = Client()

    def _tratar_resposta(self, response):
        if response.status_code != 200:
            raise Exception(f'Erro na requisição: {response.status_code}')
        else:
            dados_documentos = []
            dados = response.json()

            try:
                # Get or create the fund
                fundo = self._get_or_create_fundo(self)

                for item in dados.get('data', []):
                    doc_data = {
                        'id_documento': str(item.get('id')),
                        'descricao': item.get('tipoDocumento'),
                        'fundo': item.get('descricaoFundo'),
                    }
                    dados_documentos.append(doc_data)

                    # Save to DB with relationship
                    documento = Documento(**doc_data)
                    documento.fundo_relacionado = fundo
                    self.db.merge(documento)  # Use merge to avoid duplicates
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                raise e
            finally:
                self.db.close()

            return dados_documentos

    def dados_pagina_fundos(self):
        fundos = CadastroFundos().get_fundo_por_sigla(self.sigla_fundo)
        self.params.update(
            {
                'cnpj': fundos.cnpj,
                'cnpjFundo': fundos.cnpj,
                'dataInicio': self.data_inicial,
                'dataFim': self.data_final,
            }
        )

        url = 'https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados'
        response = self.cliente.get(url, params=self.params)
        response.raise_for_status()

        return self._tratar_resposta(response)
