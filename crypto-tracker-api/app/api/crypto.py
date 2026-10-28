from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.schemas.crypto import CryptoPriceResponse
from app.services.crypto_service import CryptoService
from app.core.database import get_db
from app.models.crypto import CryptoHistory

router = APIRouter(prefix="/api/v1/crypto", tags=["Crypto Data"])

@router.get("/current", response_model=CryptoPriceResponse)
async def get_current_crypto_price(
    crypto_id: str = Query("bitcoin", description="Exemplos: bitcoin, ethereum, solana")
):
    """Obtém a cotação atualizada em tempo real (apenas leitura)."""
    return await CryptoService.fetch_crypto_price(crypto_id=crypto_id)


@router.post("/sync", response_model=CryptoPriceResponse)
async def sync_crypto_price(
    crypto_id: str = Query("bitcoin"),
    db: Session = Depends(get_db)
):
    """Procura o preço atual na API externa e GUARDA o registo na base de dados local."""
    # 1. Procura na API externa
    crypto_data = await CryptoService.fetch_crypto_price(crypto_id)
    # 2. Guarda na base de dados
    CryptoService.save_crypto_price(db, crypto_data)
    
    return crypto_data


@router.get("/history")
async def get_crypto_history(
    crypto_id: str = Query("bitcoin"),
    limit: int = Query(10, description="Número máximo de registos a devolver"),
    db: Session = Depends(get_db)
):
    """Devolve o histórico de preços guardados na base de dados para uma moeda específica."""
    historico = db.query(CryptoHistory).filter(
        CryptoHistory.crypto_id == crypto_id
    ).order_by(CryptoHistory.timestamp.desc()).limit(limit).all()
    
    return historico