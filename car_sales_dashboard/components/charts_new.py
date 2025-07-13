"""
Consolidated chart creation module for the Car Sales Dashboard.

This module provides all chart creation functionality with a clean public API.
"""
import reflex as rx
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union


# =============================================================================
# Core Chart Creation Functions
# =============================================================================

def create_sales_trend_chart(forecast_data: pd.DataFrame) -> Dict:
    """
    Create a sales trend chart showing historical and forecast data.
    
    Args:
        forecast_data: DataFrame containing sales data with 'is_forecast' column
        
    Returns:
        Dict representation of Plotly figure
    """
    if forecast_data.empty:
        return _create_empty_chart("Sales Trend Chart")
    
    fig = go.Figure()
    
    try:
        # Add numeric index for consistent x-axis handling
        forecast_data = forecast_data.copy()
        forecast_data['x_index'] = range(len(forecast_data))
        
        # Split historical and forecast data
        if 'is_forecast' in forecast_data.columns:
            historical = forecast_data[forecast_data['is_forecast'] == False]
            forecast = forecast_data[forecast_data['is_forecast'] == True]
            
            # Add historical data
            if not historical.empty:
                fig.add_trace(go.Scatter(
                    x=historical['x_index'],
                    y=historical['sales'],
                    mode='lines+markers',
                    name='Historical Sales',
                    line=dict(color='blue', width=2),
                    marker=dict(size=4)
                ))
            
            # Add forecast data
            if not forecast.empty:
                fig.add_trace(go.Scatter(
                    x=forecast['x_index'],
                    y=forecast['sales'],
                    mode='lines+markers',
                    name='Forecasted Sales',
                    line=dict(color='red', width=2, dash='dash'),
                    marker=dict(size=4)
                ))
                
                # Add vertical line at forecast boundary
                if not historical.empty:
                    fig.add_vline(
                        x=historical['x_index'].max(),
                        line_width=1,
                        line_dash="dash",
                        line_color="gray",
                        annotation_text="Forecast Start"
                    )
            
            # Set custom x-axis labels
            tick_vals = forecast_data['x_index'].tolist()
            tick_text = forecast_data['date'].tolist() if 'date' in forecast_data.columns else tick_vals
        else:
            # No forecast distinction, plot all as historical
            fig.add_trace(go.Scatter(
                x=forecast_data['x_index'],
                y=forecast_data['sales'],
                mode='lines+markers',
                name='Sales Data',
                line=dict(color='blue', width=2),
                marker=dict(size=4)
            ))
            
            tick_vals = forecast_data['x_index'].tolist()
            tick_text = forecast_data['date'].tolist() if 'date' in forecast_data.columns else tick_vals
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Sales Trend and Forecast',
                'font': {'color': 'black', 'size': 20},
                'x': 0.5
            },
            xaxis_title={'text': 'Date', 'font': {'color': 'black', 'size': 16}},
            yaxis_title={'text': 'Sales Units', 'font': {'color': 'black', 'size': 16}},
            font=dict(color='black'),
            height=500,
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12)
            ),
            xaxis=dict(
                tickmode='array',
                tickvals=tick_vals,
                ticktext=tick_text,
                tickangle=45,
                showgrid=True,
                gridwidth=1,
                gridcolor='#E5E5E5'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#E5E5E5'
            ),
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
    except Exception as e:
        print(f"Error creating sales trend chart: {e}")
        return _create_empty_chart("Sales Trend Chart", error_msg=str(e))
    
    return fig.to_dict()


