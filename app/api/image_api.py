import asyncio
import time

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import uuid4
from app import models, schemas
from app.db.connection import db
from app.depends.validate_api_key import validate_api_key
from app.utils.image_utils import get_image_size, resize_image, get_image_extension, get_squared_thumbnail, s3_upload

image = APIRouter()


@image.post("/upload", response_model=schemas.ImageInfoRES)
async def upload_image(
    request: Request,
    body: schemas.UploadImageREQ,
    image_group_id: int,
    session: Session = Depends(db.session),
    _=Depends(validate_api_key),
):
    image_group = models.ImageGroups.get(session, request.state.user.id, image_group_id)

    if not image_group:
        raise ValueError("image group not found")
    image_convert_size = [512, 1024, 1920]
    image_size = get_image_size(body.image_base64)
    image_extension = get_image_extension(body.image_base64)
    uuid = str(uuid4())
    thumbnail, file_size = get_squared_thumbnail(body.image_base64)

    images = {"thumbnail": thumbnail}
    total_size = file_size

    for size in image_convert_size:
        if image_size[0] > size:
            resized_image, file_size = resize_image(body.image_base64, size)
            total_size += file_size
            images[size] = resized_image

    image_detail = {}
    for k, v in images.items():
        image_detail[k] = s3_upload(v, f"{uuid}_{k}.webp", image_group)

    image_model = models.Images()
    image_model.user_id = request.state.user.id
    image_model.image_group_id = image_group_id
    image_model.uuid = uuid
    image_model.file_name = body.image_file_name
    image_model.file_extension = image_extension
    image_model.total_file_size = total_size
    image_model.image_url_data = image_detail
    session.add(image_model)
    image_group.add_count()
    session.commit()
    return image_model


@image.post("/bg-task", status_code=202)
async def bg_task_test(
    bg_task: BackgroundTasks,
    session: Session = Depends(db.session),
):
    # background_task(session)
    bg_task.add_task(background_task, session)
    return {"message": "background task started"}


def background_task(session):
    time.sleep(5)
    session.query(models.ImageGroups).update({models.ImageGroups.updated_at: "1999-01-05 00:00:00"})
    session.commit()


@image.get("/{image_id}")
async def get_image(request: Request, image_id: int, session: Session = Depends(db.session)):
    if request.state.user:
        return {"message": "success"}
    return {"message": "failed"}
