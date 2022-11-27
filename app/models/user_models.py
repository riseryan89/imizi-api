import enum
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, Session

from app.models.base_model import Base
from app.utils.auth_utils import hash_password, create_token, decode_token
from config import get_env


class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class Users(Base):
    __tablename__ = "users"
    email = Column(String(64), nullable=False)
    pw = Column(String(256), nullable=False)
    status = Column(Enum(UserStatus, native_enum=False, length=50), nullable=False, default=UserStatus.ACTIVE)
    payplan_id = Column(ForeignKey("users_pay_plans.id"), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    api_keys = relationship("APIKeys", back_populates="users")
    pay_plans = relationship("UserPayPlans", backref="users")

    def __init__(self, email, pw, payplan_id=None, is_admin=False):
        self.email = email
        self.pw = hash_password(pw)
        self.payplan_id = payplan_id if payplan_id else 1
        self.is_admin = is_admin

    @classmethod
    def get(cls, session: Session, id: int = None, **kwargs):
        if id:
            return session.query(cls).filter_by(id=id, **kwargs).first()
        return session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_by_email(cls, session: Session, email: str):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def update(cls, session: Session, id: int, **kwargs):
        session.query(cls).filter_by(id=id).update(kwargs)
        session.commit()

    def get_token(self):
        return {
            "access_token": create_token(
                data=dict(id=self.id, email=self.email, staff=self.is_admin),
                delta=get_env().ACCESS_TOKEN_EXPIRE_MINUTES,
            ),
            "refresh_token": create_token(
                data=dict(id=self.id),
                delta=get_env().REFRESH_TOKEN_EXPIRE_MINUTES,
            ),
        }

    def token_refresh(self, refresh_token: str):
        refresh_payload = decode_token(refresh_token)
        now = int(datetime.utcnow().timestamp())
        if now - refresh_payload["iat"] < get_env().REFRESH_TOKEN_EXPIRE_MINUTES * 60 / 2:
            return {
                "access_token": create_token(
                    data=dict(id=self.id, email=self.email, staff=self.is_admin),
                    delta=get_env().ACCESS_TOKEN_EXPIRE_MINUTES,
                ),
                "refresh_token": refresh_token,
            }
        else:
            return self.get_token()


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


class UserPayPlans(Base):
    __tablename__ = "users_pay_plans"
    name = Column(String(64), nullable=False)
    price = Column(Integer, nullable=False)
    max_image_count = Column(Integer, nullable=False)
    max_image_size = Column(Integer, nullable=False)
    max_image_group_count = Column(Integer, nullable=False)
