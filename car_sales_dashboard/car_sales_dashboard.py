"""Main entry point for the Car Sales Dashboard Reflex application."""
import reflex as rx
from datetime import datetime

# Import the index page from the pages module
from car_sales_dashboard.pages import index

# Health check endpoint
def health_check():
    """Health check endpoint for monitoring and Docker health checks."""
    return rx.box(
        rx.heading("Health Check", size="6"),
        rx.text(f"Status: OK"),
        rx.text(f"Timestamp: {datetime.now().isoformat()}"),
        rx.text("Service: Car Sales Dashboard"),
        rx.text("Version: 1.0.0"),
        padding="2em",
        background="white"
    )

def health_simple():
    """Simple health check endpoint for load balancers."""
    return rx.text("OK")

# Create the app
app = rx.App()

# Add pages to the app
app.add_page(index, title="Auto Sales Forecast Dashboard")
app.add_page(health_check, route="/healthz")
app.add_page(health_simple, route="/health")

# Start the app if run directly
if __name__ == "__main__":
    app.compile()