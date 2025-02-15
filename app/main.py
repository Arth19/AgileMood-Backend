from fastapi import FastAPI

from app.schemas.user_schema import db

from app.databases.sqlite_database import engine
from app.routers.user_router import router as user_router
from app.routers.emotion_router import router as emotion_router
from app.routers.emotion_record_router import router as emotion_record_router
from app.routers.team_router import router as team_router

db.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(emotion_router)
app.include_router(emotion_record_router)
app.include_router(team_router)


@app.get("/ping", tags=["admin"])
async def root():
    return {"message": "pong"}

