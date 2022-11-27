from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.connection import db
from app.utils.auth_utils import is_valid_password, decode_token

user = APIRouter()


@user.post("/register", response_model=schemas.UsersRES)
async def register(data: schemas.UsersREQ, session: Session = Depends(db.session)):
    u = models.Users(email=data.email, pw=data.pw)
    if models.Users.get_by_email(session, data.email):
        raise ValueError("이미 존재하는 이메일입니다.")
    session.add(u)
    session.commit()
    return u


@user.post("/get-token", response_model=schemas.Token)
async def get_token(data: schemas.UsersREQ, session: Session = Depends(db.session)):
    u = models.Users.get_by_email(session, data.email)
    if not u:
        raise ValueError("존재하지 않는 이메일입니다.")
    if not is_valid_password(data.pw, u.pw):
        raise ValueError("비밀번호가 일치하지 않습니다.")
    return u.get_token()


@user.post("/refresh", response_model=schemas.Token)
async def refresh_token(data: schemas.RefreshToken, session: Session = Depends(db.session)):
    refresh_payload = decode_token(data.refresh_token)
    u = session.query(models.Users).filter_by(id=refresh_payload["id"]).first()
    return u.token_refresh(data.refresh_token)


@user.post("/api-keys", response_model=schemas.APIKeysExtendRES)
async def create_api_key(user_id: int, session: Session = Depends(db.session)):
    u = session.query(models.Users).filter_by(id=user_id).first()
    if not u:
        raise ValueError("존재하지 않는 유저입니다.")
    api_key = models.APIKeys(user_id=user_id)
    api_key.add(session)
    return api_key
