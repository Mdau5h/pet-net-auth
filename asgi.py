import uvicorn
from fastapi import FastAPI
from auth.app.app import create_app
from auth.database.utils import db_setup

app: FastAPI = create_app()


@app.on_event("startup")
async def startup_event():
    await db_setup()


if __name__ == '__main__':
    uvicorn.run('asgi:app', host="0.0.0.0",  port=5000, log_level='debug')
