# Import key components for easier access
from car_sales_dashboard.components.charts import (
    create_sales_trend_chart,
    create_vehicle_type_chart,
    create_region_chart,
    create_exogenous_impact_chart,
    create_top_models_chart,
    create_state_map_chart,
    create_heatmap_chart
)

from car_sales_dashboard.components.controls import (
    sidebar_filters,
    exogenous_controls,
    chart_container
)

from car_sales_dashboard.components.tables import (
    create_summary_table,
    create_forecast_table
)

# This makes it possible to import directly from the components package
# For example: from components import create_sales_trend_chart, sidebar_filters