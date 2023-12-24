from typing import Optional

from pydantic import BaseModel


class Song(BaseModel):
    id: Optional[int] = None
    name: str
    path: str
    album_id: int
    artist_id: int
    length: int
    likes: Optional[int] = 0

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
    file: str

    class Settings:
        json_schema_extra = {"example": {"name": "cool song", "file": "song.mp4"}}
