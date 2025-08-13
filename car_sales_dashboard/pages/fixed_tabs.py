"""
Fixed tabs implementation for the dashboard.
This uses DashboardState chart functions for reactive, filtered charts.
"""
import reflex as rx
from car_sales_dashboard.state import DashboardState
from car_sales_dashboard.components.tables import create_forecast_table, create_summary_table


def create_tabs():
    """Create the tabs component using DashboardState chart functions for reactivity"""
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
                # Use DashboardState chart function for reactive sales trend
                rx.box(
                    rx.heading("Sales Trend and Forecast", color="black", size="4"),
                    rx.plotly(data=DashboardState.get_sales_trend_chart),
                    width="100%",
                    height="500px",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_bottom="1em",
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
                # Use rx.cond for conditional rendering
                rx.cond(
                    DashboardState.show_table,
                    create_forecast_table(DashboardState.forecast_data),
                    rx.text("")  # Empty placeholder when table is hidden
                ),
                width="100%",
            ),
            value="sales",
        ),
        rx.tabs.content(
            rx.vstack(
                rx.hstack(
                    # Use DashboardState chart functions for reactive vehicle analysis
                    rx.box(
                        rx.heading("Sales by Vehicle Type", color="black", size="4"),
                        rx.plotly(data=DashboardState.get_vehicle_type_chart),
                        width="48%",
                        height="400px",
                        padding="1.5em",
                        background="white",
                        border_radius="md",
                        border="1px solid #EEE",
                    ),
                    rx.box(
                        rx.heading("Top Models by Sales", color="black", size="4"),
                        rx.plotly(data=DashboardState.get_top_models_chart),
                        width="48%",
                        height="400px",
                        padding="1.5em",
                        background="white",
                        border_radius="md",
                        border="1px solid #EEE",
                    ),
                    width="100%",
                    gap="2%",
                ),
                # Monthly heatmap chart
                rx.box(
                    rx.heading("Sales by Month and Vehicle Type", color="black", size="4"),
                    rx.plotly(data=DashboardState.get_sales_by_month_chart),
                    width="100%",
                    height="400px",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
                ),
                width="100%",
            ),
            value="vehicles",
        ),
        rx.tabs.content(
            rx.vstack(
                # Use DashboardState chart functions for reactive geographic analysis
                rx.box(
                    rx.heading("Sales by Region", color="black", size="4"),
                    rx.plotly(data=DashboardState.get_region_chart),
                    width="100%",
                    height="400px",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_bottom="1em",
                ),
                rx.box(
                    rx.heading("Sales by State Map", color="black", size="4"),
                    rx.plotly(data=DashboardState.get_state_map_chart),
                    width="100%",
                    height="500px",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                ),
                width="100%",
            ),
            value="geographic",
        ),
        rx.tabs.content(
            rx.vstack(
                # Use DashboardState chart function for reactive exogenous variables
                rx.box(
                    rx.heading("Exogenous Variable Trends", color="black", size="4"),
                    rx.plotly(data=DashboardState.get_exogenous_figure),
                    width="100%",
                    height="500px",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                ),
                rx.box(
                    rx.heading("Exogenous Impact Analysis", color="black", size="4"),
                    rx.plotly(data=DashboardState.get_exogenous_impact_chart),
                    width="100%",
                    height="400px",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                ),
                width="100%",
            ),
            value="economic",
        ),
        # Named arguments after positional
        default_value="sales",
        width="100%",
    )
