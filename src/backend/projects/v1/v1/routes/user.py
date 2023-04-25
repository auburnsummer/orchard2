from fastapi import APIRouter, HTTPException, status

from sqlmodel import select

from v1.dependencies.injected_user import InjectedDiscordUser, InjectedUser
from v1.dependencies.session import InjectedSession
from v1.models.user import User, UserCombined

user_routes = APIRouter()


@user_routes.get("/me", response_model=UserCombined)
async def get_current_user(user: InjectedUser):
    return user


@user_routes.post("/create", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: InjectedDiscordUser, session: InjectedSession):
    user_id = user.id
    select_statement = select(User).where(User.discord_id == user_id)
    existing_user = session.exec(select_statement).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    # if we reached here, there is no existing user so we can create one.
    new_user = User(discord_id=user.id)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
