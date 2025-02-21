# Usa Python 3.12 como base
FROM python:3.12-slim

# Evita la generación de archivos .pyc y usa salida no bloqueante
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_HTTP_TIMEOUT=1200 \
    DOCLING_SERVE_ENABLE_UI=true \
    PORT=8000

# Define argumentos de compilación
ARG UV_SYNC_EXTRA_ARGS="--no-extra cpu"

# Instala dependencias del sistema necesarias (descomentar si es necesario)
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     curl && \
#     rm -rf /var/lib/apt/lists/*

# Instala `uv` para la gestión de paquetes
RUN curl -fsSL https://astral.sh/uv/install.sh | sh

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia archivos de dependencias primero para aprovechar la caché de Docker
COPY pyproject.toml README.md ./

# Instala dependencias de Python
RUN pip install --no-cache-dir .

# Copia el código de la aplicación
COPY docling_serve ./docling_serve/

# Crea un usuario sin privilegios para ejecutar el contenedor
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser

# Expone el puerto correcto
EXPOSE 8000

# Usa ENTRYPOINT para mayor flexibilidad
ENTRYPOINT ["python", "docling_serve/runpod_handler.py"]
