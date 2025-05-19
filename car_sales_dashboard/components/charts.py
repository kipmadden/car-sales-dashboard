import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def create_sales_trend_chart(forecast_data):
    """
    Create a sales trend chart showing historical and forecasted sales
    
    Args:
        forecast_data (pd.DataFrame or list): DataFrame or list with historical and forecast data
    
    Returns:
        dict: Plotly figure as a dictionary
    """
    # Check if data is empty either as DataFrame or list
    if isinstance(forecast_data, pd.DataFrame):
        if forecast_data.empty:
            return {}
    elif not forecast_data:
        return {}
    
    # Create the chart
    fig = go.Figure()
    
    # Historical sales
    historical = forecast_data[forecast_data['is_forecast'] == False]
    fig.add_trace(go.Scatter(
        x=historical['date'],
        y=historical['sales'],
        mode='lines',
        name='Historical Sales',
        line=dict(color='blue', width=2)
    ))
    
    # Forecasted sales
    forecast = forecast_data[forecast_data['is_forecast'] == True]
    fig.add_trace(go.Scatter(
        x=forecast['date'],
        y=forecast['sales'],
        mode='lines',
        name='Forecasted Sales',
        line=dict(color='red', width=2, dash='dash')
    ))
      # Update layout
    fig.update_layout(
        title={
            'text': 'Sales Trend and Forecast',
            'font': {'color': 'black', 'size': 18}
        },
        xaxis_title={
            'text': 'Date',
            'font': {'color': 'black', 'size': 14}
        },
        yaxis_title={
            'text': 'Sales Units',
            'font': {'color': 'black', 'size': 14}
        },
        legend=dict(
            x=0, 
            y=1, 
            traceorder='normal',
            font=dict(color='black')
        ),
        font=dict(color='black'),
        height=500,
    )
      # Return the figure as a dict for consistency with other chart functions
    return fig.to_dict()


def create_vehicle_type_chart(filtered_data):
    """
    Create a pie chart showing sales distribution by vehicle type
    
    Args:
        filtered_data (pd.DataFrame): DataFrame with filtered sales data
    
    Returns:
        dict: Plotly figure as a dictionary
    """
    if filtered_data.empty:
        return {}
    
    # Group by vehicle type
    vehicle_sales = filtered_data.groupby('vehicle_type')['sales'].sum().reset_index()
    
    # Create pie chart
    fig = px.pie(
        vehicle_sales, 
        values='sales', 
        names='vehicle_type', 
        title='Sales by Vehicle Type'
    )
    
    # Update layout
    fig.update_layout(height=400)
    
    return fig.to_dict()


def create_region_chart(filtered_data):
    """
    Create a bar chart showing sales distribution by region
    
    Args:
        filtered_data (pd.DataFrame): DataFrame with filtered sales data
    
    Returns:
        dict: Plotly figure as a dictionary
    """
    if filtered_data.empty:
        return {}
    
    # Group by region
    region_sales = filtered_data.groupby('region')['sales'].sum().reset_index()
    
    # Create bar chart
    fig = px.bar(
        region_sales, 
        x='region', 
        y='sales', 
        title='Sales by Region',
        color='region'
    )
    
    # Update layout
    fig.update_layout(height=400)
    
    return fig.to_dict()


def create_exogenous_impact_chart(forecast_data):
    """
    Create a chart showing the impact of exogenous variables
    
    Args:
        forecast_data (pd.DataFrame): DataFrame with forecast data
    
    Returns:
        dict: Plotly figure as a dictionary
    """
    if forecast_data.empty:
        return {}
    
    # Create the chart
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
    
    # Add unemployment trace
    fig.add_trace(
        go.Scatter(
            x=forecast_data['date'], 
            y=forecast_data['unemployment'], 
            mode='lines', 
            name='Unemployment'
        ),
        row=1, col=1
    )
    
    # Add gas price trace
    fig.add_trace(
        go.Scatter(
            x=forecast_data['date'], 
            y=forecast_data['gas_price'], 
            mode='lines', 
            name='Gas Price'
        ),
        row=1, col=2
    )
    
    # Add CPI trace
    fig.add_trace(
        go.Scatter(
            x=forecast_data['date'], 
            y=forecast_data['cpi_all'], 
            mode='lines', 
            name='CPI'
        ),
        row=2, col=1
    )
    
    # Add search volume trace
    fig.add_trace(
        go.Scatter(
            x=forecast_data['date'], 
            y=forecast_data['search_volume'], 
            mode='lines', 
            name='Search Volume'
        ),
        row=2, col=2
    )
    
    # Highlight forecast region with colored background
    for i in range(1, 3):
        for j in range(1, 3):
            # Get the first forecast date
            if not forecast_data.empty and any(forecast_data['is_forecast']):
                first_forecast_date = forecast_data[forecast_data['is_forecast']]['date'].min()
                
                # Add a vertical line at the forecast start
                fig.add_vline(
                    x=first_forecast_date, 
                    line_width=1, 
                    line_dash="dash", 
                    line_color="gray",
                    row=i, col=j
                )
    
    # Update layout
    fig.update_layout(height=500, title_text='Exogenous Variable Trends')
    
    return fig.to_dict()


def create_top_models_chart(filtered_data):
    """
    Create a chart showing the top selling models
    
    Args:
        filtered_data (pd.DataFrame): DataFrame with filtered sales data
    
    Returns:
        dict: Plotly figure as a dictionary
    """
    if filtered_data.empty:
        return {}
    
    # Group by make and model
    model_sales = filtered_data.groupby(['make', 'model'])['sales'].sum().reset_index()
    model_sales['make_model'] = model_sales['make'] + ' ' + model_sales['model']
    
    # Sort and get top 10
    top_models = model_sales.sort_values('sales', ascending=False).head(10)
    
    # Create bar chart
    fig = px.bar(
        top_models, 
        x='make_model', 
        y='sales', 
        title='Top 10 Models by Sales',
        color='make'
    )
    
    # Update layout
    fig.update_layout(height=400)
    
    return fig.to_dict()


def create_state_map_chart(filtered_data):
    """
    Create a choropleth map of sales by state
    
    Args:
        filtered_data (pd.DataFrame): DataFrame with filtered sales data
    
    Returns:
        dict: Plotly figure as a dictionary
    """
    if filtered_data.empty:
        return {}
    
    # Group by state
    state_sales = filtered_data.groupby('state')['sales'].sum().reset_index()
    
    # Create the map
    fig = px.choropleth(
        state_sales,
        locations='state',
        locationmode='USA-states',
        color='sales',
        scope='usa',
        title='Sales by State',
        color_continuous_scale='blues'
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        coloraxis_colorbar=dict(title='Sales')
    )
    
    return fig.to_dict()


def create_heatmap_chart(filtered_data, x_col='month', y_col='vehicle_type'):
    """
    Create a heatmap chart
    
    Args:
        filtered_data (pd.DataFrame): DataFrame with filtered sales data
        x_col (str): Column to use for x-axis
        y_col (str): Column to use for y-axis
    
    Returns:
        dict: Plotly figure as a dictionary
    """
    if filtered_data.empty:
        return {}
    
    # Group by specified columns
    grouped = filtered_data.groupby([y_col, x_col])['sales'].sum().reset_index()
    
    # Pivot for heatmap format
    pivot_data = grouped.pivot(index=y_col, columns=x_col, values='sales')
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Viridis',
        colorbar=dict(title='Sales')
    ))
    
    # Update layout
    fig.update_layout(
        title=f'Sales Heatmap by {y_col} and {x_col}',
        height=400
    )
    
    return fig.to_dict()