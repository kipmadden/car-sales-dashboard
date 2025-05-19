"""
Module for creating exogenous variable charts.
"""
import reflex as rx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_exogenous_chart(title: str, forecast_data=None, height: str = "500px"):
    """Create a chart showing the impact of exogenous variables.
    
    Args:
        title: The title of the chart
        forecast_data: List of dictionaries containing forecast data (can be a Var)
        height: The height of the chart
        
    Returns:
        rx.Component: Box containing the plotly chart
    """
    # The key to reactivity is using rx.cond to properly handle Var values
    # This approach ensures the component will re-render when the Var changes
    
    # Use rx.cond for a proper reactive implementation
    return rx.cond(
        # Check if forecast_data is empty
        forecast_data == [],  # This works for both regular lists and Var
        
        # True branch: Return a component with sample data
        rx.box(
            rx.heading(title, color="black", size="4"),
            rx.center(
                rx.plotly(
                    data=_create_sample_exogenous_figure(title),
                    height=height,
                    width="100%",
                    config={"responsive": True},
                ),
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
        ),
        
        # False branch: Return a component with the actual data
        # This branch recreates the chart each time forecast_data changes
        rx.box(
            rx.heading(title, color="black", size="4"),
            rx.center(
                rx.plotly(
                    # We're using a lambda to force reactivity
                    data=lambda: _create_data_figure(forecast_data, title),
                    height=height,
                    width="100%",
                    config={"responsive": True},
                ),
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
    )

def _create_data_figure(forecast_data, title):
    """Helper function to create the chart from Var or regular data.
    
    This function is designed to be used with a lambda to force reactivity.
    """
    print(f"Creating exogenous chart with forecast data")
    try:
        # Convert forecast_data to DataFrame - works for both Var and regular data
        df = pd.DataFrame(forecast_data)
        if len(df) > 0:
            print(f"Successfully created DataFrame with {len(df)} rows of data")
            return _create_exogenous_figure_from_df(df, title)
        else:
            print("DataFrame is empty, using sample data")
            return _create_sample_exogenous_figure(title)
    except Exception as e:
        print(f"Error creating exogenous chart with data: {e}")
        return _create_sample_exogenous_figure(title)
      # Removed the return statement as we're now using rx.cond to handle both cases


def _create_sample_exogenous_figure(title: str):
    """Create a sample exogenous figure with synthetic data when no real data is available.
    
    Args:
        title: The title of the chart
        
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    print("No forecast data provided, generating sample data for visualization")
    
    # Create sample dates for the past 12 months and 6 months forecast
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 year ago
    dates = pd.date_range(start=start_date, end=end_date, freq='M').tolist()
    
    # Generate forecast dates (6 months into future)
    forecast_dates = pd.date_range(start=end_date, periods=6, freq='M').tolist()
    all_dates = dates + forecast_dates
    
    # Convert to string format for easier display
    date_strs = [d.strftime('%Y-%m-%d') for d in all_dates]
    
    # Create synthetic data
    n_points = len(all_dates)
    unemployment = 5 + np.sin(np.linspace(0, 4*np.pi, n_points)) * 0.5
    gas_price = 3.5 + np.cos(np.linspace(0, 3*np.pi, n_points)) * 0.3
    cpi_all = 260 + np.linspace(0, 10, n_points) + np.sin(np.linspace(0, 2*np.pi, n_points)) * 2
    search_volume = 100 + np.sin(np.linspace(0, 6*np.pi, n_points)) * 20
    
    # Create a dataframe with the sample data
    sample_data = {
        'date': date_strs,
        'unemployment': unemployment,
        'gas_price': gas_price,
        'cpi_all': cpi_all,
        'search_volume': search_volume,
        'is_forecast': [False] * len(dates) + [True] * len(forecast_dates)
    }
    
    forecast_data = pd.DataFrame(sample_data)
    print(f"Generated sample data with {len(forecast_data)} rows")
    
    # Create the figure with synthetic data
    return _create_exogenous_figure_from_df(forecast_data, title)


# This function is no longer needed as we've refactored create_exogenous_chart
# to handle both cases directly


def _create_exogenous_figure_from_df(forecast_data, title):
    """Helper function to create the exogenous figure from a DataFrame.
    
    Args:
        forecast_data: DataFrame containing the forecast data
        title: The title of the chart
        
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    # Print info about the data we're plotting
    print(f"Creating exogenous chart with {len(forecast_data)} rows of data")
    print(f"Data columns: {forecast_data.columns.tolist()}")
    
    # Create subplots
    fig = make_subplots(
        rows=2, 
        cols=2, 
        subplot_titles=(
            'Unemployment Rate', 
            'Gas Price', 
            'Consumer Price Index', 
            'Search Volume'
        )
    )
    
    # Check and print available columns for debugging
    available_columns = forecast_data.columns.tolist()
    print(f"Available columns in forecast_data: {available_columns}")
    
    # Add unemployment trace if column exists
    if 'date' in available_columns and 'unemployment' in available_columns:
        fig.add_trace(
            go.Scatter(
                x=forecast_data['date'],
                y=forecast_data['unemployment'],
                mode='lines',
                name='Unemployment',
                line=dict(color="blue", width=2)
            ),
            row=1, col=1
        )
    else:
        print("Warning: 'date' or 'unemployment' column missing")
    
    # Add gas price trace if column exists
    if 'date' in available_columns and 'gas_price' in available_columns:
        fig.add_trace(
            go.Scatter(
                x=forecast_data['date'],
                y=forecast_data['gas_price'],
                mode='lines',
                name='Gas Price',
                line=dict(color="green", width=2)
            ),
            row=1, col=2
        )
    else:
        print("Warning: 'date' or 'gas_price' column missing")
    
    # Add CPI trace if column exists
    if 'date' in available_columns and 'cpi_all' in available_columns:
        fig.add_trace(
            go.Scatter(
                x=forecast_data['date'],
                y=forecast_data['cpi_all'],
                mode='lines',
                name='CPI',
                line=dict(color="orange", width=2)
            ),
            row=2, col=1
        )
    else:
        print("Warning: 'date' or 'cpi_all' column missing")
    
    # Add search volume trace if column exists
    if 'date' in available_columns and 'search_volume' in available_columns:
        fig.add_trace(
            go.Scatter(
                x=forecast_data['date'],
                y=forecast_data['search_volume'],
                mode='lines',
                name='Search Volume',
                line=dict(color="purple", width=2)
            ),
            row=2, col=2
        )
    else:
        print("Warning: 'date' or 'search_volume' column missing")
    
    # Highlight forecast region with a vertical line if forecast data is available
    try:
        if 'is_forecast' in available_columns and any(forecast_data['is_forecast']):
            first_forecast_date = forecast_data[forecast_data['is_forecast']]['date'].min()
            
            # Add vertical lines to all subplots
            for i in range(1, 3):
                for j in range(1, 3):
                    fig.add_vline(
                        x=first_forecast_date, 
                        line_width=1, 
                        line_dash="dash", 
                        line_color="gray",
                        row=i, col=j
                    )
    except Exception as e:
        print(f"Error adding forecast divider: {e}")
      # Update layout
    fig.update_layout(
        height=500,
        title=title,
        font=dict(color="black"),
        plot_bgcolor='#E5ECF6',  # Light blue/gray background
        paper_bgcolor='white',
        margin=dict(t=40, b=10, l=10, r=10),
    )
    
    # Add grid lines to all subplots
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='white',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='white',
                row=i, col=j
            )
            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='white',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='white',
                row=i, col=j
            )
    
    return fig
