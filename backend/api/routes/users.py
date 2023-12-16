from datetime import date

from database.connection import SessionLocal, engine
from database.crud import Database
from fastapi import APIRouter, HTTPException, status
from loguru import logger
from models.users import Base, RegisterUser, UpdateUser, User
from pydantic import UUID4

# services
from services.users import check_username
from sqlalchemy.exc import IntegrityError

Base.metadata.create_all(bind=engine)


# dependency
def get_db():
    db = SessionLocal()
    return db


users_router = APIRouter(tags=["Users"])
users_database = Database(User, get_db())


@users_router.post("/", status_code=status.HTTP_201_CREATED)
@logger.catch(exclude=HTTPException)
async def create_user(user: RegisterUser):
    user = user.model_dump()
    user["created_at"] = date.today()
    try:
        users_database.create(user)
        logger.info("Create new user with username {}".format(user.get("username")))
        return {"message": "successfull."}
    except IntegrityError:
        logger.warning("Denied user creation: username is already in use")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with current data already exist.",
        )


@users_router.get("/")
@logger.catch
async def get_all_users():
    users_list = users_database.get_all()
    logger.info("Get users list")
    return {"users": users_list}


@users_router.get("/{user_id}")
@logger.catch(exclude=HTTPException)
async def get_user(user_id: UUID4):
    db_user = users_database.get(user_id)
    if db_user:
        logger.info(f"Get user with id {user_id}")
        return {"user": db_user}
    else:
        logger.warning(f"Can not find user with id {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )


@users_router.delete("/{user_id}")
@logger.catch(exclude=HTTPException)
async def delete_user(user_id: UUID4):
    db_user = users_database.delete(user_id)
    if db_user:
        return {"message": "succesfull"}
    else:
        logger.warning(f"Can not find user with id {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )


@users_router.delete("/")
@logger.catch()
async def delete_all_users():
    users_database.delete_all()
    logger.info("Delete all users.")
    return {"message": "succesfull"}


@users_router.put("/{user_id}")
@logger.catch(exclude=HTTPException)
async def update_user_data(user_id: UUID4, user_data: UpdateUser):
    db_users = users_database.get_all()
    user_data = user_data.model_dump()
    if not check_username(user_data, db_users):
        logger.warning(
            "User with username {} already exist.".format(user_data["username"])
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with current username already exist.",
        )

    updated_user = users_database.update(user_id, user_data)

    if updated_user:
        logger.info(f"Update user data with id {user_id}")
        return {"user": updated_user}
    else:
        logger.warning(f"Can not find user with id {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
