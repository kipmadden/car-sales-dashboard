import reflex as rx
import pandas as pd


def create_summary_table(data, groupby_col='region'):
    """
    Create a summary table of sales by a grouping column
    
    Args:
        data (pd.DataFrame): DataFrame with sales data
        groupby_col (str): Column to group by
    
    Returns:
        rx.Component: Table component
    """
    if data.empty:
        return rx.text("No data available")
    
    # Group data by the specified column
    grouped = data.groupby(groupby_col)['sales'].agg(['sum', 'mean', 'count']).reset_index()
    
    # Rename columns for better display
    grouped.columns = [groupby_col, 'Total Sales', 'Average Sales', 'Count']
    
    # Format numbers
    grouped['Total Sales'] = grouped['Total Sales'].map(lambda x: f"{x:,.0f}")
    grouped['Average Sales'] = grouped['Average Sales'].map(lambda x: f"{x:,.1f}")
    
    # Sort by total sales descending
    grouped = grouped.sort_values('Total Sales', ascending=False)
    
    # Create table headers
    headers = [
        rx.thead(
            rx.tr(
                rx.th(groupby_col),
                rx.th("Total Sales"),
                rx.th("Average Sales"),
                rx.th("Count")
            )
        )
    ]
    
    # Create table rows
    rows = []
    for _, row in grouped.iterrows():
        rows.append(
            rx.tr(
                rx.td(row[groupby_col]),
                rx.td(row['Total Sales']),
                rx.td(row['Average Sales']),
                rx.td(row['Count'])
            )
        )
    
    # Create table body
    body = [rx.tbody(*rows)]
    
    # Create the table
    table = rx.table(
        *headers,
        *body,
        width="100%",
        variant="striped",
        colorScheme="blue",
    )
    
    return table


def create_forecast_table(forecast_data):
    """
    Create a table showing forecasted sales values
    
    Args:
        forecast_data (pd.DataFrame): DataFrame with forecast data
    
    Returns:
        rx.Component: Table component
    """
    if forecast_data.empty or not any(forecast_data['is_forecast']):
        return rx.text("No forecast data available")
    
    # Get only forecast data
    forecast = forecast_data[forecast_data['is_forecast']].copy()
    
    # Format date
    forecast['formatted_date'] = forecast['date'].dt.strftime('%b %Y')
    
    # Format numeric columns
    forecast['formatted_sales'] = forecast['sales'].map(lambda x: f"{x:,.0f}")
    forecast['formatted_unemployment'] = forecast['unemployment'].map(lambda x: f"{x:.2f}%")
    forecast['formatted_gas_price'] = forecast['gas_price'].map(lambda x: f"${x:.2f}")
    
    # Create table headers
    headers = [
        rx.thead(
            rx.tr(
                rx.th("Month"),
                rx.th("Sales"),
                rx.th("Unemployment"),
                rx.th("Gas Price"),
                rx.th("CPI"),
                rx.th("Search Volume")
            )
        )
    ]
    
    # Create table rows
    rows = []
    for _, row in forecast.iterrows():
        rows.append(
            rx.tr(
                rx.td(row['formatted_date']),
                rx.td(row['formatted_sales']),
                rx.td(row['formatted_unemployment']),
                rx.td(row['formatted_gas_price']),
                rx.td(f"{row['cpi_all']:.1f}"),
                rx.td(f"{row['search_volume']:.1f}")
            )
        )
    
    # Create table body
    body = [rx.tbody(*rows)]
    
    # Create the table
    table = rx.table(
        *headers,
        *body,
        width="100%",
        variant="striped",
        colorScheme="red",
    )
    
    return rx.vstack(
        rx.heading("Forecast Details", size="4"),
        table,
        width="100%",
        padding="1em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
    )