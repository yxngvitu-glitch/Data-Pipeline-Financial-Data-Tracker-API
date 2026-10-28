import asyncio
from app.core.database import SessionLocal
from app.services.crypto_service import CryptoService

async def fetch_and_store_crypto_data():
    """
    Tarefa em segundo plano que vai buscar os preços e os guarda na base de dados.
    Como corre fora das rotas da API, precisamos de abrir e fechar a sessão da base de dados manualmente.
    """
    db = SessionLocal()
    try:
        # Pode adicionar mais moedas aqui se quiser, mas vamos começar com o bitcoin
        crypto_id = "bitcoin"
        crypto_data = await CryptoService.fetch_crypto_price(crypto_id)
        
        CryptoService.save_crypto_price(db, crypto_data)
        
        # Imprime no terminal para sabermos que está a funcionar
        print(f"🔄 [{crypto_data.timestamp.strftime('%H:%M:%S')}] {crypto_id.capitalize()} guardado com sucesso: ${crypto_data.price_usd}")
        
    except Exception as e:
        print(f"❌ Erro na tarefa automática: {e}")
    finally:
        db.close()