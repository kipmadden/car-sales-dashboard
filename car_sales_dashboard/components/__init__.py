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

# Import the fixed chart components
from car_sales_dashboard.components.chart_fix import (
    chart_container_v2,
    plotly_chart,
    create_empty_chart
)

# Import client-side chart effects
# Chart client effects are now implemented directly in index.py

# Import the responsive chart container
from car_sales_dashboard.components.chart_components import (
    responsive_chart_container
)

from car_sales_dashboard.components.tables import (
    create_summary_table,
    create_forecast_table
)

# from car_sales_dashboard.components.exogenous_chart import (
#     create_exogenous_chart
# )

# This makes it possible to import directly from the components package
# For example: from components import create_sales_trend_chart, sidebar_filters