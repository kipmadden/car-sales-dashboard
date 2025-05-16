import reflex as rx

# Configuration for the Reflex app
config = rx.Config(
    app_name="car_sales_dashboard",
    db_url="sqlite:///auto_sales.db",
    env=rx.Env.DEV,
)