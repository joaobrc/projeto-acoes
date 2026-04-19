# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar poetry e dependências
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only=main --no-root --no-interaction --no-ansi

# Stage 2: Runtime
FROM python:3.13-slim

WORKDIR /app

# Copiar pacotes Python do builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código fonte
COPY src/ ./src/
COPY alembic.ini ./
COPY entrypoint.sh ./
COPY migracao/ ./migracao/

# Tornar entrypoint executável e criar usuário não-root
RUN chmod +x entrypoint.sh && \
    useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expor porta do Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501')" || exit 1

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Comando padrão
CMD ["./entrypoint.sh"]
