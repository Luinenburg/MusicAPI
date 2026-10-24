from fastapi import APIRouter
from pydantic import BaseModel
from downloader import download

music_router = APIRouter(prefix="/add_music")

class SongList(BaseModel):
    songs: list[str]

@music_router.post("/songs/")
async def add_songs(song_list: SongList):
    """Add songs from a list"""
    for song in song_list.songs:
        download(song)
    return {"butts": "butts"}

@music_router.post("/song/{song}")
async def add_song(song: str):
    """Add one song"""
    song_url = "https://music.youtube.com/playlist?list="+song
    print(f"song_url: {song_url}")
    download(song_url)
    return {"butts": "butts"}