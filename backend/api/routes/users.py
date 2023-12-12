from database.connection import SessionLocal, engine
from database.crud import Database
from fastapi import APIRouter, HTTPException, status
from models.users import Base, RegisterUser, User

Base.metadata.create_all(bind=engine)


# dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


users_router = APIRouter(tags=["Users"])
users_database = Database(User, get_db())


@users_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: RegisterUser):
    user = user.dict()
    users_database.create(user)
    return {"message": "successfull."}


@users_router.get("/")
async def get_all_users():
    users_list = users_database.get_all()
    return {"users": users_list}


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    db_user = users_database.get(user_id)
    if db_user:
        return {"user": db_user}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
