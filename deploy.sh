#!/bin/bash
# Production deployment script for Car Sales Dashboard
# This script handles the complete production deployment process

set -e  # Exit on any error

echo "🚀 Starting Car Sales Dashboard Production Deployment..."

# Configuration
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env.production"
BACKUP_DIR="./backups"
LOG_FILE="./logs/deployment.log"

# Create necessary directories
mkdir -p logs backups ssl

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if Docker is installed and running
    if ! command -v docker &> /dev/null; then
        log "ERROR: Docker is not installed"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log "ERROR: Docker is not running"
        exit 1
    fi
    
    # Check if Docker Compose is available
    if ! command -v docker-compose &> /dev/null; then
        log "ERROR: Docker Compose is not installed"
        exit 1
    fi
    
    # Check if environment file exists
    if [ ! -f "$ENV_FILE" ]; then
        log "WARNING: $ENV_FILE not found. Creating from template..."
        cp .env.production.template "$ENV_FILE"
        log "Please edit $ENV_FILE with your production settings before continuing"
        exit 1
    fi
    
    log "Prerequisites check passed ✅"
}

# Function to backup current deployment
backup_deployment() {
    if [ -d "data" ] || [ -d "logs" ]; then
        log "Creating backup..."
        BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$BACKUP_DIR/$BACKUP_NAME"
        
        # Backup data and logs
        [ -d "data" ] && cp -r data "$BACKUP_DIR/$BACKUP_NAME/"
        [ -d "logs" ] && cp -r logs "$BACKUP_DIR/$BACKUP_NAME/"
        
        log "Backup created: $BACKUP_DIR/$BACKUP_NAME ✅"
    fi
}

# Function to build and deploy
deploy() {
    log "Building application..."
    
    # Build the application
    docker-compose -f "$COMPOSE_FILE" build --no-cache
    
    log "Starting services..."
    
    # Start services
    docker-compose -f "$COMPOSE_FILE" up -d
    
    log "Deployment completed ✅"
}

# Function to verify deployment
verify_deployment() {
    log "Verifying deployment..."
    
    # Wait for services to be ready
    sleep 30
    
    # Check if services are running
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        log "Services are running ✅"
        
        # Test health endpoints
        if curl -f http://localhost:3000/health &> /dev/null; then
            log "Health check passed ✅"
        else
            log "WARNING: Health check failed ⚠️"
        fi
    else
        log "ERROR: Some services failed to start ❌"
        docker-compose -f "$COMPOSE_FILE" logs
        exit 1
    fi
}

# Function to show deployment info
show_info() {
    log "Deployment Information:"
    echo "=========================="
    echo "🌐 Frontend URL: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "💾 Redis: localhost:6379"
    echo "📋 Health Check: http://localhost:3000/health"
    echo "📊 Full Health Info: http://localhost:3000/healthz"
    echo "=========================="
    echo "📝 View logs: docker-compose logs -f"
    echo "🛑 Stop services: docker-compose down"
    echo "🔄 Restart: ./deploy.sh"
}

# Main deployment flow
main() {
    log "Car Sales Dashboard Production Deployment Started"
    
    check_prerequisites
    backup_deployment
    deploy
    verify_deployment
    show_info
    
    log "Deployment completed successfully! 🎉"
}

# Handle script arguments
case "${1:-}" in
    "stop")
        log "Stopping services..."
        docker-compose -f "$COMPOSE_FILE" down
        log "Services stopped ✅"
        ;;
    "restart")
        log "Restarting services..."
        docker-compose -f "$COMPOSE_FILE" restart
        log "Services restarted ✅"
        ;;
    "logs")
        docker-compose -f "$COMPOSE_FILE" logs -f
        ;;
    "status")
        docker-compose -f "$COMPOSE_FILE" ps
        ;;
    *)
        main
        ;;
esac
