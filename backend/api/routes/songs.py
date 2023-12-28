# db
from database.connection import AsyncSessionLocal
from database.crud import Database

# libs
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

# models
from models.songs import AddSong, Song
from services.songs import get_new_id


# dependency
async def get_db():
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        await db.close()


songs_router = APIRouter(tags=["Songs"])


@songs_router.get("/")
@logger.catch(exclude=HTTPException)
async def retrieve_all_songs(db_session=Depends(get_db)):
    """Retrieve all songs

    Args:
        db_session (_type_, optional). Defaults to Depends(get_db).
    """

    songs_database = Database(Song, db_session)
    songs = await songs_database.get_all()
    logger.info("Get all songs.")
    return {"songs": songs}


@songs_router.get("/{song_id}")
@logger.catch(exclude=HTTPException)
async def get_song(song_id: int, db_session=Depends(get_db)):
    """Retrieve single song by id

    Args:
        song_id (int),
        db_session (_type_, optional). Defaults to Depends(get_db).

    Raises:
        HTTPException (404): Song not found.
    """

    song_database = Database(Song, db_session)
    db_song = await song_database.get(song_id)
    if db_song:
        logger.info(f"Get song with id {song_id}")
        return {"song": db_song}
    else:
        logger.warning(f"Can not find song with id {song_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Song with id {song_id} not found.",
        )


@songs_router.post("/")
@logger.catch(exclude=HTTPException)
async def create_song(song: AddSong, db_session=Depends(get_db)):
    """Add new song

    Args:
        song (AddSong): payload data
        db_session (_type_, optional). Defaults to Depends(get_db).
    """

    song_database = Database(Song, db_session)
    new_id = await get_new_id(song_database)
    song = song.model_dump()
    song["length"] = 180
    song["id"] = new_id
    await song_database.create(song)

    logger.info(f"Add song {song}")
    return {"message": "successfull."}


@songs_router.delete("/{song_id}")
async def delete_single_song(song_id: int, db_session=Depends(get_db)):
    """Delete single song by id

    Args:
        song_id (int): id
        db_session (_type_, optional). Defaults to Depends(get_db).

    Raises:
        HTTPException: Song not found.
    """

    song_database = Database(Song, db_session)
    result = await song_database.delete(song_id)
    if result:
        logger.info(f"Delete song with id {song_id}")
        return {"message": "successfull."}
    else:
        logger.warning(f"Can not delete song with {song_id} (not found)")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Song with id {song_id} not found.",
        )
