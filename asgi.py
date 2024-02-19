import uvicorn
from fastapi import FastAPI
from auth.app.app import create_app
from auth.app.db import db_setup, async_session

app: FastAPI = create_app()


@app.on_event("startup")
async def startup_event():
    async with async_session() as session:
        await db_setup(session=session)


if __name__ == '__main__':
    uvicorn.run('asgi:app', host="0.0.0.0",  port=5000, log_level='debug')
