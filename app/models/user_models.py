from enum import Enum

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship, Session

from app.models.base_model import Base


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class Users(Base):
    __tablename__ = "users"
    email = Column(String(64), nullable=False)
    pw = Column(String(256), nullable=False)
    status = Column(Enum(UserStatus), native_enum=False, length=50, nullable=False)
    payplan_id = Column(ForeignKey("users_pay_plans.id"), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    api_keys = relationship("APIKeys", back_populates="users")
    pay_plans = relationship("PayPlans", backref="users")


class APIKeys(Base):
    __tablename__ = "users_api_keys"
    user_id = Column(ForeignKey("users.id"), nullable=False)
    access_key = Column(String(64), nullable=False)
    secret_key = Column(String(64), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    users = relationship("Users", back_populates="api_keys")
    whitelist = relationship("APIKeysWhitelist", backref="api_keys")


class APIKeysWhitelist(Base):
    __tablename__ = "users_api_keys_whitelist"
    api_key_id = Column(ForeignKey("users_api_keys.id"), nullable=False)
    ip = Column(String(64), nullable=False)

    @classmethod
    def has_ip(cls, api_key_id: int, ip: str, session: Session) -> bool:
        if not session.query(cls).filter_by(api_key_id=api_key_id).first():
            return True
        return session.query(cls).filter_by(ip=ip, api_key_id=api_key_id).first() is not None


class UserPayPlan(Base):
    __tablename__ = "users_pay_plans"
    name = Column(String(64), nullable=False)
    price = Column(Integer, nullable=False)
    max_image_count = Column(Integer, nullable=False)
    max_image_size = Column(Integer, nullable=False)
    max_image_group_count = Column(Integer, nullable=False)
