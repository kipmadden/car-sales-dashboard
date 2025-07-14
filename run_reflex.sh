#!/bin/bash
# Car Sales Dashboard - Reflex Runner with SSL Fix (Unix/Linux/WSL)
# This script fixes SSL certificate issues

echo "Starting Car Sales Dashboard..."

# Fix SSL certificate path using certifi
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")

# Verify certificate file exists
if [ ! -f "$SSL_CERT_FILE" ]; then
    echo "Error: SSL certificate file not found at $SSL_CERT_FILE"
    echo "Please ensure certifi is installed: pip install certifi"
    exit 1
fi

echo "Using SSL certificate: $SSL_CERT_FILE"

# Set Reflex environment
export REFLEX_ENV=dev

# Run Reflex with proper SSL configuration
echo "Running: reflex run"
reflex run
