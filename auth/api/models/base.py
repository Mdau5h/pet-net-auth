import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    Boolean
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseMixin:
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
