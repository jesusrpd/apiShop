from fastapi import FastAPI, Request
from app.config import Settings
from pymongo import AsyncMongoClient
from contextlib import asynccontextmanager

settings = Settings()

class Database:
    def __init__(self, db):
        self.db = db

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        #Srtartup code only time when the app is started
        app.state.mongo_client = AsyncMongoClient(
            settings.DB_URI,
            maxPoolSize=50,
            minPoolSize=10,
        )
        app.state.db = app.state.mongo_client[settings.DB_NAME]
        yield
        #Shutdown code only time when the app is stopped
        await app.state.mongo_client.close()

    def get_db(resquest: Request):
        return resquest.app.state.db