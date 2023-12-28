# date
from datetime import date

# db
from database.connection import AsyncSessionLocal
from database.crud import Database

# libs
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

# models
from models.users import RegisterUser, UpdateUser, User
from pydantic import UUID4

# services
from services.users import check_username

# exc
from sqlalchemy.exc import SQLAlchemyError


# dependency
async def get_db():
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        await db.close()


users_router = APIRouter(tags=["Users"])


@users_router.get("/")
@logger.catch
async def get_all_users(db_session=Depends(get_db)):
    """Retrieve all users

    Args:
        db_session (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """

    users_database = Database(User, db_session)
    users_list = await users_database.get_all()
    logger.info("Get users list")
    return {"users": users_list}


@users_router.get("/{user_id}")
@logger.catch(exclude=HTTPException)
async def get_user(user_id: UUID4, db_session=Depends(get_db)):
    """Retieve single user by uuid

    Args:
        user_id (UUID4): _description_
        db_session (_type_, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    users_database = Database(User, db_session)
    db_user = await users_database.get(user_id)
    if db_user:
        logger.info(f"Get user with id {user_id}")
        return {"user": db_user}
    else:
        logger.warning(f"Can not find user with id {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )


@users_router.post("/", status_code=status.HTTP_201_CREATED)
@logger.catch(exclude=HTTPException)
async def create_user(user: RegisterUser, db_session=Depends(get_db)):
    """Create new user

    Args:
        user (RegisterUser): _description_
        db_session (_type_, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    users_database = Database(User, db_session)
    user = user.model_dump()
    user["created_at"] = date.today()
    try:
        await users_database.create(user)
        logger.info("Create new user with username {}".format(user.get("username")))
        return {"message": "successfull."}
    except SQLAlchemyError:
        logger.warning("Denied user creation: username is already in use")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with current data already exist.",
        )


@users_router.delete("/{user_id}")
@logger.catch(exclude=HTTPException)
async def delete_user(user_id: UUID4, db_session=Depends(get_db)):
    """Delete user by uuid

    Args:
        user_id (UUID4): _description_
        db_session (_type_, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    users_database = Database(User, db_session)
    db_user = await users_database.delete(user_id)
    if db_user:
        logger.info(f"Delete user with id {user_id}")
        return {"message": "succesfull"}
    else:
        logger.warning(f"Can not find user with id {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )


@users_router.delete("/")
@logger.catch()
async def delete_all_users(db_session=Depends(get_db)):
    """(Temporarily) Delete all users

    Args:
        db_session (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """

    users_database = Database(User, db_session)
    await users_database.delete_all()
    logger.info("Delete all users.")
    return {"message": "succesfull"}


@users_router.put("/{user_id}")
@logger.catch(exclude=HTTPException)
async def update_user_data(
    user_id: UUID4, user_data: UpdateUser, db_session=Depends(get_db)
):
    """Update user data

    Args:
        user_id (UUID4): _description_
        user_data (UpdateUser): _description_
        db_session (_type_, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException (409): Conflict with username
        HTTPException (404): User not found

    Returns:
        _type_: _description_
    """

    users_database = Database(User, db_session)
    db_users = await users_database.get_all()
    user_data = user_data.model_dump()
    if not check_username(user_data, db_users):
        logger.warning(
            "User with username {} already exist.".format(user_data["username"])
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with current username already exist.",
        )

    updated_user = await users_database.update(user_id, user_data)

    if updated_user:
        logger.info(f"Update user data with id {user_id}")
        return {"user": updated_user}
    else:
        logger.warning(f"Can not find user with id {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
