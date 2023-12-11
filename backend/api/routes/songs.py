from fastapi import APIRouter

songs_router = APIRouter(tags=["Songs"])

songs = list()


@songs_router.get("/")
async def retrieve_all_songs():
    return {"songs": songs}
