from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from app import models
from app.db.connection import db
from app.exceptions.excpetions import ImiziException
from app.utils.auth_utils import decode_token


class AccessControl(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.user = None
        request.state.access_token = request.headers.get("Authorization")
        if request.state.access_token:
            request.state.access_token = request.headers.get("Authorization").replace("Bearer ", "")
            session = next(db.session())
            user = decode_token(request.state.access_token)
            if user:
                request.state.user = models.Users.get(session, user.get("id"))
        ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
        request.state.ip = ip.split(",")[0] if "," in ip else ip
        try:
            return await call_next(request)
        except Exception as e:
            # raise e
            if not isinstance(e, ImiziException):
                return JSONResponse({"message": "Internal Server Error"}, status_code=500)
            else:
                return JSONResponse({"message": e.msg}, status_code=e.status_code)
