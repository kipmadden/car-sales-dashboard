import reflex as rx
import os

# Initialize logging before anything else
from car_sales_dashboard.utils.logging_config import setup_logging

# Setup logging based on environment
debug_mode = os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes', 'on')
setup_logging(debug_mode=debug_mode)

# =============================================================================
# Data Generation Configuration (S5 Remediation)
# =============================================================================

# Default seed for reproducible synthetic data generation
DEFAULT_SEED = int(os.getenv('SYNTHETIC_DATA_SEED', '42'))

# Realistic bounds for exogenous variables
DATA_BOUNDS = {
    'sales': {'min': 500, 'max': 50000},  # Individual model sales per month
    'unemployment': {'min': 2.0, 'max': 12.0},  # US unemployment rate %
    'gas_price': {'min': 1.50, 'max': 6.00},  # US gas price per gallon
    'cpi_energy': {'min': 150, 'max': 350},  # Energy CPI index
    'cpi_all': {'min': 200, 'max': 320},  # All items CPI index
    'search_volume': {'min': 20, 'max': 120},  # Relative search interest (0-100+)
}

# Configuration for the Reflex app
config = rx.Config(
    app_name="car_sales_dashboard",
    db_url="sqlite:///auto_sales.db",
    env=rx.Env.PROD if os.getenv('REFLEX_ENV') == 'prod' else rx.Env.DEV,
    state_serializer="dill",
    # Redis configuration for production
    redis_host=os.getenv('REDIS_HOST', 'localhost'),
    redis_port=int(os.getenv('REDIS_PORT', '6379')),
    # Network configuration for Docker deployment
    backend_host="0.0.0.0" if os.getenv('REFLEX_ENV') == 'prod' else "127.0.0.1",
    backend_port=8000,
    frontend_port=3000,
)