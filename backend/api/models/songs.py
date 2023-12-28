# db dependency
from database.connection import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=False)
    path = Column(Text, unique=True)
    length = Column(Integer)
    likes = Column(Integer, nullable=True, default=0)
    # album_id: int
    # artist_id: int

    class Settings:
        json_schema_extra = {
            "example": {
                "name": "cool song",
                "path": "/static/songs/album/id.mp4",
                "album_id": 1,
                "artist_id": 2,
                "length": 154,
                "likes": 31,
            }
        }


class AddSong(BaseModel):
    name: str
    path: str

    class Settings:
        json_schema_extra = {"example": {"name": "cool song", "path": "song.mp4"}}
