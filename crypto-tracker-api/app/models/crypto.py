from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base
from datetime import datetime

class CryptoHistory(Base):
    __tablename__ = "crypto_history"

    id = Column(Integer, primary_key=True, index=True)
    crypto_id = Column(String, index=True)
    symbol = Column(String)
    price_usd = Column(Float)
    market_cap_usd = Column(Float)
    change_24h = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)