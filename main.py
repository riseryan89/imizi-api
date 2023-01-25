import logging

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from sqlalchemy import text

from app.middlewares.access_control import AccessControl
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from config import get_env
from app.db.connection import db
from app.api.user_api import user
from app.api.image_api import image

HTTP_BEARER = HTTPBearer(auto_error=False)


def start_app():
    app = FastAPI(debug=True)
    env = get_env()
    db.init_db(app=app, **env.dict())
    # get_session = db.session
    # session = next(get_session)
    # print(session.query(text("select 1")))

    app.add_middleware(AccessControl)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=env.TRUSTED_HOSTS, except_path=["/"])
    app.include_router(user, prefix="/users", tags=["Users"])
    app.include_router(image, prefix="/images", tags=["Images"], dependencies=[Depends(HTTP_BEARER)])

    return app


app = start_app()

if __name__ == "__main__":
    uvicorn.run("main:start_app", host="0.0.0.0", port=8000, reload=True, factory=True)
