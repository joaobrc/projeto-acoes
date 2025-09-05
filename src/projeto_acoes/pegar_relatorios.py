from httpx import Client
from bs4 import BeautifulSoup


class RelatorioFii:
    def __init__(self, sigla_fundo: str, data_inicial: str, data_final: str):
        self.sigla_fundo = sigla_fundo
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.cliente = Client()

    def __repr__(self):
        return f'RelatorioFii(sigla_fundo={self.sigla_fundo}, data_inicial={self.data_inicial}, data_final={self.data_final})'

    def dados_pagina_fundos(self):
        fundos = {'GARE11': '37295919000160'}
        url = f'https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM?cnpjFundo={fundos.get(self.sigla_fundo)}'
        response = self.cliente.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Aqui você pode adicionar a lógica para extrair os dados desejados da página
        return soup.prettify()
