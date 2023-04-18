from fastapi import FastAPI, File, UploadFile

from typing import Annotated

from .models import create_db_and_tables

from .routes import auth_routes

app = FastAPI()

import vitals 


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/analyze")
async def analyze(file: UploadFile):
    result = vitals.analyze(file.file)
    
    return result.dict(exclude={'image', 'thumb', 'icon'}) 

app.include_router(auth_routes, tags=["auth"], prefix="/auth")