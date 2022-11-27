from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.connection import db

image = APIRouter()


@image.post("/image")
def upload_image(ts: int, api_key: str, signature: str, session: Session = Depends(db.session)):
    is_valid = models.APIKeys.validate_signature(api_key, ts, signature, session)
    print(is_valid)
    if is_valid:
        return {"message": "success"}
    return {"message": "failed"}
