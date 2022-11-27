import uuid
from sqlalchemy import Column, String, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Images(Base):
    __tablename__ = "images"
    user_id = Column(ForeignKey("users.id"), nullable=False)
    image_group_id = Column(ForeignKey("image_groups.id"), nullable=False)
    uuid = Column(String(64), nullable=False, default=uuid.uuid4)
    s3_key = Column(String(256), nullable=False)
    file_name = Column(String(128), nullable=False)
    file_mime = Column(String(64), nullable=False)
    file_extension = Column(String(16), nullable=False)
    file_size = Column(Integer, nullable=False)
    total_file_size = Column(Integer, nullable=False)
    image_url_data = Column(JSON, nullable=False)
    image_group = relationship("ImageGroups", back_populates="images", uselist=False)


class ImageGroups(Base):
    __tablename__ = "images_groups"
    uuid = Column(String(64), nullable=False, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    image_group_name = Column(String(64), nullable=False)
    image_count = Column(Integer, nullable=False, default=0)
    images = relationship("Images", back_populates="image_groups")

