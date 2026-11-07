from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Database
from routes import products

app = FastAPI(lifespan=Database.lifespan)

origins = ["http://localhost:3000"]

app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)

@app.get("/")
async def root():
    return {"message": "Hello API SHOP"}


