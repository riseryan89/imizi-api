# create user api endpoints
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db.connection import db
from app.schemas import UsersREQ

user = APIRouter()


@user.post("/users", response_model=schemas.UsersRES)
async def create_user(data: UsersREQ, session: Session = Depends(db.session)):
    user_model = models.Users(**data.dict())
    session.add(user_model)
    session.commit()
    return user_model


@user.get("/users/{user_id}", response_model=schemas.UsersRES)
async def get_user(user_id: int, session: Session = Depends(db.session)):
    user_info = session.query(models.Users).filter_by(id=user_id).first()
    return user_info


@user.patch("/users/{user_id}", response_model=schemas.UsersRES)
async def update_user(user_id: int, session: Session = Depends(db.session)):
    session.query(models.Users).filter_by(id=user_id).update({"email": "sdfdsfsd@dlsdkf.com"})
    session.commit()
    return await get_user(user_id=user_id, session=session)


@user.delete("/users/{user_id}", response_model=schemas.Message)
async def delete_user(user_id: int, session: Session = Depends(db.session)):
    session.query(models.Users).filter_by(id=user_id).delete()
    session.commit()
    return schemas.Message()


@user.post("/users/{user_id}/api_keys", response_model=schemas.APIKeysExtendRES)
async def create_user_api_key(user_id: int, session: Session = Depends(db.session)):
    api_key = models.APIKeys(access_key="abcdefg1234", secret_key="xyz1234", user_id=user_id)
    session.add(api_key)
    session.commit()
    return api_key


@user.delete("/users/{user_id}/api_keys{key_id}", response_model=schemas.Message)
async def delete_user_api_key(user_id: int, key_id: int, session: Session = Depends(db.session)):
    session.query(models.APIKeys).filter_by(id=key_id, user_id=user_id).delete()
    session.commit()
    return schemas.Message()
