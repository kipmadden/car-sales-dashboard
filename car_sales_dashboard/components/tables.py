import reflex as rx


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
        rx.text("No data available", color="black"),
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
    """    # Create a simple table with the most important columns
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell(groupby_col.capitalize(), color="black", font_weight="bold"),
                rx.table.column_header_cell("Total Sales", color="black", font_weight="bold"),
                rx.table.column_header_cell("Count", color="black", font_weight="bold")
            )
        ),
        rx.table.body(
            # Use rx.cond to check if data exists and then use rx.foreach
            rx.foreach(
                # We use the first 10 items as a simplification
                # In a real app, proper processing would be done in the backend
                data,  # Use complete data and limit in the lambda function
                lambda item, idx: rx.cond(
                    idx < 10,  # Only render the first 10 items
                    rx.table.row(
                        rx.table.cell(item.get(groupby_col, ""), color="black"),
                        rx.table.cell(f"{item.get('sales', 0):,.0f}", color="black"),
                        rx.table.cell("1", color="black")  # Simplified count value
                    ),
                    rx.fragment()  # Don't render items beyond index 10
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
    """    # Use rx.cond instead of regular if/else for handling Vars
    return rx.cond(
        item.get("is_forecast", False),
        rx.table.row(
            rx.table.cell(
                item.get("date", ""), 
                color="black", 
                font_weight=rx.cond(idx == 0, "bold", "normal")
            ),
            rx.table.cell(f"{item.get('sales', 0):,.0f}", color="black"),
            rx.table.cell(f"{item.get('unemployment', 0):.2f}", color="black"),
            rx.table.cell(f"${item.get('gas_price', 0):.2f}", color="black"),
            rx.table.cell(f"{item.get('cpi_all', 0):.1f}", color="black"),
            rx.table.cell(f"{item.get('search_volume', 0):.0f}", color="black"),
        ),
        rx.fragment() # Empty fragment for non-forecast rows
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
        rx.text("No forecast data available", color="black"),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Date", color="black", font_weight="bold"),
                        rx.table.column_header_cell("Sales", color="black", font_weight="bold"),
                        rx.table.column_header_cell("Unemployment", color="black", font_weight="bold"),
                        rx.table.column_header_cell("Gas Price", color="black", font_weight="bold"),
                        rx.table.column_header_cell("CPI", color="black", font_weight="bold"),
                        rx.table.column_header_cell("Search Volume", color="black", font_weight="bold"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        forecast_data,
                        lambda item, idx: _create_forecast_row(item, idx)
                    )
                ),
                width="100%",
            ),
            width="100%",
            margin_top="1.5em",
            padding="1em",
            background="white",
            border_radius="md",
            border="1px solid #EEE",
        )
    )