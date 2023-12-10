from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Artist(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: str
    image: str
    description: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 2,
                "name": "cool artist",
                "image": "static/imgs/artists/1.png",
                "description": "No description.",
                "created_at": datetime.now(),
            }
        }


class RegisterArtist(BaseModel):
    email: EmailStr
    name: str
    image: str
    description: Optional[str] = "No description."

    class Config:
        json_schema_extra = {
            "example": {
                "email": "some@mail.ru",
                "name": "cool artist",
                "image": "cool_image.png",
            }
        }


class UpdateArtist(BaseModel):
    name: Optional[str]
    image: Optional[str]
    description: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "cool artist v2",
                "image": "cool_image.png",
                "description": "very cool artist.",
            }
        }
