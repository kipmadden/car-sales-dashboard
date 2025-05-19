import reflex as rx
import pandas as pd
from car_sales_dashboard.state import DashboardState, df
from car_sales_dashboard.components.controls import sidebar_filters, exogenous_controls
from car_sales_dashboard.components.tables import create_summary_table, create_forecast_table
from car_sales_dashboard.components import chart_client_effects, responsive_chart_container

def index():
    """Main page of the dashboard"""
    unique_regions = sorted(df['region'].unique())
    unique_states = sorted(df['state'].unique())
    unique_vehicle_types = sorted(df['vehicle_type'].unique())
    unique_makes = sorted(df['make'].unique())
    unique_models = sorted(df['model'].unique())
    unique_years = sorted(str(int(year)) for year in df['model_year'].unique())
    
    # Include client-side effects to update charts
    for effect in chart_client_effects:
        rx.include(effect)

    return rx.container(
        rx.hstack(
            sidebar_filters(
                unique_regions,
                unique_states,
                unique_vehicle_types,
                unique_makes,
                unique_models,
                unique_years,
                DashboardState
            ),
            rx.vstack(
                rx.heading("Automotive Sales Forecast Dashboard", size="6"),
                rx.text(
                    "Explore the impact of exogenous factors on vehicle sales",
                    margin_bottom="1em",
                ),
                exogenous_controls(DashboardState),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Sales Forecast", value="sales", color="black"),
                        rx.tabs.trigger("Vehicle Analysis", value="vehicles", color="black"),
                        rx.tabs.trigger("Geographic", value="geographic", color="black"),
                        rx.tabs.trigger("Economic Factors", value="economic", color="black"),
                    ),
                    rx.tabs.content(
                        rx.vstack(                            # Use responsive chart container for sales trend chart
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
                                margin_top="2em",  # Increased margin
                                margin_bottom="1em",  # Added bottom margin
                                padding="0.5em",  # Added padding
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
                        rx.vstack(                            rx.hstack(                                responsive_chart_container(
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
                            ),                            responsive_chart_container(
                                title="Sales by Month and Vehicle Type",
                                chart_id="sales-by-month-chart",
                                height="400px"
                            ),
                            width="100%",                        ),
                        value="vehicles",
                    ),
                    rx.tabs.content(
                        rx.vstack(                            responsive_chart_container(
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
                        rx.vstack(                            responsive_chart_container(
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
                        value="economic",                    ),                    # Use default_value only to avoid issues with event handlers
                    default_value="sales",
                    orientation="horizontal",
                    width="100%",
                    variant="enclosed",
                    margin_top="1em",
                ),
                rx.text(
                    "Built with Reflex | Data is synthetic",
                    margin_top="2em",
                    font_size="sm",
                    color="gray",
                ),
            on_change=DashboardState.update_active_tab,
            ),
        ),
        padding="2em",
        max_width="1400px",
    )