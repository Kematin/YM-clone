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