def create_exogenous_variables_chart(forecast_data: pd.DataFrame) -> Dict:
    """
    Create a multi-panel chart showing exogenous variables over time.
    
    Args:
        forecast_data: DataFrame with exogenous variables and dates
        
    Returns:
        Dict representation of Plotly figure with subplots
    """
    if forecast_data.empty:
        return _create_empty_chart("Exogenous Variables")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Unemployment Rate (%)', 'Gas Price ($)', 'Consumer Price Index', 'Search Volume'),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    try:
        # Define variable mappings
        variables = [
            ('unemployment', 'blue', 1, 1),
            ('gas_price', 'green', 1, 2),
            ('cpi_all', 'orange', 2, 1),
            ('search_volume', 'purple', 2, 2)
        ]
        
        # Add traces for each variable
        for var_name, color, row, col in variables:
            if var_name in forecast_data.columns and 'date' in forecast_data.columns:
                # Split historical and forecast if available
                if 'is_forecast' in forecast_data.columns:
                    historical = forecast_data[forecast_data['is_forecast'] == False]
                    forecast = forecast_data[forecast_data['is_forecast'] == True]
                    
                    # Add historical data
                    if not historical.empty:
                        fig.add_trace(
                            go.Scatter(
                                x=historical['date'],
                                y=historical[var_name],
                                mode='lines',
                                name=f'{var_name.replace("_", " ").title()} (Historical)',
                                line=dict(color=color, width=2),
                                showlegend=False
                            ),
                            row=row, col=col
                        )
                    
                    # Add forecast data
                    if not forecast.empty:
                        fig.add_trace(
                            go.Scatter(
                                x=forecast['date'],
                                y=forecast[var_name],
                                mode='lines',
                                name=f'{var_name.replace("_", " ").title()} (Forecast)',
                                line=dict(color=color, width=2, dash='dash'),
                                showlegend=False
                            ),
                            row=row, col=col
                        )
                        
                        # Add vertical line at forecast boundary
                        if not historical.empty:
                            fig.add_vline(
                                x=historical['date'].max(),
                                line_width=1,
                                line_dash="dot",
                                line_color="gray",
                                row=row, col=col
                            )
                else:
                    # No forecast distinction
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_data['date'],
                            y=forecast_data[var_name],
                            mode='lines',
                            name=var_name.replace("_", " ").title(),
                            line=dict(color=color, width=2),
                            showlegend=False
                        ),
                        row=row, col=col
                    )
        
        # Update layout
        fig.update_layout(
            height=600,
            title={
                'text': 'Exogenous Variable Trends',
                'font': {'color': 'black', 'size': 18},
                'x': 0.5
            },
            font=dict(color='black'),
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        # Update axes for all subplots
        for i in range(1, 3):
            for j in range(1, 3):
                fig.update_xaxes(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#E5E5E5',
                    row=i, col=j
                )
                fig.update_yaxes(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#E5E5E5',
                    row=i, col=j
                )
        
    except Exception as e:
        print(f"Error creating exogenous variables chart: {e}")
        return _create_empty_chart("Exogenous Variables", error_msg=str(e))
    
    return fig.to_dict()


def create_vehicle_type_chart(filtered_data: pd.DataFrame) -> Dict:
    """Create a bar chart showing sales by vehicle type."""
    if filtered_data.empty:
        return _create_empty_chart("Vehicle Type Sales")
    
    try:
        # Group by vehicle type
        vehicle_data = filtered_data.groupby('vehicle_type')['sales'].sum().reset_index()
        vehicle_data = vehicle_data.sort_values('sales', ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=vehicle_data['vehicle_type'],
            y=vehicle_data['sales'],
            marker_color='#2E86AB',
            text=vehicle_data['sales'],
            texttemplate='%{text:,.0f}',
            textposition='outside'
        ))
        
        fig.update_layout(
            title={'text': 'Sales by Vehicle Type', 'font': {'color': 'black', 'size': 18}},
            xaxis_title={'text': 'Vehicle Type', 'font': {'color': 'black'}},
            yaxis_title={'text': 'Total Sales', 'font': {'color': 'black'}},
            font=dict(color='black'),
            height=400,
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            margin=dict(l=60, r=40, t=60, b=60)
        )
        
        return fig.to_dict()
        
    except Exception as e:
        print(f"Error creating vehicle type chart: {e}")
        return _create_empty_chart("Vehicle Type Sales", error_msg=str(e))


