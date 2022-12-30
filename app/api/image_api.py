from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import uuid4
from app import models, schemas
from app.db.connection import db
from app.depends.validate_api_key import validate_api_key
from app.schemas.image_schemas import UploadImageREQ
from app.utils.image_utils import get_image_size, resize_image, get_image_extension, get_squared_thumbnail, s3_upload

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
    image_convert_size = [512, 1024, 1920]
    image_size = get_image_size(body.image)
    image_extension = get_image_extension(body.image)
    uuid = str(uuid4())
    thumbnail, file_size = get_squared_thumbnail(body.image)

    images = {"thumbnail": thumbnail}
    total_size = file_size

    for size in image_convert_size:
        if image_size[0] > size:
            resized_image, file_size = resize_image(body.image, size)
            total_size += file_size
            images[size] = resized_image

    image_detail = {}
    for k, v in images.items():
        image_detail[k] = s3_upload(v, f"{uuid}_{k}.webp")

    print(image_detail)


"""
    있음 user_id = Column(ForeignKey("users.id"), nullable=False)
    있음 image_group_id = Column(ForeignKey("image_groups.id"), nullable=False)
    있음 uuid = Column(String(64), nullable=False, default=uuid.uuid4)
    필요없는 모델 s3_key = Column(String(256), nullable=False)
    있음 file_name = Column(String(128), nullable=False)
    필요없는 모델 file_mime = Column(String(64), nullable=False)
    있음 file_extension = Column(String(16), nullable=False)
    필요없는 모델 file_size = Column(Integer, nullable=False)
    있음 total_file_size = Column(Integer, nullable=False)
    있음 image_url_data = Column(JSON, nullable=False)
    image_group = relationship("ImageGroups", back_populates="images", uselist=False)

"""


@image.get("/{image_id}")
def get_image(request: Request, image_id: int, session: Session = Depends(db.session)):
    if request.state.user:
        return {"message": "success"}
    return {"message": "failed"}
