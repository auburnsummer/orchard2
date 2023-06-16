from fastapi import FastAPI, UploadFile, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from v1.dependencies.client_nonrestricted import client_nonrestricted_shutdown

from v1.dependencies.session import create_db_and_tables

from .routes import auth_routes, user_routes, interaction_router
import logging

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event('shutdown')
async def shutdown_event():
    await client_nonrestricted_shutdown()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth_routes, tags=["auth"], prefix="/auth")
app.include_router(user_routes, tags=["user"], prefix="/user")
app.include_router(interaction_router, tags=["interactions"], prefix="/bot")