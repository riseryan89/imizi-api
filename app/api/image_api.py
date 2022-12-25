from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app import models, schemas
from app.db.connection import db
from app.depends.validate_api_key import validate_api_key

image = APIRouter()


@image.post("/upload")
def upload_image(session: Session = Depends(db.session), valid_key: bool = Depends(validate_api_key)):
    if valid_key:
        return {"message": "success"}
    return {"message": "failed"}


@image.get("/{image_id}")
def get_image(request: Request, image_id: int, session: Session = Depends(db.session)):
    if request.state.user:
        return {"message": "success"}
    return {"message": "failed"}
