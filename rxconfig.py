import reflex as rx
import os

# Initialize logging before anything else
from car_sales_dashboard.utils.logging_config import setup_logging

# Setup logging based on environment
debug_mode = os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes', 'on')
setup_logging(debug_mode=debug_mode)

# Configuration for the Reflex app
config = rx.Config(
    app_name="car_sales_dashboard",
    db_url="sqlite:///auto_sales.db",
    env=rx.Env.DEV,
    state_serializer="dill",
)