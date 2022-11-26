import os
from os import path
from platform import system
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: str = path.dirname((path.abspath(__file__)))
    LOCAL_MODE: bool = True if system().lower().startswith("darwin") or system().lower().startswith("Windows") else False
    app_name: str = "Imizi API"
    TEST_MODE: bool = False

    ALLOW_SITE = ["*"]
    TRUSTED_HOSTS = ["*"]
    JWT_ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "imizi-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1  # one day

    DB_URL: str = ""
    DB_POOL_RECYCLE: Optional[int] = 900
    DB_ECHO: Optional[bool] = True
    DB_POOL_SIZE: Optional[int] = 1
    DB_MAX_OVERFLOW: Optional[int] = 1


class DevSettings(Settings):
    DB_URL = "mysql+pymysql://root:root@localhost:3306/imizi?charset=utf8mb4"
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10


class TestSettings(Settings):
    DB_URL = "mysql+pymysql://root:root@localhost:3306/imizi?charset=utf8mb4"
    DB_POOL_SIZE = 1
    DB_MAX_OVERFLOW = 0


class ProdSettings(Settings):
    DB_URL = "mysql+pymysql://root:root@localhost:3306/imizi?charset=utf8mb4"
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10


def get_env():
    cfg_cls = dict(
        prd=ProdSettings,
        dev=DevSettings,
        test=TestSettings,
    )
    env = cfg_cls[os.getenv("FASTAPI_ENV", "dev")]()

    return env


settings = get_env()
