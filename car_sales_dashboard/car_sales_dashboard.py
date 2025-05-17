"""Main entry point for the Car Sales Dashboard Reflex application."""
import reflex as rx

# Import the index page from the pages module
from car_sales_dashboard.pages import index

# Create the app
app = rx.App()

# Add the index page to the app
app.add_page(index, title="Auto Sales Forecast Dashboard")

# Start the app if run directly
if __name__ == "__main__":
    app.compile()