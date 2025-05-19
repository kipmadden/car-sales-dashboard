"""
Module for creating exogenous variable charts.
"""
import reflex as rx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def _create_sample_exogenous_figure(title: str):
    """Create a sample exogenous figure with synthetic data when no real data is available.
    Args:
        title: The title of the chart
    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    print("No forecast data provided, generating sample data for visualization")

    # Set last historical date to April 2025
    last_hist_date = pd.Timestamp(year=2025, month=4, day=1)
    n_hist_months = 36  # 3 years of history
    hist_dates = pd.date_range(end=last_hist_date, periods=n_hist_months, freq='MS')

    # Generate forecast dates (6 months into future)
    n_forecast_months = 6
    forecast_dates = pd.date_range(start=last_hist_date + pd.DateOffset(months=1), periods=n_forecast_months, freq='MS')
    all_dates = hist_dates.tolist() + forecast_dates.tolist()

    # Use MonthYear format for all dates
    date_strs = [d.strftime('%b %Y') for d in all_dates]

    n_points = len(all_dates)
    unemployment = 5 + np.sin(np.linspace(0, 4*np.pi, n_points)) * 0.5
    gas_price = 3.5 + np.cos(np.linspace(0, 3*np.pi, n_points)) * 0.3
    cpi_all = 260 + np.linspace(0, 10, n_points) + np.sin(np.linspace(0, 2*np.pi, n_points)) * 2
    search_volume = 100 + np.sin(np.linspace(0, 6*np.pi, n_points)) * 20
    sales = 1000 + 100 * np.random.rand(n_points) + np.linspace(0, 200, n_points)

    sample_data = {
        'date': date_strs,
        'sales': sales,
        'unemployment': unemployment,
        'gas_price': gas_price,
        'cpi_all': cpi_all,
        'search_volume': search_volume,
        'is_forecast': [False] * len(hist_dates) + [True] * len(forecast_dates)
    }
    forecast_data = pd.DataFrame(sample_data)
    print(f"Generated sample data with {len(forecast_data)} rows, last hist: {date_strs[len(hist_dates)-1]}, first forecast: {date_strs[len(hist_dates)]}")
    return _create_exogenous_figure_from_df(forecast_data, title)


def create_exogenous_figure(title: str, forecast_data) -> go.Figure:
    """Create a Plotly figure for exogenous variables using forecast_data.

    Args:
        title: The chart title.
        forecast_data: List[dict] or DataFrame with exogenous data.

    Returns:
        plotly.graph_objects.Figure: The chart.
    """
    # Handle empty or None forecast_data by generating sample data
    if not forecast_data or (isinstance(forecast_data, list) and len(forecast_data) == 0):
        print("No forecast data provided, generating sample data for visualization")
        return _create_sample_exogenous_figure(title)

    # Accept both list-of-dicts and DataFrame
    if isinstance(forecast_data, list):
        df = pd.DataFrame(forecast_data)
    elif isinstance(forecast_data, pd.DataFrame):
        df = forecast_data
    else:
        raise ValueError("forecast_data must be a list of dicts or a DataFrame.")

    print(f"Creating exogenous chart with {len(df)} rows of data")
    print(f"Data columns: {df.columns.tolist()}")

    # (the rest of your existing plotting logic here)
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

    available_columns = df.columns.tolist()
    # Add traces as before...

    # Unemployment
    if 'date' in available_columns and 'unemployment' in available_columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['unemployment'],
                mode='lines',
                name='Unemployment',
                line=dict(color="blue", width=2)
            ),
            row=1, col=1
        )
    # Gas Price
    if 'date' in available_columns and 'gas_price' in available_columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['gas_price'],
                mode='lines',
                name='Gas Price',
                line=dict(color="green", width=2)
            ),
            row=1, col=2
        )
    # CPI
    if 'date' in available_columns and 'cpi_all' in available_columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['cpi_all'],
                mode='lines',
                name='CPI',
                line=dict(color="orange", width=2)
            ),
            row=2, col=1
        )
    # Search Volume
    if 'date' in available_columns and 'search_volume' in available_columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['search_volume'],
                mode='lines',
                name='Search Volume',
                line=dict(color="purple", width=2)
            ),
            row=2, col=2
        )
    # Forecast region divider
    try:
        if 'is_forecast' in available_columns and any(df['is_forecast']):
            first_forecast_date = df[df['is_forecast']]['date'].min()
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
    # Layout and grid
    fig.update_layout(
        height=500,
        title=title,
        font=dict(color="black"),
        plot_bgcolor='#E5ECF6',
        paper_bgcolor='white',
        margin=dict(t=40, b=10, l=10, r=10),
    )
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
