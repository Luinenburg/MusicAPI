from fastapi import APIRouter
from pydantic import BaseModel
from downloader import download

music_router = APIRouter(prefix="/add_music")

class SongList(BaseModel):
    songs: list[str]

@music_router.post("/songs/")
async def add_songs(song_list: SongList):
    """Add songs from a list"""
    results = []
    for song in song_list.songs:
        results.append(download(song))
    return {"status": "request complete", "individual_responses": results}

@music_router.post("/song/{song}")
async def add_song(song: str):
    """Add one song"""
    song_url = "https://music.youtube.com/playlist?list="+song
    print(f"song_url: {song_url}")
    try:
        status = download(song_url)
    except:
        status = "some bullshit in the download function"
    return {"status": status}

@music_router.post("/songs/overwrite/")
async def add_songs(song_list: SongList):
    """Add songs from a list"""
    results = []
    for song in song_list.songs:
        if song.overwrite == "true":
            results.append(download(song.id, True))
        else:
            results.append(download(song.id, False))
    return {"status": "request complete", "individual_responses": results}

@music_router.post("/song/overwrite/{song}")
async def add_song(song: str):
    """Add one song"""
    song_url = "https://music.youtube.com/playlist?list="+song
    print(f"song_url: {song_url}")
    try:
        status = download(song_url, True)
    except:
        status = "some bullshit in the download function"
    return {"status": status}
