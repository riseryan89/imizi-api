from pydantic import BaseModel, EmailStr
from typing import List


class APIKeysRES(BaseModel):
    id: int
    access_key: str
    whitelist_ips: str | None

    class Config:
        orm_mode = True


class APIKeysExtendRES(APIKeysRES):
    secret_key: str


class UsersRES(BaseModel):
    id: int
    email: str
    api_keys: List[APIKeysRES] = []

    class Config:
        orm_mode = True


class UsersREQ(BaseModel):
    email: EmailStr
    pw: str
