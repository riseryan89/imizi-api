import os
from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.connection import db
from app.models import Base, UserPayPlans
from main import start_app


@pytest.fixture(scope="package")
def client():
    """
    서버 생성 함수
    :return:
    """
    os.environ["FASTAPI_ENV"] = "test"

    app = start_app()
    Base.metadata.create_all(db.engine)
    with TestClient(app=app, base_url="http://localhost:8000") as client:
        yield client


def prepare_db():
    Base.metadata.create_all(db.engine)
    sess = next(db.session())
    sample_plan = UserPayPlans()
    sample_plan.name = "FREE"
    sample_plan.price = 0
    sample_plan.max_image_size = 0
    sample_plan.max_image_count = 0
    sample_plan.max_image_group_count = 0
    sess.add(sample_plan)
    sess.commit()


@pytest.fixture(scope="function", autouse=True)
def session():
    """
    테스트 단위로 작동하며 디비 초기화
    :return:
    """
    sess = next(db.session())
    yield sess
    sess.rollback()
