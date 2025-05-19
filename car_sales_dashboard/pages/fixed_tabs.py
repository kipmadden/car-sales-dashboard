"""
Fixed tabs implementation for the dashboard.
This resolves issues with argument ordering in tabs component.
"""
import reflex as rx
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from car_sales_dashboard.state import DashboardState, df
from car_sales_dashboard.components.tables import create_forecast_table, create_summary_table
from car_sales_dashboard.components.exogenous_chart import create_exogenous_chart

# Create basic chart functions directly here to avoid circular imports
def create_simple_bar_chart(title: str, x_values, y_values, height: str = "400px"):
    """Create a simple bar chart with the provided data."""
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=x_values,
            y=y_values,
            marker_color='rgb(55, 83, 109)'
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="",
        yaxis_title="Sales",
        font=dict(color="black"),
        plot_bgcolor='#E5ECF6',  # Light blue/gray background
        paper_bgcolor='white',
    )
    
    # Add grid lines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='white',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='white'
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='white',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='white'
    )
      # Use the figure object directly with rx.plotly
    return rx.box(
        rx.heading(title, color="black", size="4"),
        rx.center(
            rx.plotly(data=fig),  # Pass the figure object using the fig parameter
            height=height,
            width="100%",
        ),
        width="100%",
        padding="1.5em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        margin_top="1.5em",
        margin_bottom="1.5em",
    )

def create_line_chart(title: str, x_values, y_values, forecast_y_values=None, height: str = "500px"):
    """Create a line chart with both historical and forecast data."""
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(
        go.Scatter(
            x=x_values[:len(y_values)],
            y=y_values,
            mode="lines+markers",
            name="Historical",
            line=dict(color="blue", width=2)
        )
    )
    
    # Add forecast data if provided
    if forecast_y_values is not None:
        # Add vertical line to separate historical from forecast
        split_point = len(y_values) - 1
        fig.add_vline(x=split_point, line_width=1, line_dash="dash", line_color="gray")
        
        # Create month names for forecast periods - continue the pattern
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        forecast_months = []
        last_month_idx = months.index(x_values[split_point])
        
        for i in range(len(forecast_y_values) + 1):
            next_month_idx = (last_month_idx + i + 1) % 12  # Wrap around for next year
            forecast_months.append(months[next_month_idx])
        
        # Add forecast line - starting from last historical point
        forecast_x = forecast_months
        forecast_y = [y_values[-1]] + forecast_y_values  # Connect with last historical point
        
        fig.add_trace(
            go.Scatter(
                x=forecast_x,
                y=forecast_y,
                mode="lines+markers",
                name="Forecast",
                line=dict(color="red", width=2, dash="dash")
            )
        )    fig.update_layout(
        title=title,
        xaxis_title="Month",
        yaxis_title="Sales",
        font=dict(color="black"),
        plot_bgcolor='#E5ECF6',  # Light blue/gray background
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add grid lines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='white',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='white'
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='white',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='white'
    )
    
    # Use the figure object directly with rx.plotly
    return rx.box(
        rx.heading(title, color="black", size="4"),
        rx.center(
            rx.plotly(data=fig),  # Pass the figure object using the fig parameter
            height=height,
            width="100%",
        ),
        width="100%",
        padding="1.5em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        margin_top="1.5em",
        margin_bottom="1.5em",
    )

def create_pie_chart(title: str, labels, values, height: str = "400px"):
    """Create a simple pie chart with the provided data."""
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            textinfo="label+percent",
            insidetextorientation="radial"
        )
    )
    fig.update_layout(
        title=title,
        font=dict(color="black"),
        plot_bgcolor='#E5ECF6',  # Light blue/gray background
        paper_bgcolor='white'
    )
    
    # Use the figure object directly with rx.plotly
    return rx.box(
        rx.heading(title, color="black", size="4"),
        rx.center(
            rx.plotly(data=fig),  # Pass the figure object using the fig parameter
            height=height,
            width="100%",
        ),
        width="100%",
        padding="1.5em",
        background="white", 
        border_radius="md",
        border="1px solid #EEE",
        margin_top="1.5em",
        margin_bottom="1.5em",
    )

