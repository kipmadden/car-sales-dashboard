"""
Fixed tabs implementation for the dashboard.
This resolves issues with argument ordering in tabs component.
"""
import reflex as rx
from car_sales_dashboard.state import DashboardState
from car_sales_dashboard.components.tables import create_forecast_table, create_summary_table

def create_simple_chart_container(title: str, height: str = "400px"):
    """Create a simple chart container without reactive chart data."""
    return rx.box(
        rx.heading(title, color="black", size="4"),
        rx.center(
            rx.text("Chart loading... Please refresh the page after initial load.", color="gray"),
            height=height,
            width="100%",
        ),
        width="100%",
        padding="1.5em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        margin_top="1.5em",
        margin_bottom="1.5em",
    )

def create_tabs():
    """Create the tabs component with correct argument ordering"""
    return rx.tabs.root(
        # All positional arguments first
        rx.tabs.list(
            rx.tabs.trigger("Sales Forecast", value="sales", color="black"),
            rx.tabs.trigger("Vehicle Analysis", value="vehicles", color="black"),
            rx.tabs.trigger("Geographic", value="geographic", color="black"),
            rx.tabs.trigger("Economic Factors", value="economic", color="black"),
        ),
        rx.tabs.content(
            rx.vstack(
                create_simple_chart_container("Sales Trend and Forecast", height="500px"),
                rx.box(height="20px"),  # Add space between chart and controls
                rx.hstack(
                    rx.switch(
                        on_change=DashboardState.toggle_table,
                        is_checked=DashboardState.show_table
                    ),
                    rx.text("Show Forecast Table", color="black"),
                    margin_top="2em",
                    margin_bottom="1em",
                    padding="0.5em",
                ),
                rx.cond(
                    DashboardState.show_table,
                    create_forecast_table(DashboardState.forecast_data),
                    rx.text("")
                ),
                width="100%",
            ),
            value="sales",
        ),        rx.tabs.content(
            rx.vstack(
                rx.hstack(
                    create_simple_chart_container("Sales by Vehicle Type"),
                    create_simple_chart_container("Top Models by Sales"),
                    width="100%",
                ),
                create_simple_chart_container("Sales by Month and Vehicle Type"),
                width="100%",
            ),
            value="vehicles",
        ),        rx.tabs.content(
            rx.vstack(
                create_simple_chart_container("Sales by Region"),
                create_simple_chart_container("Sales by State", height="500px"),width="100%",
            ),
            value="geographic",
        ),        rx.tabs.content(
            rx.vstack(
                create_simple_chart_container("Exogenous Variable Trends", height="500px"),
                rx.box(
                    create_summary_table(
                        DashboardState.filtered_data,
                        groupby_col='vehicle_type'
                    ),
                    width="100%",
                    padding="1em", 
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1em",
                ),
                width="100%",
            ),
            value="economic",
        ),
        # Then all keyword arguments
        on_change=DashboardState.update_active_tab,
        default_value="sales",
        orientation="horizontal",
        width="100%",
        variant="enclosed",
        margin_top="1em",
    )
