import uvicorn
from fastapi import FastAPI

from auth.app.fastapi_ import create_app

app: FastAPI = create_app()


if __name__ == '__main__':
    uvicorn.run('asgi:app', host="0.0.0.0",  port=5000, log_level='debug')
