from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Conexão com o banco de dados SQLite
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} # Necessário para o SQLite no FastAPI
)

# Criador de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos
Base = declarative_base()

# Dependência para injetar a sessão da base de dados nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()