from src.projeto_acoes.pegar_relatorios import RelatorioFii
import json


def test_pegar_relatorios(db_session, fundos_teste):
    relatorios = RelatorioFii(
        db=db_session,
        sigla_fundo='GARE11',
        data_inicial='2023-01-01',
        data_final='2023-12-31',
    )
    relatorios = relatorios.dados_pagina_fundos()
    print(relatorios)
    assert relatorios is not None


def test_baxar_relatorio():
    ...