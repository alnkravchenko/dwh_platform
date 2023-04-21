from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
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


def create_entity(db: Session, entity: Base) -> Base:
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity
