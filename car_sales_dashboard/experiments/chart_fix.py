import reflex as rx
import pandas as pd
import plotly.graph_objects as go

def create_empty_chart():
    """Create an empty chart as a fallback"""
    fig = go.Figure()
    fig.update_layout(
        title='No Data Available',
        xaxis_title='',
        yaxis_title='',
        annotations=[
            dict(
                text="No data available for this selection",
                xref="paper",
                yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(
                    color="black",
                    size=16
                )
            )
        ],
        font=dict(color='black'),
        height=400,
    )
    return fig.to_dict()

def chart_container_v2(title, height="400px"):
    """
    Create a container for a chart with a title heading
    This version doesn't take a chart_data parameter directly
    to avoid style conflicts
    
    Args:
        title (str): Chart title
        height (str): Chart height
    
    Returns:
        rx.Component: Chart container component
    """
    return rx.box(
        rx.heading(title, color="black", size="4"),
        rx.center(
            rx.text("Loading chart data...", color="black"),
            height="200px"
        ),
        width="100%",
        padding="1.5em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        margin_top="1.5em", 
        margin_bottom="1.5em",
        height=height,
    )

def plotly_chart(figure_data, height="400px"):
    """
    Create a Plotly chart component
    
    Args:
        figure_data: Dictionary containing the plotly figure
        height (str): Chart height
    
    Returns:
        rx.Component: Plotly chart component
    """
    if not figure_data:
        figure_data = create_empty_chart()
        
    return rx.plotly(
        figure=figure_data,
        height=height,
    )
