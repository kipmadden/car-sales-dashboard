@echo off
REM Car Sales Dashboard - Reflex Runner with SSL Fix
REM This script fixes SSL certificate issues on Windows

echo Starting Car Sales Dashboard...

REM Fix SSL certificate path
set SSL_CERT_FILE=C:\Users\kip.madden\AppData\Local\anaconda3\envs\AI-102\Lib\site-packages\certifi\cacert.pem

REM Verify certificate file exists
if not exist "%SSL_CERT_FILE%" (
    echo Error: SSL certificate file not found at %SSL_CERT_FILE%
    echo Please ensure certifi is installed: pip install certifi
    pause
    exit /b 1
)

echo Using SSL certificate: %SSL_CERT_FILE%

REM Set Reflex environment
set REFLEX_ENV=dev

REM Run Reflex with proper SSL configuration
echo Running: reflex run
reflex run

pause
