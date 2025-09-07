from httpx import Client


class RelatorioFii:
    def __init__(self, sigla_fundo: str, data_inicial: str, data_final: str):
        self.sigla_fundo = sigla_fundo
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.cliente = Client()

    def __repr__(self):
        return f'RelatorioFii(sigla_fundo={self.sigla_fundo}, data_inicial={self.data_inicial}, data_final={self.data_final})'

    def dados_pagina_fundos(self):
        params = {
            'd': '1',
            's': '0',
            'l': '15',
            'o[0][dataEntrega]': 'desc',
            'idCategoriaDocumento': '0',
            'idTipoDocumento': '0',
            'idEspecieDocumento': '0',
            'isSession': 'true',
            'cnpj': '45188176000157',
            'cnpjFundo': '45188176000157',
        }

        url = 'https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados'
        response = self.cliente.get(url, params=params)
        response.raise_for_status()
        # Aqui você pode adicionar a lógica para extrair os dados desejados da página
        return response.json()
