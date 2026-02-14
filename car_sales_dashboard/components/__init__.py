"""
Main components package for the Car Sales Dashboard.

This package provides a clean public API for all dashboard components.
"""

# Core chart functions - single source of truth
from car_sales_dashboard.components.charts import (
    create_sales_trend_chart,
    create_exogenous_variables_chart,
    create_vehicle_type_chart,
    create_region_chart,
    create_top_models_chart,
    create_state_map_chart,
    create_heatmap_chart,
    chart_container,
    generate_sample_data
)

# Legacy aliases for backward compatibility
from car_sales_dashboard.components.charts import (
    create_exogenous_variables_chart as create_exogenous_impact_chart
)

# Control components
from car_sales_dashboard.components.controls import (
    sidebar_filters,
    exogenous_controls
)

# Table components
from car_sales_dashboard.components.tables import (
    create_summary_table,
    create_forecast_table
)

# Public API - these are the only functions that should be imported elsewhere
__all__ = [
    # Chart functions
    'create_sales_trend_chart',
    'create_exogenous_variables_chart',
    'create_vehicle_type_chart',
    'create_region_chart',
    'create_top_models_chart',
    'create_state_map_chart',
    'create_heatmap_chart',
    'chart_container',
    
    # Control functions
    'sidebar_filters',
    'exogenous_controls',
    
    # Table functions
    'create_summary_table',
    'create_forecast_table',
    
    # Utilities
    'generate_sample_data',
    
    # Legacy aliases
    'create_exogenous_impact_chart'
]