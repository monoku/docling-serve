FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_HTTP_TIMEOUT=1200 \
    DOCLING_SERVE_ENABLE_UI=true \
    PORT=5001

# Set build arguments with defaults
ARG UV_SYNC_EXTRA_ARGS="--no-extra cpu"

# Install system dependencies from os-packages.txt
# COPY os-packages.txt /tmp/
# RUN apt-get update && \
#     xargs -a /tmp/os-packages.txt apt-get install -y --no-install-recommends && \
#     rm -rf /var/lib/apt/lists/* && \
#     rm /tmp/os-packages.txt

# Install uv for Python package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY docling_serve ./docling_serve/

# Install Python dependencies with pip
# Note: Some packages might need to be pinned to specific versions for Python 3.12 compatibility
RUN pip install .

# Set the entrypoint to run the service
ENTRYPOINT ["docling-serve", "run", "--host", "0.0.0.0", "--port", "5001"]
