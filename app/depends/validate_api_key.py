import functools

from starlette.requests import Request

from app import models
from app.db.connection import db
from app.models import Users
from app.utils.auth_utils import get_current_timestamp, hash_string
import asyncio


def get_session(func):
    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            req = kwargs.get("request")
            get_current_session = hasattr(req.state, "current_session")
            if not get_current_session:
                req.state.current_session = next(db.session())
            return await func(*args, **kwargs)

        return wrapper
    else:
        ...


@get_session
async def validate_api_key(request: Request, ts: int, access_key: str, signature: str):
    session = request.state.current_session
    api_key = models.APIKeys.get_api_key(access_key=access_key, session=session)
    reproduced_signature = hash_string(
        {
            "ts": ts,
            "access_key": access_key,
        },
        api_key.secret_key,
    )
    if reproduced_signature != signature:
        raise ValueError("signature not match")
    if ts < int(get_current_timestamp()) - 5000:
        raise ValueError("timestamp expired")
    if ts > int(get_current_timestamp()):
        raise ValueError("timestamp not valid")
    request.state.user = Users.get(id=api_key.user_id, session=session)


async def validate_jwt_token():
    ...


async def validate_jwt_admin_token():
    ...
