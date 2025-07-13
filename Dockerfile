# Car Sales Dashboard Dockerfile
# Production-ready containerized deployment

# Use specific Python version to ensure reproducibility
FROM python:3.12.1-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    build-essential \
    redis-server \
    unzip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# Copy requirements and install Python dependencies
COPY requirements/production.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Create necessary directories for Reflex
RUN mkdir -p /home/appuser/.local/share/reflex && \
    chown -R appuser:appuser /home/appuser

USER appuser

# Create necessary directories
RUN mkdir -p logs assets /tmp/redis

# Initialize Reflex during build (downloads frontend dependencies)
RUN reflex init

# Set environment for Reflex
ENV REFLEX_ENV=prod

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=180s --retries=5 \
    CMD curl -f http://localhost:3000/healthz || exit 1

# Expose port
EXPOSE 3000

# Default command
CMD ["sh", "-c", "redis-server --port 6379 --bind 127.0.0.1 --dir /tmp/redis --daemonize yes && reflex run --env prod --host 0.0.0.0 --port 3000"]
