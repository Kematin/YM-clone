from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

DEFAULT_IMAGE = "static/imgs/default/default_user.png"


class User(BaseModel):
    id: Optional[int] = None  # TODO autoincrement by db
    username: str
    email: EmailStr
    password: str
    image: Optional[str] = DEFAULT_IMAGE
    created_at: Optional[datetime] = None
    is_artist: Optional[bool] = False
    liked_playlist_id: List[Optional[int]]
    liked_album_id: List[Optional[int]]
    liked_artist_id: List[Optional[int]]

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
    image: Optional[str] = DEFAULT_IMAGE

    class config:
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

    class config:
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
