from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import uuid4
from app import models, schemas
from app.db.connection import db
from app.depends.validate_api_key import validate_api_key
from app.schemas.image_schemas import UploadImageREQ
from app.utils.image_utils import get_image_size, resize_image, get_image_extension, get_squared_thumbnail

image = APIRouter()


@image.post("/upload")
def upload_image(
    body: schemas.UploadImageREQ,
    image_group_id: int,
    session: Session = Depends(db.session),
    # valid_key: bool = Depends(validate_api_key),
):
    """
    :param body:
    :param session:
    :param valid_key:
    :return:
    """
    image_convert_size = [512, 1024, 1980]
    image_size = get_image_size(body.image)
    image_extension = get_image_extension(body.image)
    uuid = str(uuid4())
    thumbnail, file_size = get_squared_thumbnail(body.image)
    images = {}
    total_size = file_size

    for size in image_convert_size:
        if image_size[0] > size:
            resized_image, file_size = resize_image(body.image, size)
            total_size += file_size
            images[size] = resized_image
            print(file_size)
            print(image_extension)


@image.get("/{image_id}")
def get_image(request: Request, image_id: int, session: Session = Depends(db.session)):
    if request.state.user:
        return {"message": "success"}
    return {"message": "failed"}
