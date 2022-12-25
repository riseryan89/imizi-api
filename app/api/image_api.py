from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.connection import db
from app.depends.validate_api_key import validate_api_key

image = APIRouter()


@image.post("/image")
def upload_image(
        session: Session = Depends(db.session),
        valid_key: bool = Depends(validate_api_key)
):
    if valid_key:
        return {"message": "success"}
    return {"message": "failed"}
