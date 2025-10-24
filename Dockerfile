# Project: EPT-MX-ADM
# Company: EasyProTech LLC (www.easypro.tech)
# Dev: Brabus
# Date: Fri 24 Oct 2025 UTC
# Status: Created
# Telegram: https://t.me/EasyProTech

FROM python:3.10-slim

LABEL maintainer="EasyProTech LLC <mail.easypro.tech@gmail.com>"
LABEL description="EPT-MX-ADM - Matrix Synapse Administration Panel"
LABEL version="1.0.1"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN useradd -r -s /bin/bash -u 1000 -U matrix-admin

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=matrix-admin:matrix-admin . .

# Download static assets
RUN chmod +x install_assets.sh && \
    ./install_assets.sh && \
    chown -R matrix-admin:matrix-admin static/

# Create logs directory
RUN mkdir -p logs && chown -R matrix-admin:matrix-admin logs/

# Switch to non-root user
USER matrix-admin

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/login || exit 1

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]

