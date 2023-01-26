from starlette import status


class ImiziException(Exception):
    status_code: int
    msg: str
    ex: Exception

    def __init__(self, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, msg: str = None, ex: Exception = None):
        self.status_code = status_code
        self.msg = msg
        self.ex = ex


class InternalServerException(ImiziException):
    def __init__(
        self,
        msg="internal server error",
        status_code=500,
        ex: Exception = None,
    ):
        super().__init__(
            status_code=status_code,
            msg=msg,
            ex=ex,
        )


class NotFoundException(ImiziException):
    def __init__(
        self,
        msg,
        status_code=404,
        ex: Exception = None,
    ):
        super().__init__(
            status_code=status_code,
            msg=msg,
            ex=ex,
        )


class BadRequestException(ImiziException):
    def __init__(
        self,
        msg,
        status_code=400,
        ex: Exception = None,
    ):
        super().__init__(
            status_code=status_code,
            msg=msg,
            ex=ex,
        )