"""
Client-side chart updater for Car Sales Dashboard.

This module provides client-side effects to update charts after page loads
to avoid EventHandler errors when directly using state methods in style props.
"""

import reflex as rx
from car_sales_dashboard.state import DashboardState

# Create a client-side effect to update the sales trend chart
sales_trend_chart_effect = rx.effect(
    lambda: DashboardState.get_sales_trend_chart(),
    dependencies=[
        DashboardState.forecast_data,
        DashboardState.active_tab
    ],
    handler=lambda result: rx.set_custom_value(
        id="sales-trend-chart",
        attribute="plotly_figure",
        value=result
    )
)

# Create a client-side effect to update the vehicle type chart
vehicle_type_chart_effect = rx.effect(
    lambda: DashboardState.get_vehicle_type_chart(),
    dependencies=[
        DashboardState.filtered_data,
        DashboardState.active_tab
    ],
    handler=lambda result: rx.set_custom_value(
        id="vehicle-type-chart",
        attribute="plotly_figure",
        value=result
    )
)

# Create a client-side effect to update the top models chart
top_models_chart_effect = rx.effect(
    lambda: DashboardState.get_top_models_chart(),
    dependencies=[
        DashboardState.filtered_data,
        DashboardState.active_tab
    ],
    handler=lambda result: rx.set_custom_value(
        id="top-models-chart",
        attribute="plotly_figure",
        value=result
    )
)

# Create a client-side effect to update the sales by month chart
sales_by_month_chart_effect = rx.effect(
    lambda: DashboardState.get_sales_by_month_chart(),
    dependencies=[
        DashboardState.filtered_data,
        DashboardState.active_tab
    ],
    handler=lambda result: rx.set_custom_value(
        id="sales-by-month-chart",
        attribute="plotly_figure",
        value=result
    )
)

# Create a client-side effect to update the region chart
region_chart_effect = rx.effect(
    lambda: DashboardState.get_region_chart(),
    dependencies=[
        DashboardState.filtered_data,
        DashboardState.active_tab
    ],
    handler=lambda result: rx.set_custom_value(
        id="region-chart",
        attribute="plotly_figure",
        value=result
    )
)

# Create a client-side effect to update the state map chart
state_map_chart_effect = rx.effect(
    lambda: DashboardState.get_state_map_chart(),
    dependencies=[
        DashboardState.filtered_data,
        DashboardState.active_tab
    ],
    handler=lambda result: rx.set_custom_value(
        id="state-map-chart",
        attribute="plotly_figure",
        value=result
    )
)

# Create a client-side effect to update the exogenous impact chart
exogenous_impact_chart_effect = rx.effect(
    lambda: DashboardState.get_exogenous_impact_chart(),
    dependencies=[
        DashboardState.forecast_data,
        DashboardState.active_tab
    ],
    handler=lambda result: rx.set_custom_value(
        id="exogenous-impact-chart",
        attribute="plotly_figure",
        value=result
    )
)

# Bundle all effects together for easy import
chart_client_effects = [
    sales_trend_chart_effect,
    vehicle_type_chart_effect,
    top_models_chart_effect,
    sales_by_month_chart_effect,
    region_chart_effect,
    state_map_chart_effect,
    exogenous_impact_chart_effect,
]
