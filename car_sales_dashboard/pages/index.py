import reflex as rx
import pandas as pd
from car_sales_dashboard.state import DashboardState , df
from car_sales_dashboard.components.controls import sidebar_filters, exogenous_controls, chart_container
from car_sales_dashboard.components.tables import create_summary_table, create_forecast_table


def index():
    """Main page of the dashboard"""
    # Get unique values for filters
    unique_regions = sorted(df['region'].unique())
    unique_states = sorted(df['state'].unique())
    unique_vehicle_types = sorted(df['vehicle_type'].unique())
    unique_makes = sorted(df['make'].unique())
    unique_models = sorted(df['model'].unique())
    # Convert years to strings for dropdown compatibility
    unique_years = sorted(str(int(year)) for year in df['model_year'].unique())
    
    # Create page layout
    return rx.container(
        rx.hstack(
            # Left sidebar with filters
            sidebar_filters(
                unique_regions, 
                unique_states, 
                unique_vehicle_types,
                unique_makes, 
                unique_models, 
                unique_years,
                DashboardState
            ),
            
            # Main content
            rx.vstack(
                rx.heading("Automotive Sales Forecast Dashboard", size="6"),
                rx.text(
                    "Explore the impact of exogenous factors on vehicle sales",
                    margin_bottom="1em",
                ),
                
                # Exogenous variable controls
                exogenous_controls(DashboardState),
                
                # Tabs for different views
                rx.tabs(
                    tabs=[
                        rx.tab("Sales Forecast", id="sales", on_click=lambda: DashboardState.set_active_tab("sales")),
                        rx.tab("Vehicle Analysis", id="vehicles", on_click=lambda: DashboardState.set_active_tab("vehicles")),
                        rx.tab("Geographic", id="geographic", on_click=lambda: DashboardState.set_active_tab("geographic")),
                        rx.tab("Economic Factors", id="economic", on_click=lambda: DashboardState.set_active_tab("economic")),
                    ],
                    panels=[
                        rx.tab_panel(
                            rx.vstack(
                                # Main sales trend and forecast chart
                                chart_container(
                                    "Sales Trend and Forecast",
                                    get_sales_trend_chart(),
                                    height="500px"
                                ),
                                
                                # Toggle for forecast table
                                rx.hstack(
                                    rx.switch(
                                        on_change=DashboardState.toggle_table,
                                        is_checked=DashboardState.show_table
                                    ),
                                    rx.text("Show Forecast Table"),
                                    margin_top="1em",
                                ),
                                
                                # Conditional forecast table
                                rx.cond(
                                    DashboardState.show_table,
                                    create_forecast_table(pd.DataFrame(DashboardState.forecast_data)),
                                    rx.text("")
                                ),
                                
                                width="100%",
                            ),
                            id="sales-panel",
                        ),
                        
                        rx.tab_panel(
                            rx.vstack(
                                rx.hstack(
                                    # Vehicle type chart
                                    chart_container(
                                        "Sales by Vehicle Type",
                                        get_vehicle_type_chart(),
                                        height="400px"
                                    ),
                                    
                                    # Top models chart
                                    chart_container(
                                        "Top Models by Sales",
                                        get_top_models_chart(),
                                        height="400px"
                                    ),
                                    
                                    width="100%",
                                ),
                                
                                # Sales heatmap
                                chart_container(
                                    "Sales by Month and Vehicle Type",
                                    get_sales_by_month_chart(),
                                    height="400px"
                                ),
                                
                                width="100%",
                            ),
                            id="vehicles-panel",
                        ),
                        
                        rx.tab_panel(
                            rx.vstack(
                                # Region chart
                                chart_container(
                                    "Sales by Region",
                                    get_region_chart(),
                                    height="400px"
                                ),
                                
                                # State map
                                chart_container(
                                    "Sales by State",
                                    get_state_map_chart(),
                                    height="500px"
                                ),
                                
                                width="100%",
                            ),
                            id="geographic-panel",
                        ),
                        
                        rx.tab_panel(
                            rx.vstack(
                                # Exogenous variable impact
                                chart_container(
                                    "Exogenous Variable Trends",
                                    get_exogenous_impact_chart(),
                                    height="500px"
                                ),
                                
                                # Summary table
                                rx.box(
                                    create_summary_table(
                                        pd.DataFrame(DashboardState.filtered_data),
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
                            id="economic-panel",
                        ),
                    ],
                    width="100%",
                    variant="enclosed",
                    margin_top="1em",
                ),
                
                # Footer with attribution
                rx.text(
                    "Built with Reflex | Data is synthetic",
                    margin_top="2em",
                    font_size="sm",
                    color="gray",
                ),
                
                width="100%",
                spacing="4",
            ),
            align_items="start",
            width="100%",
        ),
        padding="2em",
        max_width="1400px",
    )