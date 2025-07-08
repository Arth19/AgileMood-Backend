from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 🚀 Importação do CORS

from app.schemas.user_schema import db
from app.databases.postgres_database import Base, engine, get_db
from app.routers.user_router import router as user_router
from app.routers.emotion_router import router as emotion_router
from app.routers.emotion_record_router import router as emotion_record_router
from app.routers.team_router import router as team_router
from app.routers.reports_router import router as reports_router
from app.routers.feedback_router import router as feedback_router
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

db.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",  # Para desenvolvimento local
    "https://agile-mood-frontend.vercel.app",  # Domínio principal do Vercel
    "https://agile-mood-frontend-arth19.vercel.app",  # Seu subdomínio no Vercel
    "https://agile-mood-frontend-git-main-arth19.vercel.app"  # URL de preview
    "https://agile-mood-front-end.vercel.app"
    "https://agile-mood.vercel.app"
]

# 🚨 Configuração do CORS para permitir acesso do frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ Permitir acesso apenas do Next.js
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # ✅ Permite todos os headers (incluindo Authorization)
)

# 🚀 Incluindo as rotas
app.include_router(user_router)
app.include_router(emotion_router)
app.include_router(emotion_record_router)
app.include_router(team_router)
app.include_router(reports_router)
app.include_router(feedback_router)


@app.get("/ping", tags=["admin"])
async def root():
    return {"message": "pong"}
