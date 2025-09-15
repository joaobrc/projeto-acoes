from sqlalchemy import select

from src.projeto_acoes.model import FundosII


def test_cadastrar_fundos(db_session):
    novo_fundo = FundosII(
        nome='Fundo de Teste', sigla='TEST11', cnpj='00.000.000/0001-00'
    )
    db_session.add(novo_fundo)
    db_session.commit()
    db_session.refresh(novo_fundo)

    stmt = select(FundosII).where(FundosII.sigla == 'TEST11')
    resultado = db_session.execute(stmt).scalar_one_or_none()

    assert resultado is not None
    assert resultado.nome == 'Fundo de Teste'
    assert resultado.sigla == 'TEST11'
    assert resultado.cnpj == '00.000.000/0001-00'
