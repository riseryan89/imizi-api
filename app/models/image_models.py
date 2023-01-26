import uuid
from sqlalchemy import Column, String, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship

from app.models import Users
from app.models.base_model import Base


class ImageGroups(Base):
    __tablename__ = "images_groups"
    uuid = Column(String(64), nullable=False, default=uuid.uuid4)
    user_id = Column(ForeignKey(Users.id), nullable=False)
    image_group_name = Column(String(64), nullable=False)
    image_count = Column(Integer, nullable=False, default=0)


class Images(Base):
    __tablename__ = "images"
    user_id = Column(ForeignKey(Users.id), nullable=False)
    image_group_id = Column(ForeignKey(ImageGroups.id), nullable=False)
    uuid = Column(String(64), nullable=False, default=uuid.uuid4)
    file_name = Column(String(128), nullable=False)
    file_extension = Column(String(16), nullable=False)
    total_file_size = Column(Integer, nullable=False)
    image_url_data = Column(JSON, nullable=False)
    image_group = relationship("ImageGroups", backref="image_group", uselist=False)




    def add_count(self):
        self.image_count += 1

    @classmethod
    def get(cls, session, user_id, image_group_id):
        return session.query(cls).filter_by(user_id=user_id, id=image_group_id).first()
