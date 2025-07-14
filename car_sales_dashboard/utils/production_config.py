"""Production monitoring and observability configuration."""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


class ProductionConfig:
    """Production configuration settings."""
    
    # Application settings
    APP_NAME = os.getenv("APP_NAME", "car-sales-dashboard")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
    WORKERS = int(os.getenv("WORKERS", "4"))
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
    
    # Monitoring
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "True").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "/app/logs/dashboard.log")
    ERROR_LOG_FILE = os.getenv("ERROR_LOG_FILE", "/app/logs/dashboard_errors.log")


def setup_logging(config: ProductionConfig) -> None:
    """Setup production logging configuration."""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(config.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - '
        '[%(filename)s:%(lineno)d] - PID:%(process)d'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for general logs
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = logging.FileHandler(config.ERROR_LOG_FILE)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # Suppress noisy loggers in production
    if not config.DEBUG:
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)


def setup_sentry(config: ProductionConfig) -> None:
    """Setup Sentry error tracking."""
    
    if config.SENTRY_DSN:
        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        )
        
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            integrations=[
                sentry_logging,
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=0.1,
            profiles_sample_rate=0.1,
            environment="production",
            release=config.APP_VERSION,
            before_send=filter_sentry_events,
        )
        
        logging.info("Sentry error tracking initialized")


def filter_sentry_events(event, hint):
    """Filter out noise from Sentry events."""
    
    # Filter out health check errors
    if 'request' in event and event['request'].get('url', '').endswith('/health'):
        return None
    
    # Filter out expected SSL/connection errors
    if 'exception' in event:
        exc_info = event['exception']['values'][0]
        if 'SSL' in exc_info.get('type', '') or 'ConnectionError' in exc_info.get('type', ''):
            return None
    
    return event


def setup_metrics(config: ProductionConfig) -> None:
    """Setup application metrics collection."""
    
    if config.ENABLE_METRICS:
        # This would integrate with Prometheus/Grafana in a real deployment
        logging.info("Metrics collection enabled")


class HealthChecker:
    """Health check utilities for production monitoring."""
    
    @staticmethod
    def check_dependencies() -> dict:
        """Check the health of external dependencies."""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Check Redis connectivity
        try:
            import redis
            redis_client = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=5)
            redis_client.ping()
            health_status["checks"]["redis"] = {"status": "healthy"}
        except Exception as e:
            health_status["checks"]["redis"] = {"status": "unhealthy", "error": str(e)}
            health_status["status"] = "degraded"
        
        # Check disk space
        try:
            import shutil
            disk_usage = shutil.disk_usage("/app")
            free_percent = (disk_usage.free / disk_usage.total) * 100
            
            if free_percent < 10:
                health_status["checks"]["disk"] = {"status": "critical", "free_percent": free_percent}
                health_status["status"] = "unhealthy"
            elif free_percent < 20:
                health_status["checks"]["disk"] = {"status": "warning", "free_percent": free_percent}
                health_status["status"] = "degraded"
            else:
                health_status["checks"]["disk"] = {"status": "healthy", "free_percent": free_percent}
        except Exception as e:
            health_status["checks"]["disk"] = {"status": "unknown", "error": str(e)}
        
        # Check memory usage
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            if memory.percent > 90:
                health_status["checks"]["memory"] = {"status": "critical", "usage_percent": memory.percent}
                health_status["status"] = "unhealthy"
            elif memory.percent > 80:
                health_status["checks"]["memory"] = {"status": "warning", "usage_percent": memory.percent}
                health_status["status"] = "degraded"
            else:
                health_status["checks"]["memory"] = {"status": "healthy", "usage_percent": memory.percent}
        except Exception as e:
            health_status["checks"]["memory"] = {"status": "unknown", "error": str(e)}
        
        return health_status


def initialize_production_environment():
    """Initialize the production environment with all configurations."""
    
    config = ProductionConfig()
    
    # Setup logging first
    setup_logging(config)
    logging.info(f"Starting {config.APP_NAME} v{config.APP_VERSION} in production mode")
    
    # Setup error tracking
    setup_sentry(config)
    
    # Setup metrics
    setup_metrics(config)
    
    # Log configuration (without sensitive data)
    logging.info(f"Host: {config.HOST}:{config.FRONTEND_PORT}")
    logging.info(f"Debug mode: {config.DEBUG}")
    logging.info(f"Workers: {config.WORKERS}")
    logging.info("Production environment initialized successfully")
    
    return config


if __name__ == "__main__":
    # Initialize production environment
    config = initialize_production_environment()
    
    # Run health check
    health_checker = HealthChecker()
    health_status = health_checker.check_dependencies()
    
    print(f"Health Status: {health_status}")
