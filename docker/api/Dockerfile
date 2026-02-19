FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema para SASL/Thrift
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libsasl2-dev \
    libsasl2-modules && \
    rm -rf /var/lib/apt/lists/*

# Dependencias Python
# 1. Instalar pure-sasl primero (pura Python, sin C++)
# 2. Instalar pyhive SIN el extra [hive] para evitar que arrastre
#    el paquete C 'sasl' que no compila en Python 3.11
RUN pip install --no-cache-dir pure-sasl==0.6.2 && \
    pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn==0.27.0 \
    pyhive==0.7.0 \
    thrift==0.16.0 \
    thrift-sasl==0.4.3 \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0

CMD ["uvicorn", "src.serving.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]