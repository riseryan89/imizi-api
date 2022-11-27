from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Users(Base):
    __tablename__ = "users"
    email = Column(String(64), nullable=False)
    pw = Column(String(256), nullable=False)
    api_keys = relationship("APIKeys", back_populates="users")


class APIKeys(Base):
    __tablename__ = "users_api_keys"
    user_id = Column(ForeignKey("users.id"), nullable=False)
    access_key = Column(String(64), nullable=False)
    secret_key = Column(String(64), nullable=False)
    whitelist_ips = Column(String(256), nullable=False)
    users = relationship("Users", back_populates="api_keys")
