from datetime import datetime
from typing import List, Optional

from database.connection import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, Column, Integer, String

DEFAULT_USER_IMAGE = "static/imgs/default/default_user.png"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    is_artist = Column(Boolean, nullable=True, default=False)
    password = Column(String(100))
    # created_at: datetime
    # image: Optional[str] = DEFAULT_USER_IMAGE
    # liked_playlist_id: List[Optional[int]]
    # liked_album_id: List[Optional[int]]
    # liked_artist_id: List[Optional[int]]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "kematin",
                "email": "some@mail.ru",
                "password": "strong!!!",
                "image": "static/imgs/users/id.png",
                "is_artist": False,
                "created_at": datetime.now(),
                "liked_playlist_id": "[]",
                "liked_album_id": "[]",
                "liked_artist_id": "[]",
            }
        }


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    # image: Optional[str] = DEFAULT_USER_IMAGE

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "kematin",
                "email": "some@mail.ru",
                "password": "strong!!!",
                "image": "image.png",
            }
        }


class LoginUser(BaseModel):
    username: str | EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "kematin",
                "password": "strong!!!",
            }
        }


class UpdateUser(BaseModel):
    username: Optional[str]
    image: Optional[str]
    is_artist: Optional[bool]
    liked_playlist_id: Optional[List[int]]
    liked_album_id: Optional[List[int]]
    liked_artist_id: Optional[List[int]]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "kematin v2",
                "image": "some_img.jpg",
                "is_artist": True,
            }
        }


# TODO Reset password after email check
class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str

    class Config:
        json_schema_extra = {
            "example": {"email": "some@mail.ru", "new_password": "very strong!!!"}
        }


# TODO Reset email by link in new email box
class EmailReset(BaseModel):
    email: EmailStr
    new_email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {"email": "some@mail.ru", "new_email": "some2@mail.ru"}
        }
