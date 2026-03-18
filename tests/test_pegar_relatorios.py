from src.projeto_acoes.pegar_relatorios import RelatorioFii, CadastroFundos
import json


def test_pegar_relatorios(db_session, fundos_teste):
    relatorios = RelatorioFii(
        db=db_session,
        sigla_fundo='GARE11',
        data_inicial='2023-01-01',
        data_final='2023-12-31',
    )
    dados = relatorios.dados_pagina_fundos()
    print(dados)
    documentos = relatorios.get_documentos()
    print(documentos)
    documento_por_tipo = relatorios.get_documento_por_tipo(
        'Rendimentos e Amortizações'
    )
    print(documento_por_tipo)
    assert dados is not None
    assert documentos is not None
    assert documento_por_tipo is not None


def test_baixar_relatorio(db_session, fundos_teste, documentos):
    relatorios = RelatorioFii(
        db=db_session,
        sigla_fundo='GARE11',
        data_inicial='2025-09-01',
        data_final='2025-09-27',
    )
    local = relatorios.baixar_documento('Informe Mensal Estruturado ')
    print(local)
    assert local is not None
