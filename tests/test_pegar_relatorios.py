from src.projeto_acoes.pegar_relatorios import RelatorioFii


def test_pegar_relatorios():
    relatorios = RelatorioFii(
        sigla_fundo='GARE11',
        data_inicial='2023-01-01',
        data_final='2023-12-31',
    )

    assert relatorios is not None
