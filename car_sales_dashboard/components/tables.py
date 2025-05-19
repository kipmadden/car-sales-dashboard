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
    """
    # Convert to pandas DataFrame for proper grouping
    import pandas as pd
    
    try:
        # Debug information
        print(f"Creating summary table with groupby_col: {groupby_col}")
        print(f"Data sample (first 3 items): {data[:3] if len(data) >= 3 else data}")
        
        # Convert the data to a DataFrame
        df = pd.DataFrame(data)
        
        # Check if the groupby column exists in the data
        if groupby_col not in df.columns:
            print(f"Warning: Column '{groupby_col}' not found in data. Available columns: {df.columns.tolist()}")
            # Fall back to a column that definitely exists
            available_cols = df.columns.tolist()
            if 'vehicle_type' in available_cols:
                groupby_col = 'vehicle_type'
            elif 'region' in available_cols:
                groupby_col = 'region'
            elif len(available_cols) > 0:
                groupby_col = available_cols[0]
            else:
                raise ValueError("No columns available for grouping")
            print(f"Using '{groupby_col}' as fallback grouping column")
        
        # Ensure we have 'sales' column for aggregation
        if 'sales' not in df.columns:
            print(f"Warning: 'sales' column not found. Using count only.")
            # Group by the specified column and just count records
            grouped = df.groupby(groupby_col).size().reset_index(name='count')
            grouped['sales'] = 0  # Add a placeholder sales column
        else:
            # Use a more robust approach with explicit column checks
            agg_dict = {}
            if 'sales' in df.columns:
                agg_dict['sales'] = 'sum'
            
            # Add count using a column that definitely exists
            count_col = 'model' if 'model' in df.columns else df.columns[0]
            agg_dict[count_col] = 'count'
            
            # Group by the specified column and calculate aggregations
            grouped = df.groupby(groupby_col).agg(agg_dict).reset_index()
            
            # Rename the count column to 'count'
            count_col_name = f"{count_col}_count" if pd.__version__ >= '0.25.0' else count_col
            grouped = grouped.rename(columns={count_col_name: 'count'})
        
        # Sort and limit results
        grouped = grouped.sort_values('sales', ascending=False).head(10)
        
        # Debug the results
        print(f"Grouped data sample: {grouped.head(3).to_dict('records')}")
        
        # Convert back to list of dicts
        summary_data = grouped.to_dict('records')
    except Exception as e:
        # In case of any error, provide detailed error info and fallback to a simple implementation
        print(f"Error in table creation: {e}")
        import traceback
        traceback.print_exc()
        summary_data = data[:10] if len(data) > 10 else data
    
    # Create a simple table with the most important columns
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell(groupby_col.capitalize(), color="black", font_weight="bold"),
                rx.table.column_header_cell("Total Sales", color="black", font_weight="bold"),
                rx.table.column_header_cell("Count", color="black", font_weight="bold")
            )
        ),
        rx.table.body(
            # Use foreach to render each row
            rx.foreach(
                summary_data,
                lambda item, idx: rx.table.row(
                    rx.table.cell(item.get(groupby_col, ""), color="black"),
                    rx.table.cell(f"{item.get('sales', 0):,.0f}", color="black"),
                    rx.table.cell(f"{item.get('count', 0):,d}", color="black")
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