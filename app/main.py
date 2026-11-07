from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from pymongo import AsyncMongoClient
from contextlib import asynccontextmanager
from datetime import datetime
from bson.timestamp import Timestamp
from .config import Settings

settings = Settings()

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
    app.state.mongo_client.close()

app = FastAPI(lifespan=lifespan)

def get_db(resquest: Request):
    return resquest.app.state.db

PyObjectId = Annotated[str, BeforeValidator(str)]

def ts_to_datetime(v):
    return v.as_datetime() if isinstance(v, Timestamp) else v

MongoDatetime = Annotated[datetime, BeforeValidator(ts_to_datetime)]

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    description: str
    price: float
    created_at: MongoDatetime

@app.get("/")
async def root():
    return {"message": "Hello API SHOP"}

@app.get("/products", response_model=list[Product])
async def get_products(db=Depends(get_db)):
    products = await db.products.find().to_list(1000)
    return products
