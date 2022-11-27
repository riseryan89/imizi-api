from operator import or_

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db.connection import db

user = APIRouter()


@user.get("/users/{user_id}", response_model=schemas.UsersRES)
async def get_user(user_id: int, session: Session = Depends(db.session)):
    user_info = session.query(models.Users).filter_by(id=user_id).first()
    user_info = session.query(models.Users).filter((models.Users.id == user_id) | (models.Users.id == 4)).first()
    user_info = session.query(models.Users).filter(or_(models.Users.id == user_id, models.Users.id == 4)).first()
    return user_info
