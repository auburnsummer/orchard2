from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated
from pydantic import BaseModel
from sqlmodel import Session, select

from v1.dependencies.injected_user import InjectedUser, injected_user
from v1.dependencies.session import InjectedSession
from v1.models import engine
from v1.models.discord import DiscordUser
from v1.models.user import User

auth_routes = APIRouter()

class CreateUserPayload(BaseModel):
    pass

@auth_routes.post("/create")
async def create_user(user: InjectedUser, session: InjectedSession):
    user_id = user.id
    select_statement = select(User).where(User.discord_id == user_id)
    existing_user = session.exec(select_statement).first()
    if existing_user:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    # if we reached here, there is no existing user so we can create one.
    new_user = User(id=user.id)
    session.add(new_user)

    session.commit()