from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import settings as config

engine = create_engine(
    config.settings.DATABASE_URL,
    client_encoding="utf8",
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
