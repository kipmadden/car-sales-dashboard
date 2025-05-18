import reflex as rx


def sidebar_filters(unique_regions, unique_states, unique_vehicle_types, 
                   unique_makes, unique_models, unique_years, state_class):
    """
    Create sidebar filters for the dashboard
    
    Args:
        unique_regions (list): List of unique regions
        unique_states (list): List of unique states
        unique_vehicle_types (list): List of unique vehicle types
        unique_makes (list): List of unique makes
        unique_models (list): List of unique models
        unique_years (list): List of unique years
        state_class: State class with update handlers
    
    Returns:
        rx.Component: Sidebar component with filters
    """
    return rx.vstack(
        rx.heading("Filters", size="4"),
        
        # Region filter
        rx.text("Regions:"),
        rx.select(
            unique_regions,
            placeholder="Select regions",
            on_change=state_class.update_regions,
            is_multi=True,
        ),
        
        # State filter
        rx.text("States:"),
        rx.select(
            unique_states,
            placeholder="Select states",
            on_change=state_class.update_states,
            is_multi=True,
        ),
        
        # Vehicle type filter
        rx.text("Vehicle Types:"),
        rx.select(
            unique_vehicle_types,
            placeholder="Select vehicle types",
            on_change=state_class.update_vehicle_types,
            is_multi=True,
        ),
        
        # Make filter
        rx.text("Makes:"),
        rx.select(
            unique_makes,
            placeholder="Select makes",
            on_change=state_class.update_makes,
            is_multi=True,
        ),
        
        # Model filter
        rx.text("Models:"),
        rx.select(
            unique_models,
            placeholder="Select models",
            on_change=state_class.update_models,
            is_multi=True,
        ),
        
        # Year filter
        rx.text("Model Years:"),
        rx.select(
            unique_years,
            placeholder="Select years",
            on_change=state_class.update_years,
            is_multi=True,
        ),
        
        width="250px",
        padding="1em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        height="100%",
    )


def exogenous_controls(state_class):
    """
    Create controls for adjusting exogenous variables
    
    Args:
        state_class: State class with update handlers
    
    Returns:
        rx.Component: Controls component
    """
    return rx.vstack(
        rx.heading("Exogenous Variable Simulation", size="4"),
        rx.text("Adjust the sliders to see the impact on forecasted sales"),
        
        # Unemployment rate modifier
        rx.hstack(
            rx.text("Unemployment Rate:", width="150px"),
            rx.slider(
                min=0.5,
                max=2.0,
                step=0.01,
                default_value=1.0,
                on_change=state_class.update_unemployment,
                width="100%",
            ),
            rx.text(f"{state_class.unemployment_modifier:.2f}", width="50px"),
            width="100%",
        ),
        
        # Gas price modifier
        rx.hstack(
            rx.text("Gas Price:", width="150px"),
            rx.slider(
                min=0.5,
                max=2.0,
                step=0.01,
                default_value=1.0,
                on_change=state_class.update_gas_price,
                width="100%",
            ),
            rx.text(f"{state_class.gas_price_modifier:.2f}", width="50px"),
            width="100%",
        ),
        
        # CPI modifier
        rx.hstack(
            rx.text("Consumer Price Index:", width="150px"),
            rx.slider(
                min=0.5,
                max=2.0,
                step=0.01,
                default_value=1.0,
                on_change=state_class.update_cpi,
                width="100%",
            ),
            rx.text(f"{state_class.cpi_modifier:.2f}", width="50px"),
            width="100%",
        ),
        
        # Search volume modifier
        rx.hstack(
            rx.text("Search Volume:", width="150px"),
            rx.slider(
                min=0.5,
                max=2.0,
                step=0.01,
                default_value=1.0,
                on_change=state_class.update_search_volume,
                width="100%",
            ),
            rx.text(f"{state_class.search_volume_modifier:.2f}", width="50px"),
            width="100%",
        ),
        
        # Forecast months
        rx.hstack(
            rx.text("Forecast Months:", width="150px"),
            rx.slider(
                min=1,
                max=24,
                step=1,
                default_value=6,
                on_change=state_class.update_forecast_months,
                width="100%",
            ),
            rx.text(state_class.forecast_months.to_string(), width="50px"),
            width="100%",
        ),
        
        # Model selection
        rx.hstack(
            rx.text("Forecast Model:", width="150px"),
            rx.select(
                ["Linear Regression", "Random Forest"],
                default_value="Linear Regression",
                on_change=state_class.update_model_type,
                width="100%",
            ),
            width="100%",
        ),
        
        padding="1em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        width="100%",
    )


def chart_container(title, chart_data, height="400px"):
    """
    Create a container for a chart with a title heading
    
    Args:
        title (str): Chart title
        chart_data: Chart data formula - should be a Var containing a plot dictionary
        height (str): Chart height
    
    Returns:
        rx.Component: Chart container component
    """
    return rx.box(
        rx.heading(title),
        rx.plotly(
            figure=chart_data,
            fallback=rx.center("No data available", height="200px")
        ),
        width="100%",
        padding="1em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        margin_top="1em",
        height=height,
    )
