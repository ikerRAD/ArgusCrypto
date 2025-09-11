from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


from app.domain.crypto.models import *  # noqa: F401
from app.domain.exchange.models import *  # noqa: F401
