from fastapi import APIRouter, Depends
from models.products import Product
from database.connection import Database
router = APIRouter()

@router.get("/products", response_model=list[Product])
async def get_products(db=Depends(Database.get_db)):
    products = await db.products.find().to_list(1000)
    return products