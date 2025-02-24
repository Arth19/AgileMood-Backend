from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 🚀 Importação do CORS

from app.schemas.user_schema import db
from app.databases.sqlite_database import engine
from app.routers.user_router import router as user_router
from app.routers.emotion_router import router as emotion_router
from app.routers.emotion_record_router import router as emotion_record_router
from app.routers.team_router import router as team_router
from app.routers.reports_router import router as reports_router

db.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🚨 Configuração do CORS para permitir acesso do frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Permitir acesso apenas do Next.js
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # ✅ Permite todos os headers (incluindo Authorization)
)

# 🚀 Incluindo as rotas
app.include_router(user_router)
app.include_router(emotion_router)
app.include_router(emotion_record_router)
app.include_router(team_router)
app.include_router(reports_router)


@app.get("/ping", tags=["admin"])
async def root():
    return {"message": "pong"}
