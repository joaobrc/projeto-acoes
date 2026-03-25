from sqlalchemy import create_engine
from config.config import get_links_config
from sqlalchemy.orm import Session

# SQLite database URL
DATABASE_URL = get_links_config().get_uri_db()

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session


def get_db():
    with Session(engine) as db:
        yield db
