from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def _database_exist(engine, schema_name):
    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{schema_name}'"
    with engine.connect() as conn:
        result_proxy = conn.execute(query)
        result = result_proxy.scalar()
        return bool(result)


def _drop_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"DROP DATABASE {schema_name};")


def _create_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"CREATE DATABASE {schema_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;")



class DBConnection:
    def __init__(self):
        self._engine = None
        self._session = None
        self._read_session = None

    def init_db(self, app: FastAPI, **kwargs):
        db_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.get("DB_POOL_RECYCLE")
        db_echo = kwargs.get("DB_ECHO")
        pool_size = kwargs.get("DB_POOL_SIZE")
        max_overflow = kwargs.get("DB_MAX_OVERFLOW")
        test_mode = kwargs.get("TEST_MODE")
        self._engine = create_engine(
                db_url,
                echo=db_echo,
                pool_recycle=pool_recycle,
                pool_pre_ping=True,
                pool_size=pool_size,
                max_overflow=max_overflow,
            )
        if test_mode:
            print(db_url)
            db_name = self._engine.url.database
            if _database_exist(self._engine, db_name):
                _drop_database(self._engine, db_name)
            _create_database(self._engine, db_name)
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        self.init_app_event(app=app)

    def init_app_event(self, app: FastAPI):

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            print("DB 연결 성공")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            print("DB 연결 해제")

    def session(self):
        db_session = self._session()
        try:
            yield db_session
        finally:
            db_session.close()

    @property
    def engine(self):
        return self._engine


db = DBConnection()
