from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnection:
    def __init__(self):
        self._engine = None
        self._engines = None
        self._session = None
        self._read_session = None

    def init_db(self, app: FastAPI, **kwargs):
        db_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.get("DB_POOL_RECYCLE")
        db_echo = kwargs.get("DB_ECHO")
        pool_size = kwargs.get("DB_POOL_SIZE")
        max_overflow = kwargs.get("DB_MAX_OVERFLOW")
        self._engines = create_engine(
                db_url,
                echo=db_echo,
                pool_recycle=pool_recycle,
                pool_pre_ping=True,
                pool_size=pool_size,
                max_overflow=max_overflow,
            )

        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engines)
        self.init_app_event(app=app)

    def init_app_event(self, app: FastAPI):

        @app.on_event("startup")
        def startup():
            self._engines.connect()
            print("DB 연결 성공")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engines.dispose()
            print("DB 연결 해제")

    def session(self):
        db_session = self._session()
        try:
            yield db_session
        finally:
            db_session.close()

    @property
    def engine(self):
        return self._engines[0]


db = DBConnection()
