from fastapi import FastAPI, UploadFile

from v1.dependencies.client_nonrestricted import client_nonrestricted_shutdown

from v1.dependencies.session import create_db_and_tables

from .routes import auth_routes, user_routes

app = FastAPI()

import vitals
import httpx

client = httpx.AsyncClient()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event('shutdown')
async def shutdown_event():
    await client_nonrestricted_shutdown()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/analyze")
async def analyze(file: UploadFile):
    result = vitals.analyze(file.file)
    
    return result.dict(exclude={'image', 'thumb', 'icon'}) 

app.include_router(auth_routes, tags=["auth"], prefix="/auth")
app.include_router(user_routes, tags=["user"], prefix="/user")