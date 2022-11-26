import uvicorn
from fastapi import FastAPI

from config import get_env


def start_app():
    app = FastAPI()
    env = get_env()
    for i in env.__dict__.items():
        print(i)
    print()
    return app


if __name__ == "__main__":
    uvicorn.run("main:start_app", host="0.0.0.0", port=8000, reload=True, factory=True)