def create_region_chart(filtered_data: pd.DataFrame) -> Dict:
    """Create a bar chart showing sales by region."""
    if filtered_data.empty:
        return _create_empty_chart("Regional Sales")
    
    try:
        # Group by region
        region_data = filtered_data.groupby('region')['sales'].sum().reset_index()
        region_data = region_data.sort_values('sales', ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=region_data['region'],
            y=region_data['sales'],
            marker_color='#A23B72',
            text=region_data['sales'],
            texttemplate='%{text:,.0f}',
            textposition='outside'
        ))
        
        fig.update_layout(
            title={'text': 'Sales by Region', 'font': {'color': 'black', 'size': 18}},
            xaxis_title={'text': 'Region', 'font': {'color': 'black'}},
            yaxis_title={'text': 'Total Sales', 'font': {'color': 'black'}},
            font=dict(color='black'),
            height=400,
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            margin=dict(l=60, r=40, t=60, b=60)
        )
        
        return fig.to_dict()
        
    except Exception as e:
        print(f"Error creating region chart: {e}")
        return _create_empty_chart("Regional Sales", error_msg=str(e))


def create_top_models_chart(filtered_data: pd.DataFrame) -> Dict:
    """Create a horizontal bar chart showing top models by sales."""
    if filtered_data.empty:
        return _create_empty_chart("Top Models")
    
    try:
        # Group by model and get top 10
        model_data = filtered_data.groupby('model')['sales'].sum().reset_index()
        model_data = model_data.sort_values('sales', ascending=True).tail(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=model_data['sales'],
            y=model_data['model'],
            orientation='h',
            marker_color='#F18F01',
            text=model_data['sales'],
            texttemplate='%{text:,.0f}',
            textposition='outside'
        ))
        
        fig.update_layout(
            title={'text': 'Top 10 Models by Sales', 'font': {'color': 'black', 'size': 18}},
            xaxis_title={'text': 'Total Sales', 'font': {'color': 'black'}},
            yaxis_title={'text': 'Model', 'font': {'color': 'black'}},
            font=dict(color='black'),
            height=500,
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            margin=dict(l=120, r=40, t=60, b=60)
        )
        
        return fig.to_dict()
        
    except Exception as e:
        print(f"Error creating top models chart: {e}")
        return _create_empty_chart("Top Models", error_msg=str(e))


def create_state_map_chart(filtered_data: pd.DataFrame) -> Dict:
    """Create a choropleth map showing sales by state."""
    if filtered_data.empty:
        return _create_empty_chart("State Sales Map")
    
    try:
        # Group by state
        state_data = filtered_data.groupby('state')['sales'].sum().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Choropleth(
            locations=state_data['state'],
            z=state_data['sales'],
            locationmode='USA-states',
            colorscale='Blues',
            text=state_data['state'],
            colorbar_title="Sales"
        ))
        
        fig.update_layout(
            title={'text': 'Sales by State', 'font': {'color': 'black', 'size': 18}},
            geo_scope='usa',
            height=500,
            font=dict(color='black'),
            paper_bgcolor='white'
        )
        
        return fig.to_dict()
        
    except Exception as e:
        print(f"Error creating state map chart: {e}")
        return _create_empty_chart("State Sales Map", error_msg=str(e))


