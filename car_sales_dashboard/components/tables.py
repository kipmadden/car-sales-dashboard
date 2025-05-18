import reflex as rx
import pandas as pd


def create_summary_table(data, groupby_col='region'):
    """
    Create a summary table of sales by a grouping column
    
    Args:
        data: List of data dicts (can be a Var)
        groupby_col (str): Column to group by
    
    Returns:
        rx.Component: Table component
    """
    # Handle the case when there's no data - use rx.cond for Vars
    return rx.cond(
        data == [],
        rx.text("No data available"),
        _create_summary_table_from_data(data, groupby_col)
    )


def _create_summary_table_from_data(data, groupby_col):
    """
    Create a summary table using rx components instead of pandas operations
    
    Args:
        data: List of data dicts
        groupby_col: Column to group by
    
    Returns:
        rx.Component: Table component
    """
    # Create a simple table with the most important columns
    return rx.table(
        rx.thead(
            rx.tr(
                rx.th(groupby_col.capitalize()),
                rx.th("Total Sales"),
                rx.th("Count")
            )
        ),
        rx.tbody(
            rx.foreach(
                # We use the first 10 items as a simplification
                # In a real app, proper processing would be done in the backend
                rx.slice(data, 0, 10),
                lambda item, idx: rx.tr(
                    rx.td(item.get(groupby_col, "")),
                    rx.td(f"{item.get('sales', 0):,.0f}"),
                    rx.td("1")  # Simplified count value
                )
            )
        ),
        width="100%",
    )


def _create_forecast_row(item, idx):
    """
    Create a row for the forecast table
    
    Args:
        item: Dictionary containing forecast data
        idx: Index of the item
    
    Returns:
        rx.Component: Table row
    """
    # Only show forecast rows
    if not item.get('is_forecast', False):
        return rx.fragment()
    
    # Create row with formatted values
    return rx.tr(
        rx.td(item.get('date', ''), color="blue"),
        rx.td(f"{item.get('sales', 0):,.0f}"),
        rx.td(f"{item.get('unemployment', 0):.2f}"),
        rx.td(f"${item.get('gas_price', 0):.2f}"),
        rx.td(f"{item.get('cpi_all', 0):.1f}"),
        rx.td(f"{item.get('search_volume', 0):.0f}"),
    )


def create_forecast_table(forecast_data):
    """
    Create a table showing forecasted sales values
    
    Args:
        forecast_data: List of forecast data dicts (can be a Var)
    
    Returns:
        rx.Component: Table component
    """
    # Handle the case when there's no data - use rx.cond for Vars
    return rx.cond(
        forecast_data == [],
        rx.text("No forecast data available"),
        rx.table(
            rx.thead(
                rx.tr(
                    rx.th("Date"),
                    rx.th("Sales"),
                    rx.th("Unemployment"),
                    rx.th("Gas Price"),
                    rx.th("CPI"),
                    rx.th("Search Volume"),
                )
            ),
            rx.tbody(
                rx.foreach(
                    forecast_data,
                    lambda item, idx: _create_forecast_row(item, idx)
                )
            ),
            width="100%",
        )
    )
    
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