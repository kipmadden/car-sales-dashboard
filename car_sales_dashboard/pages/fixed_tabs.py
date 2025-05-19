# This file contains the fixed tabs implementation
import reflex as rx
from car_sales_dashboard.state import DashboardState
from car_sales_dashboard.components.static_charts import create_static_chart
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
                # Create charts by passing title as a prop, not calling functions directly
                rx.fragment(
                    rx.heading("Sales Trend and Forecast", color="black", size="4"),
                    rx.center(
                        rx.plotly(
                            figure=DashboardState.get_sales_trend_chart,
                            height="500px",
                            width="100%",
                        ),
                        height="500px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
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
                    # Direct integration of charts with Vars
                    rx.fragment(
                        rx.heading("Sales by Vehicle Type", color="black", size="4"),
                        rx.center(
                            rx.plotly(
                                figure=DashboardState.get_vehicle_type_chart,
                                height="400px",
                                width="100%",
                            ),
                            height="400px",
                            width="100%",
                        ),
                        width="100%",
                        padding="1.5em",
                        background="white",
                        border_radius="md",
                        border="1px solid #EEE",
                        margin_top="1.5em",
                        margin_bottom="1.5em",
                    ),
                    rx.fragment(
                        rx.heading("Top Models by Sales", color="black", size="4"),
                        rx.center(
                            rx.plotly(
                                figure=DashboardState.get_top_models_chart,
                                height="400px",
                                width="100%",
                            ),
                            height="400px",
                            width="100%",
                        ),
                        width="100%",
                        padding="1.5em",
                        background="white",
                        border_radius="md",
                        border="1px solid #EEE",
                        margin_top="1.5em",
                        margin_bottom="1.5em",
                    ),
                    width="100%",
                ),
                rx.fragment(
                    rx.heading("Sales by Month and Vehicle Type", color="black", size="4"),
                    rx.center(
                        rx.plotly(
                            figure=DashboardState.get_sales_by_month_chart,
                            height="400px",
                            width="100%",
                        ),
                        height="400px",
                        width="100%",
                    ),
                    width="100%",
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
                rx.fragment(
                    rx.heading("Sales by Region", color="black", size="4"),
                    rx.center(
                        rx.plotly(
                            figure=DashboardState.get_region_chart,
                            height="400px",
                            width="100%",
                        ),
                        height="400px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
                ),
                rx.fragment(
                    rx.heading("Sales by State", color="black", size="4"),
                    rx.center(
                        rx.plotly(
                            figure=DashboardState.get_state_map_chart,
                            height="500px",
                            width="100%",
                        ),
                        height="500px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
                ),
                width="100%",
            ),
            value="geographic",
        ),
        rx.tabs.content(
            rx.vstack(
                rx.fragment(
                    rx.heading("Exogenous Variable Trends", color="black", size="4"),
                    rx.center(
                        rx.plotly(
                            figure=DashboardState.get_exogenous_impact_chart,
                            height="500px",
                            width="100%",
                        ),
                        height="500px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white", 
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
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
