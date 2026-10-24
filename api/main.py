from fastapi import FastAPI
from api.router.music import music_router

app = FastAPI()
app.include_router(music_router)