from src.projeto_acoes.pegar_relatorios import RelatorioFii
import json


def test_pegar_relatorios():
    relatorios = RelatorioFii(
        sigla_fundo='GARE11',
        data_inicial='2023-01-01',
        data_final='2023-12-31',
    )
    relatorios = relatorios.dados_pagina_fundos()
    print(json.dumps(relatorios, indent=2, ensure_ascii=False))
    assert relatorios is not None
