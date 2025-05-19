import reflex as rx
import pandas as pd
from car_sales_dashboard.state import DashboardState, df
from car_sales_dashboard.components.controls import sidebar_filters, exogenous_controls
from car_sales_dashboard.components.tables import create_summary_table, create_forecast_table
from car_sales_dashboard.components import responsive_chart_container
from car_sales_dashboard.pages.fixed_tabs import create_tabs

def index():
    """Main page of the dashboard"""
    unique_regions = sorted(df['region'].unique())
    unique_states = sorted(df['state'].unique())
    unique_vehicle_types = sorted(df['vehicle_type'].unique())
    unique_makes = sorted(df['make'].unique())
    unique_models = sorted(df['model'].unique())
    unique_years = sorted(str(int(year)) for year in df['model_year'].unique())
    
    # Create client-side effects for chart updates
    # Sales trend chart effect
    rx.include(rx.effect(
        lambda: DashboardState.get_sales_trend_chart(),
        dependencies=[DashboardState.forecast_data, DashboardState.active_tab],
        handler=lambda result: rx.set_custom_value(
            id="sales-trend-chart",
            attribute="plotly_figure",
            value=result
        )
    ))
    
    # Vehicle type chart effect
    rx.include(rx.effect(
        lambda: DashboardState.get_vehicle_type_chart(),
        dependencies=[DashboardState.filtered_data, DashboardState.active_tab],
        handler=lambda result: rx.set_custom_value(
            id="vehicle-type-chart",
            attribute="plotly_figure",
            value=result
        )
    ))
    
    # Top models chart effect
    rx.include(rx.effect(
        lambda: DashboardState.get_top_models_chart(),
        dependencies=[DashboardState.filtered_data, DashboardState.active_tab],
        handler=lambda result: rx.set_custom_value(
            id="top-models-chart",
            attribute="plotly_figure",
            value=result
        )
    ))
    
    # Other chart effects
    rx.include(rx.effect(
        lambda: DashboardState.get_sales_by_month_chart(),
        dependencies=[DashboardState.filtered_data, DashboardState.active_tab],
        handler=lambda result: rx.set_custom_value(
            id="sales-by-month-chart",
            attribute="plotly_figure",
            value=result
        )
    ))
    
    rx.include(rx.effect(
        lambda: DashboardState.get_region_chart(),
        dependencies=[DashboardState.filtered_data, DashboardState.active_tab],
        handler=lambda result: rx.set_custom_value(
            id="region-chart", 
            attribute="plotly_figure",
            value=result
        )
    ))
    
    rx.include(rx.effect(
        lambda: DashboardState.get_state_map_chart(),
        dependencies=[DashboardState.filtered_data, DashboardState.active_tab],
        handler=lambda result: rx.set_custom_value(
            id="state-map-chart",
            attribute="plotly_figure",
            value=result
        )
    ))
    
    rx.include(rx.effect(
        lambda: DashboardState.get_exogenous_impact_chart(),
        dependencies=[DashboardState.forecast_data, DashboardState.active_tab],
        handler=lambda result: rx.set_custom_value(
            id="exogenous-impact-chart",
            attribute="plotly_figure",
            value=result
        )
    ))

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
                ),                exogenous_controls(DashboardState),                # Use the fixed tabs component which has correct positioning of arguments
                create_tabs(),
                rx.text(
                    "Built with Reflex | Data is synthetic",
                    margin_top="2em",
                    font_size="sm",
                    color="gray",
                ),            ),
        ),
        padding="2em",
        max_width="1400px",
    )