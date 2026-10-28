# Usa uma imagem oficial do Python, leve e segura
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contentor
WORKDIR /app

# Impede o Python de gravar ficheiros .pyc e força o log no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copia os ficheiros de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o contentor
COPY . .

# Expõe a porta que o FastAPI vai utilizar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]