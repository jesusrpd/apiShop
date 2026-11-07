
from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from datetime import datetime
from bson.timestamp import Timestamp

def ts_to_datetime(v):
    return v.as_datetime() if isinstance(v, Timestamp) else v

PyObjectId = Annotated[str, BeforeValidator(str)]
MongoDatetime = Annotated[datetime, BeforeValidator(ts_to_datetime)]

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    description: str
    price: float
    created_at: MongoDatetime