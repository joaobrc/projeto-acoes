from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Base

# SQLite database URL
DATABASE_URL = "sqlite:///projeto_acoes.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
