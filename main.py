from fastapi import FastAPI

import crud.emotion_crud as emotion_crud
import models.user_model as user_models
import schemas.emotion_schema as emotions_schema

from databases.sqlite_database import engine
from routers.user_router import router as user_router
from routers.emotion_router import router as emotion_router

user_models.db.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(emotion_router)


@app.get("/ping", tags=["admin"])
async def root():
    return {"message": "pong"}

