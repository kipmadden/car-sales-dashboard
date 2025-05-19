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
            print("Forecast data DataFrame is empty")
            return {}
    elif not forecast_data:
        print("Forecast data is None or empty list")
        return {}
    
    # Additional debug info
    try:
        print(f"Forecast data type: {type(forecast_data)}")
        print(f"Forecast data columns: {forecast_data.columns if hasattr(forecast_data, 'columns') else 'No columns'}")
        print(f"Forecast data shape: {forecast_data.shape if hasattr(forecast_data, 'shape') else 'No shape'}")
    except Exception as e:
        print(f"Error inspecting forecast data: {e}")
      
    # Create the chart
    fig = go.Figure()
    
    try:
        # Convert to numeric indices for x-axis to avoid text rendering issues
        forecast_data['x_index'] = range(len(forecast_data))
        
        # Historical sales - with error handling
        if 'is_forecast' in forecast_data.columns:
            # Handle if filtering works correctly
            historical = forecast_data[forecast_data['is_forecast'] == False]
            if not historical.empty:
                fig.add_trace(go.Scatter(
                    x=historical['x_index'],  # Use numeric indices for x-axis
                    y=historical['sales'],
                    mode='lines',
                    name='Historical Sales',
                    line=dict(color='blue', width=2)
                ))
            else:
                print("No historical data after filtering")
            
            # Forecasted sales
            forecast = forecast_data[forecast_data['is_forecast'] == True]
            if not forecast.empty:
                fig.add_trace(go.Scatter(
                    x=forecast['x_index'],  # Use numeric indices for x-axis
                    y=forecast['sales'],
                    mode='lines',
                    name='Forecasted Sales',
                    line=dict(color='red', width=2, dash='dash')
                ))
                
                # Add a vertical line to separate historical from forecast
                if not historical.empty:
                    fig.add_vline(
                        x=historical['x_index'].max(),
                        line_width=1,
                        line_dash="dash",
                        line_color="gray"
                    )
            else:
                print("No forecast data after filtering")
                
            # Create custom tick labels from the date column
            tick_vals = forecast_data['x_index'].tolist()
            tick_text = forecast_data['date'].tolist()
        else:
            # If 'is_forecast' column doesn't exist, just plot all data
            print("'is_forecast' column not found in data, plotting all as historical")
            fig.add_trace(go.Scatter(
                x=forecast_data['x_index'],
                y=forecast_data['sales'],
                mode='lines',
                name='Sales Data',
                line=dict(color='blue', width=2)
            ))
            # Create custom tick labels from the date column
            tick_vals = forecast_data['x_index'].tolist()
            tick_text = forecast_data['date'].tolist() 
    except Exception as e:
        print(f"Error creating chart traces: {e}")
        # Set default tick values if the above code fails
        tick_vals = list(range(12))
        tick_text = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]    # Update layout with improved visibility settings and custom x-axis ticks
    fig.update_layout(
        title={
            'text': 'Sales Trend and Forecast',
            'font': {'color': 'black', 'size': 20}  # Increased font size
        },
        xaxis_title={
            'text': 'Date',
            'font': {'color': 'black', 'size': 16}  # Increased font size
        },
        yaxis_title={
            'text': 'Sales Units',
            'font': {'color': 'black', 'size': 16}  # Increased font size
        },
        legend=dict(
            x=0, 
            y=1, 
            traceorder='normal',
            font=dict(color='black', size=14)  # Specified size
        ),
        font=dict(color='black'),
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),  # Improved margins
        plot_bgcolor='#E5ECF6',  # Light blue/gray background for consistency
        paper_bgcolor='white',  # White paper
        # Set custom tick positions and labels
        xaxis=dict(
            tickmode='array',
            tickvals=tick_vals,
            ticktext=tick_text,
            tickangle=45  # Angle the labels for better readability
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