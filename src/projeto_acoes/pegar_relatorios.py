from httpx import Client


class RelatorioFii:
    def __init__(self, sigla_fundo: str, data_inicial: str, data_final: str):
        self.sigla_fundo = sigla_fundo
        self.data_inicial = data_inicial
        self.data_final = data_final

    def __repr__(self):
        return f'RelatorioFii(sigla_fundo={self.sigla_fundo}, data_inicial={self.data_inicial}, data_final={self.data_final})'
