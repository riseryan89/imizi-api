from fastapi import Depends
from starlette.requests import Request

from app import models
from app.db.connection import db
from app.utils.auth_utils import get_current_timestamp, hash_string


async def validate_api_key(ts: int, access_key: str, signature: str):
    session = next(db.session())
    api_key = models.APIKeys.get_api_key(access_key=access_key, session=session)
    reproduced_signature = hash_string(
        {
            "ts": ts,
            "access_key": access_key,
        },
        api_key.secret_key,
    )
    if reproduced_signature != signature:
        print("signature not match")
        return False
    if ts < int(get_current_timestamp()) - 500:
        print(ts, int(get_current_timestamp()))
        print("timestamp expired")
        return False
    if ts > int(get_current_timestamp()):
        print("timestamp not valid")
        return False
    return True