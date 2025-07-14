@echo off
REM Production deployment script for Car Sales Dashboard (Windows)
REM This script handles the complete production deployment process

setlocal EnableDelayedExpansion

echo 🚀 Starting Car Sales Dashboard Production Deployment...

REM Configuration
set COMPOSE_FILE=docker-compose.yml
set ENV_FILE=.env.production
set BACKUP_DIR=.\backups
set LOG_FILE=.\logs\deployment.log

REM Create necessary directories
if not exist logs mkdir logs
if not exist backups mkdir backups
if not exist ssl mkdir ssl

REM Function to log messages
:log
echo %date% %time% - %~1 >> "%LOG_FILE%"
echo %date% %time% - %~1
goto :eof

REM Check prerequisites
call :log "Checking prerequisites..."

REM Check if Docker is installed and running
docker --version >nul 2>&1
if errorlevel 1 (
    call :log "ERROR: Docker is not installed"
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    call :log "ERROR: Docker is not running"
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :log "ERROR: Docker Compose is not installed"
    pause
    exit /b 1
)

REM Check if environment file exists
if not exist "%ENV_FILE%" (
    call :log "WARNING: %ENV_FILE% not found. Creating from template..."
    copy .env.production.template "%ENV_FILE%"
    call :log "Please edit %ENV_FILE% with your production settings before continuing"
    pause
    exit /b 1
)

call :log "Prerequisites check passed ✅"

REM Backup current deployment
if exist data (
    call :log "Creating backup..."
    set BACKUP_NAME=backup_%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set BACKUP_NAME=!BACKUP_NAME: =0!
    mkdir "%BACKUP_DIR%\!BACKUP_NAME!"
    
    if exist data xcopy data "%BACKUP_DIR%\!BACKUP_NAME!\data" /E /I /Q
    if exist logs xcopy logs "%BACKUP_DIR%\!BACKUP_NAME!\logs" /E /I /Q
    
    call :log "Backup created: %BACKUP_DIR%\!BACKUP_NAME! ✅"
)

REM Build and deploy
call :log "Building application..."
docker-compose -f "%COMPOSE_FILE%" build --no-cache

call :log "Starting services..."
docker-compose -f "%COMPOSE_FILE%" up -d

call :log "Deployment completed ✅"

REM Verify deployment
call :log "Verifying deployment..."
timeout /t 30 /nobreak >nul

REM Check if services are running
docker-compose -f "%COMPOSE_FILE%" ps | findstr "Up" >nul
if errorlevel 1 (
    call :log "ERROR: Some services failed to start ❌"
    docker-compose -f "%COMPOSE_FILE%" logs
    pause
    exit /b 1
) else (
    call :log "Services are running ✅"
)

REM Test health endpoint
curl -f http://localhost:3000/health >nul 2>&1
if errorlevel 1 (
    call :log "WARNING: Health check failed ⚠️"
) else (
    call :log "Health check passed ✅"
)

REM Show deployment info
call :log "Deployment Information:"
echo ==========================
echo 🌐 Frontend URL: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 💾 Redis: localhost:6379
echo 📋 Health Check: http://localhost:3000/health
echo 📊 Full Health Info: http://localhost:3000/healthz
echo ==========================
echo 📝 View logs: docker-compose logs -f
echo 🛑 Stop services: docker-compose down
echo 🔄 Restart: deploy.bat

call :log "Deployment completed successfully! 🎉"
pause
