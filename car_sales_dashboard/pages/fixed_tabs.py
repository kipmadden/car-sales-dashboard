# This file contains the fixed tabs implementation
import reflex as rx
from car_sales_dashboard.state import DashboardState
from car_sales_dashboard.components import responsive_chart_container
from car_sales_dashboard.components.tables import create_forecast_table, create_summary_table

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
                responsive_chart_container(
                    title="Sales Trend and Forecast",
                    chart_id="sales-trend-chart",
                    height="500px"
                ),
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
        ),
        rx.tabs.content(
            rx.vstack(
                rx.hstack(
                    responsive_chart_container(
                        title="Sales by Vehicle Type",
                        chart_id="vehicle-type-chart",
                        height="400px"
                    ),
                    responsive_chart_container(
                        title="Top Models by Sales",
                        chart_id="top-models-chart",
                        height="400px"
                    ),
                    width="100%",
                ),
                responsive_chart_container(
                    title="Sales by Month and Vehicle Type",
                    chart_id="sales-by-month-chart",
                    height="400px"
                ),
                width="100%",
            ),
            value="vehicles",
        ),
        rx.tabs.content(
            rx.vstack(
                responsive_chart_container(
                    title="Sales by Region",
                    chart_id="region-chart",
                    height="400px"
                ),
                responsive_chart_container(
                    title="Sales by State", 
                    chart_id="state-map-chart",
                    height="500px"
                ),
                width="100%",
            ),
            value="geographic",
        ),
        rx.tabs.content(
            rx.vstack(
                responsive_chart_container(
                    title="Exogenous Variable Trends",
                    chart_id="exogenous-impact-chart",
                    height="500px"
                ),
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
