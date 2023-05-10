from fastapi import APIRouter, HTTPException, status

from sqlmodel import select

from v1.dependencies.injected_user import InjectedToken, InjectedUserFull
from v1.dependencies.session import InjectedSession
from v1.models.user import User, UserCombined

user_routes = APIRouter()


@user_routes.get("/me", response_model=UserCombined)
async def get_current_user(user: InjectedUserFull):
    return user


@user_routes.post("/create", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(token: InjectedToken, session: InjectedSession):
    # use InjectedToken here not InjectedUser as InjectedUser will not succeed if the user does not exist.
    user_id = token.sub
    select_statement = select(User).where(User.discord_id == user_id)
    existing_user = session.exec(select_statement).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    # if we reached here, there is no existing user so we can create one.
    new_user = User(discord_id=user_id)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
 