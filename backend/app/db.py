from typing import Generator

from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, create_engine
from contextlib import contextmanager

from app.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


from app.infrastructure.crypto.database.table_models import *  # noqa: F401
from app.infrastructure.exchange.database.table_models import *  # noqa: F401
