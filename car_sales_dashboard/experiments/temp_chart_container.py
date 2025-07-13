import reflex as rx

def chart_container(title, chart_data, height="400px"):
    """
    Create a container for a chart with a title heading
    
    Args:
        title (str): Chart title
        chart_data: Var containing a plot dictionary
        height (str): Chart height
    
    Returns:
        rx.Component: Chart container component
    """
    # We use rx.cond to handle the case when chart_data might be empty
    return rx.box(
        rx.heading(title, color="black", size="4"),
        # The key change: use rx.cond to handle empty data case
        rx.cond(
            chart_data == {},
            rx.center("No data available for this selection", height="200px", color="black"),
            rx.plotly(
                figure=chart_data,
                height=height
            )
        ),
        width="100%",
        padding="1em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        margin_top="1em",
        height=height,
    )
