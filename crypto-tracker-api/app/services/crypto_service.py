import httpx
from datetime import datetime
from typing import Dict, Any, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.crypto import CryptoPriceResponse
from app.models.crypto import CryptoHistory

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

class CryptoService:
    @staticmethod
    async def fetch_crypto_price(crypto_id: str = "bitcoin") -> CryptoPriceResponse:
        """
        Procura o preço atual e métricas de uma criptomoeda na CoinGecko.
        """
        url = f"{COINGECKO_BASE_URL}/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": crypto_id,
            "order": "market_cap_desc",
            "sparkline": "false"
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=404, detail=f"Criptomoeda '{crypto_id}' não encontrada.")

                coin = data[0]
                return CryptoPriceResponse(
                    crypto_id=coin["id"],
                    name=coin["name"],
                    symbol=coin["symbol"].upper(),
                    price_usd=float(coin["current_price"]),
                    market_cap_usd=float(coin["market_cap"]),
                    change_24h=float(coin["price_change_percentage_24h"] or 0.0),
                    timestamp=datetime.utcnow()
                )

            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail="Erro ao comunicar com a API externa.")
            except httpx.RequestError:
                raise HTTPException(status_code=503, detail="Serviço externo temporariamente indisponível.")

    @staticmethod
    def save_crypto_price(db: Session, crypto_data: CryptoPriceResponse):
        """
        Recebe os dados processados e guarda-os na base de dados SQLite.
        """
        db_record = CryptoHistory(
            crypto_id=crypto_data.crypto_id,
            symbol=crypto_data.symbol,
            price_usd=crypto_data.price_usd,
            market_cap_usd=crypto_data.market_cap_usd,
            change_24h=crypto_data.change_24h,
            timestamp=crypto_data.timestamp
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record