# This function is now imported from components.exogenous_chart

def create_tabs():
    """Create the tabs component with correct argument ordering"""
    # Prepare some simple data for charts
    # For Sales by Vehicle Type
    vehicle_type_data = df.groupby('vehicle_type')['sales'].sum().reset_index()
    vehicle_types = vehicle_type_data['vehicle_type'].tolist()
    vehicle_sales = vehicle_type_data['sales'].tolist()
    
    # For Top Models by Sales
    model_data = df.groupby('model')['sales'].sum().sort_values(ascending=False).head(10).reset_index()
    top_models = model_data['model'].tolist()
    model_sales = model_data['sales'].tolist()
    
    # For Sales by Region
    region_data = df.groupby('region')['sales'].sum().reset_index()
    regions = region_data['region'].tolist()
    region_sales = region_data['sales'].tolist()
      # Generate mock forecast data if needed
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sales_trend = [150000, 160000, 155000, 175000, 190000, 180000, 195000, 205000, 215000, 230000, 220000, 240000]
    forecast_values = [250000, 260000, 270000, 265000, 280000, 290000]
    
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
                create_line_chart("Sales Trend and Forecast", months, sales_trend, forecast_values, height="500px"),rx.box(height="20px"),  # Add space between chart and controls
                rx.hstack(
                    rx.switch(
                        on_change=DashboardState.toggle_table,
                        is_checked=DashboardState.show_table
                    ),
                    rx.text("Show Forecast Table", color="black"),
                    margin_top="2em",
                    margin_bottom="1em",
                    padding="0.5em",
                ),                # Use rx.cond for more reliable conditonal rendering
                rx.cond(
                    DashboardState.show_table,
                    create_forecast_table(DashboardState.forecast_data),
                    rx.text("")  # Empty placeholder when table is hidden
                ),
                width="100%",
            ),
            value="sales",
        ),        rx.tabs.content(
            rx.vstack(
                rx.hstack(
                    create_simple_bar_chart("Sales by Vehicle Type", vehicle_types, vehicle_sales),
                    create_simple_bar_chart("Top Models by Sales", top_models, model_sales),
                    width="100%",
                ),
                # Create a heatmap-like display as a plain table for simplicity
                rx.box(
                    rx.heading("Sales by Month and Vehicle Type", color="black", size="4"),
                    rx.text("Month by vehicle type breakdown", padding="1em"),                    width="100%",
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
        ),        rx.tabs.content(
            rx.vstack(
                create_simple_bar_chart("Sales by Region", regions, region_sales),
                create_pie_chart("Sales by State", 
                                 df.groupby('state')['sales'].sum().nlargest(10).index.tolist(),
                                 df.groupby('state')['sales'].sum().nlargest(10).values.tolist(),
                                 height="500px"),
                width="100%",
            ),
            value="geographic",
        ),        rx.tabs.content(
            rx.vstack(
                # Use the state method directly to ensure reactivity
                DashboardState.get_exogenous_variable_chart,
                rx.box(
                    # Use a simple static component for the summary table
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Vehicle Type", color="black", font_weight="bold"),
                                rx.table.column_header_cell("Total Sales", color="black", font_weight="bold"),
                                rx.table.column_header_cell("Count", color="black", font_weight="bold")
                            )
                        ),
                        rx.table.body(
                            rx.table.row(
                                rx.table.cell("Sedan", color="black"),
                                rx.table.cell("1,250,000", color="black"),
                                rx.table.cell("125", color="black")
                            ),
                            rx.table.row(
                                rx.table.cell("SUV", color="black"),
                                rx.table.cell("950,000", color="black"),
                                rx.table.cell("95", color="black")
                            ),
                            rx.table.row(
                                rx.table.cell("Truck", color="black"),
                                rx.table.cell("675,000", color="black"),
                                rx.table.cell("67", color="black")
                            )
                        ),
                        width="100%",
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
