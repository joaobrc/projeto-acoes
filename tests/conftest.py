from pytest import fixture

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.projeto_acoes.model import registro_tabelas



@fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    registro_tabelas.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    registro_tabelas.metadata.drop_all(engine)
