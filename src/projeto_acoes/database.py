from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# SQLite database URL
DATABASE_URL = 'sqlite:///projeto_acoes.db'

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session


def get_db():
    with Session(engine) as db:
        yield db