def create_heatmap_chart(filtered_data: pd.DataFrame, x_col: str = 'month', y_col: str = 'vehicle_type') -> Dict:
    """Create a heatmap showing sales by two categorical variables."""
    if filtered_data.empty:
        return _create_empty_chart("Sales Heatmap")
    
    try:
        # Create pivot table for heatmap
        if x_col not in filtered_data.columns or y_col not in filtered_data.columns:
            return _create_empty_chart("Sales Heatmap", error_msg=f"Missing columns: {x_col} or {y_col}")
        
        pivot_data = filtered_data.pivot_table(
            values='sales',
            index=y_col,
            columns=x_col,
            aggfunc='sum',
            fill_value=0
        )
        
        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis',
            colorbar_title="Sales"
        ))
        
        fig.update_layout(
            title={'text': f'Sales Heatmap: {y_col.title()} vs {x_col.title()}', 'font': {'color': 'black', 'size': 18}},
            xaxis_title={'text': x_col.title(), 'font': {'color': 'black'}},
            yaxis_title={'text': y_col.title(), 'font': {'color': 'black'}},
            font=dict(color='black'),
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig.to_dict()
        
    except Exception as e:
        print(f"Error creating heatmap chart: {e}")
        return _create_empty_chart("Sales Heatmap", error_msg=str(e))


# =============================================================================
# Chart Container Components
# =============================================================================

def chart_container(title: str, chart_data: Union[Dict, rx.Var], height: str = "500px") -> rx.Component:
    """
    Create a responsive chart container with error handling.
    
    Args:
        title: Chart title
        chart_data: Chart data (dict or Var containing dict)
        height: Container height
        
    Returns:
        rx.Component: Chart container with title and plotly chart
    """
    return rx.box(
        rx.heading(title, color="black", size="4", margin_bottom="1em"),
        rx.cond(
            chart_data == {},
            rx.center(
                rx.text("No data available for this selection", color="gray", size="3"),
                height="300px"
            ),
            rx.plotly(
                data=chart_data,
                height=height,
                width="100%"
            )
        ),
        width="100%",
        padding="1.5em",
        background="white",
        border_radius="md",
        border="1px solid #E5E5E5",
        margin_bottom="1.5em"
    )


# =============================================================================
# Utility Functions
# =============================================================================

def _create_empty_chart(title: str, error_msg: Optional[str] = None) -> Dict:
    """Create an empty chart with optional error message."""
    fig = go.Figure()
    
    message = error_msg or "No data available for this selection"
    
    fig.update_layout(
        title={'text': title, 'font': {'color': 'black', 'size': 18}},
        xaxis_title='',
        yaxis_title='',
        annotations=[
            dict(
                text=message,
                xref="paper",
                yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(color="gray", size=14)
            )
        ],
        font=dict(color='black'),
        height=400,
        plot_bgcolor='#F8F9FA',
        paper_bgcolor='white'
    )
    
    return fig.to_dict()


def generate_sample_data(n_points: int = 24) -> pd.DataFrame:
    """Generate sample data for testing charts."""
    dates = pd.date_range(start='2022-01-01', periods=n_points, freq='M')
    
    # Create sample data with trend and seasonality
    trend = np.linspace(1000, 1500, n_points)
    seasonal = 200 * np.sin(2 * np.pi * np.arange(n_points) / 12)
    noise = np.random.normal(0, 50, n_points)
    
    sales = trend + seasonal + noise
    
    # Create exogenous variables
    unemployment = 5 + np.sin(np.linspace(0, 4*np.pi, n_points)) * 0.5
    gas_price = 3.5 + np.cos(np.linspace(0, 3*np.pi, n_points)) * 0.3
    cpi_all = 260 + np.linspace(0, 10, n_points) + np.sin(np.linspace(0, 2*np.pi, n_points)) * 2
    search_volume = 100 + np.sin(np.linspace(0, 6*np.pi, n_points)) * 20
    
    # Mark last 6 months as forecast
    is_forecast = [False] * (n_points - 6) + [True] * 6
    
    return pd.DataFrame({
        'date': dates.strftime('%b %Y'),
        'sales': sales,
        'unemployment': unemployment,
        'gas_price': gas_price,
        'cpi_all': cpi_all,
        'search_volume': search_volume,
        'is_forecast': is_forecast
    })


# =============================================================================
# Legacy Function Aliases (for backward compatibility)
# =============================================================================

# Keep these for backward compatibility during transition
create_exogenous_impact_chart = create_exogenous_variables_chart
