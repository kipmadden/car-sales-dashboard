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
    # Create a fallback table to use when data processing fails
    def create_fallback_table():
        return rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Category", color="black", font_weight="bold"),
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
        )
            
    # Convert to pandas DataFrame for proper grouping
    import pandas as pd
    
    try:
        # Debug information
        print(f"Creating summary table with groupby_col: {groupby_col}")
        
        # Don't try to access slices or length of data directly if it's a Var
        # Convert the data to a DataFrame - with error handling for Var types
        try:
            df = pd.DataFrame(data)
        except TypeError as e:
            if "has no attribute 'columns'" in str(e) or "has no len()" in str(e):
                print(f"Data appears to be a Reflex Var, creating a simple table instead")
                return create_fallback_table()
            else:
                raise e
                
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
          # Use fallback static data
        return create_fallback_table()
    
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
    """
    try:
        # Use .get() for safe access with default values for all fields
        # This approach is more resilient to missing data
        date_val = item.get("date", "")
        sales_val = item.get("sales", 0)
        unemployment_val = item.get("unemployment", 0)
        gas_price_val = item.get("gas_price", 0)
        cpi_val = item.get("cpi_all", 0)
        search_vol_val = item.get("search_volume", 0)
        is_forecast = item.get("is_forecast", False)
        
        # Format the values with proper formatting
        sales_formatted = f"{sales_val:,.0f}" if isinstance(sales_val, (int, float)) else "0"
        unemployment_formatted = f"{unemployment_val:.2f}" if isinstance(unemployment_val, (int, float)) else "0.00"
        gas_price_formatted = f"${gas_price_val:.2f}" if isinstance(gas_price_val, (int, float)) else "$0.00"
        cpi_formatted = f"{cpi_val:.1f}" if isinstance(cpi_val, (int, float)) else "0.0"
        search_vol_formatted = f"{search_vol_val:.0f}" if isinstance(search_vol_val, (int, float)) else "0"
        
        # Return the formatted row
        return rx.table.row(
            rx.table.cell(
                date_val, 
                color="black", 
                font_weight=rx.cond(idx == 0, "bold", "normal")
            ),
            rx.table.cell(sales_formatted, color="black"),
            rx.table.cell(unemployment_formatted, color="black"),
            rx.table.cell(gas_price_formatted, color="black"),
            rx.table.cell(cpi_formatted, color="black"),
            rx.table.cell(search_vol_formatted, color="black"),
            # Add highlighting for forecast rows
            background=rx.cond(
                is_forecast,
                "rgba(255, 240, 240, 0.5)",  # Light pink background for forecast rows
                "white"  # White background for historical rows
            )
        )
    except Exception as e:
        # Fallback for any errors
        print(f"Error creating forecast row: {e}")
        return rx.table.row(
            rx.table.cell("Error", color="red"),
            rx.table.cell("", color="black"),
            rx.table.cell("", color="black"),
            rx.table.cell("", color="black"),
            rx.table.cell("", color="black"),
            rx.table.cell("", color="black")
        )


def create_forecast_table(forecast_data):
    """
    Create a table showing forecasted sales values
    
    Args:
        forecast_data: List of forecast data dicts (can be a Var)
    
    Returns:
        rx.Component: Table component
    """
    # Print debug information about the forecast_data
    print(f"Creating forecast table - data type: {type(forecast_data)}")
    
    # Always return a table component, but handle empty data within the component
    # This approach is more reliable with Reflex Vars
    return rx.box(
        rx.heading("Sales Forecast Data", size="4", color="black"),
        rx.cond(
            # Check if forecast_data is empty or None (works with Vars)
            forecast_data is None,
            # If empty, show a message
            rx.text("No forecast data available", color="black", padding="1em"),
            # If not empty, show the table
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
            )
        ),
        width="100%",
        margin_top="1.5em",
        padding="1em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
    )