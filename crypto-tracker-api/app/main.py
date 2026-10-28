from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.api.crypto import router as crypto_router
from app.core.database import engine, Base
from app.models import crypto
from app.core.tasks import fetch_and_store_crypto_data

# Cria as tabelas na base de dados SQLite
Base.metadata.create_all(bind=engine)

# Configuração do Scheduler
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- O que acontece ao LIGAR o servidor ---
    print("🚀 A iniciar o agendador de tarefas...")
    scheduler.add_job(
        fetch_and_store_crypto_data, 
        'interval', 
        seconds=settings.FETCH_INTERVAL_SECONDS
    )
    scheduler.start()
    yield
    # --- O que acontece ao DESLIGAR o servidor ---
    print("🛑 A encerrar o agendador de tarefas...")
    scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API para agregação e análise de dados em tempo real",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # Regista os eventos de arranque e encerramento
)

app.include_router(crypto_router)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "online", 
        "project": settings.PROJECT_NAME
    }

@app.get("/", tags=["System"])
async def root():
    return {"mensagem": "Bem-vindo à Data Tracker API! Aceda a /docs para ver a documentação."}