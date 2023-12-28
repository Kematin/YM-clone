from database.crud import Database


async def get_new_id(song_database: Database):
    last_song = await song_database.get_all()
    try:
        return last_song[-1].id + 1
    except IndexError:
        return 1
