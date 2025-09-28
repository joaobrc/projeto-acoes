from pytest import fixture

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.projeto_acoes.model import registro_tabelas, FundosII
from src.projeto_acoes.pegar_relatorios import RelatorioFii


@fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    registro_tabelas.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    registro_tabelas.metadata.drop_all(engine)
    engine.dispose()


@fixture
def fundos_teste(db_session):
    fundo = FundosII(
        nome='GUARDIAN REAL ESTATE', sigla='GARE11', cnpj='37.295.919/0001-60'
    )
    db_session.add(fundo)
    db_session.commit()
    db_session.refresh(fundo)
    fundo = FundosII(
        nome='HOSPITAL NOSSA SENHORA DE LOURDES',
        sigla='NSLU11',
        cnpj='08.014.513/0001-63',
    )
    db_session.add(fundo)
    db_session.commit()
    db_session.refresh(fundo)
    return fundo


@fixture
def documentos(db_session):
    relatorios = RelatorioFii(
        db=db_session,
        sigla_fundo='GARE11',
        data_inicial='2025-09-01',
        data_final='2025-09-27',
    )
    relatorios.dados_pagina_fundos()
