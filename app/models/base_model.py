from datetime import datetime

from sqlalchemy import Column, BIGINT, DateTime
from sqlalchemy.orm import as_declarative

from config import settings


@as_declarative()
class Base:
    if settings.TEST_MODE:
        __table_args__ = {"schema": "imz_test"}
    else:
        __table_args__ = {"schema": "imizi"}

    id = Column(BIGINT, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

