from datetime import date

from database.connection import SessionLocal, engine
from database.crud import Database
from fastapi import APIRouter, HTTPException, status
from models.users import Base, RegisterUser, UpdateUser, User
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError

Base.metadata.create_all(bind=engine)


# dependency
def get_db():
    db = SessionLocal()
    return db


users_router = APIRouter(tags=["Users"])
users_database = Database(User, get_db())


@users_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: RegisterUser):
    user = user.model_dump()
    user["created_at"] = date.today()
    try:
        users_database.create(user)
        return {"message": "successfull."}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with current data already exist.",
        )


@users_router.get("/")
async def get_all_users():
    users_list = users_database.get_all()
    return {"users": users_list}


@users_router.get("/{user_id}")
async def get_user(user_id: UUID4):
    db_user = users_database.get(user_id)
    if db_user:
        return {"user": db_user}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )


@users_router.delete("/{user_id}")
async def delete_user(user_id: UUID4):
    db_user = users_database.delete(user_id)
    if db_user:
        return {"message": "succesfull"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )


def check_username(user_id: UUID4, user_data: UpdateUser) -> True:
    user_data = user_data.model_dump()
    new_username = user_data.get("username", None)

    if new_username is None:
        return True

    db_users = users_database.get_all()
    for db_user in db_users:
        if db_user.username == new_username:
            return False

    return True


@users_router.put("/{user_id}")
async def update_user_data(user_id: UUID4, user_data: UpdateUser):
    if not check_username(user_id, user_data):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with current username already exist.",
        )

    updated_user = users_database.update(user_id, user_data)
    if updated_user:
        return {"user": updated_user}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
