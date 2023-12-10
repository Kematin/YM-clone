from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Album(BaseModel):
    id: Optional[int] = None
    artist_id: int
    title: str
    cover: str
    created_at: datetime
    is_single: bool

    class Settings:
        json_schema_extra = {
            "example": {
                "artist_id": 1,
                "title": "cool album",
                "cover": "static/imgs/cover/albums/id.png",
                "created_at": datetime.now(),
                "is_single": True,
            }
        }


class AddAlbum(BaseModel):
    title: str
    cover: str

    class Settings:
        json_schema_extra = {"example": {"title": "cool album", "cover": "cover.png"}}


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
    song: str

    class Settings:
        json_schema_extra = {"example": {"name": "cool song", "file": "song.mp4"}}


class AlbumSongs(BaseModel):
    album_id: int
    songs: List[int]

    class Settings:
        json_schema_extra = {
            "example": {
                "album_id": 2,
                "songs": [
                    1,
                    4,
                    5,
                ],
            }
        }
