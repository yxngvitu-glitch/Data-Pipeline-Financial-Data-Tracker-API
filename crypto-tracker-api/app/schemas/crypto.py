from pydantic import BaseModel, Field
from datetime import datetime

class CryptoPriceResponse(BaseModel):
    crypto_id: str = Field(..., example="bitcoin", description="ID da criptomoeda")
    name: str = Field(..., example="Bitcoin")
    symbol: str = Field(..., example="btc")
    price_usd: float = Field(..., example=65000.50, description="Preço em USD")
    market_cap_usd: float = Field(..., example=1200000000000.0)
    change_24h: float = Field(..., example=2.5, description="Variação percentual em 24h")
    timestamp: datetime

    class Config:
        from_attributes = True