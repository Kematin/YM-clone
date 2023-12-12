from typing import Annotated

from database.connection import SessionLocal, engine
from fastapi import APIRouter, Depends, status
from models.users import Base, RegisterUser, User
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

users_router = APIRouter(tags=["Users"])


@users_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: RegisterUser, db: db_dependency):
    user = user.dict()
    db_user = User(**user)
    db.add(db_user)
    db.commit()
    return {"message": "successfull."}


@users_router.get("/")
async def get_all_users(db: db_dependency):
    users_list = db.query(User).all()
    return {"users": users_list}


@users_router.get("/{user_id}")
async def get_user(user_id: int, db: db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    return {"user": db_user}
