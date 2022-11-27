from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.connection import db
from app.schemas import UsersREQ

user = APIRouter()


@user.post("/register", response_model=schemas.UsersRES)
async def register(data: UsersREQ, session: Session = Depends(db.session)):
    u = models.Users(email=data.email, pw=data.pw)
    if models.Users.get_by_email(session, data.email):
        raise ValueError("이미 존재하는 이메일입니다.")
    session.add(u)
    session.commit()
    return u
