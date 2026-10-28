# 📈 Data Pipeline & Crypto Tracker API

Uma API RESTful assíncrona desenvolvida em Python para rastrear, agregar e armazenar cotações de criptomoedas em tempo real. O projeto demonstra a criação de pipelines de dados em segundo plano utilizando boas práticas de engenharia de software.

## 🚀 Tecnologias Utilizadas

* **Python 3.11+** com tipagem estática
* **FastAPI:** Framework web moderno e de alto desempenho
* **Pydantic v2:** Validação de dados e gestão de configurações
* **SQLAlchemy 2.0:** ORM para interação com a base de dados SQLite
* **APScheduler:** Agendamento de tarefas em segundo plano (Background Jobs)
* **HTTPX:** Cliente HTTP assíncrono para consumo de APIs externas (CoinGecko)
* **Docker & Docker Compose:** Containerização para fácil distribuição

## ⚙️ Arquitetura

1. Um **Background Job** (APScheduler) é executado a cada 30 segundos.
2. Faz uma requisição assíncrona (`httpx`) à API pública da CoinGecko.
3. Os dados são validados (`Pydantic`) e guardados na base de dados (`SQLAlchemy`).
4. A **API REST** expõe endpoints para consultar o estado atual e o histórico guardado.

## 🛠️ Como Executar o Projeto

A forma mais fácil de correr o projeto é utilizando o Docker.

### Via Docker (Recomendado)
```bash
# Clone o repositório
git clone [https://github.com/yxngvitu-glitch/crypto-tracker-api.git](https://github.com/yxngvitu-glitch/crypto-tracker-api.git)
cd crypto-tracker-api

# Suba os contentores
docker-compose up --build