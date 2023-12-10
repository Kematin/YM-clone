from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

DEFAULT_PLAYLIST_COVER = "static/imgs/default/cover.png"


class Playlist(BaseModel):
    id: Optional[int] = None
    title: str
    user_id: int
    song_list_id: List[Optional[int]]
    cover: Optional[str] = DEFAULT_PLAYLIST_COVER
    created_at: datetime
    updated_at: datetime
    is_public: bool

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 2,
                "song_list_id": [2, 4, 1],
                "title": "cool playlist",
                "cover": DEFAULT_PLAYLIST_COVER,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "is_public": False,
            }
        }


class CreatePlaylist(BaseModel):
    title: str
    song_list_id: List[Optional[int]]
    cover: Optional[str] = DEFAULT_PLAYLIST_COVER
    is_public: bool

    class Config:
        json_schema_extra = {
            "example": {
                "title": "cool playlist",
                "song_list_id": [2, 4, 1],
                "cover": "cover.png",
                "is_public": False,
            }
        }


class UpdatePlaylist(BaseModel):
    title: Optional[str]
    song_list_id: Optional[List[int]]
    cover: Optional[str]
    is_public: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "cool playlist v2",
                "cover": "cover2.png",
                "is_public": True,
            }
        }
