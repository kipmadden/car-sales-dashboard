"""
Chart components that can be rendered with client-side data.

This module provides a custom chart component that can be rendered with data
from client-side scripts to avoid EventHandler errors. This approach separates
the UI structure from the data loading logic.
"""

import reflex as rx
import plotly.graph_objects as go

def create_empty_chart():
    """Create an empty chart as a fallback"""
    fig = go.Figure()
    fig.update_layout(
        title='Loading Chart...',
        xaxis_title='',
        yaxis_title='',
        annotations=[
            dict(
                text="Chart is loading...",
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

def responsive_chart_container(title: str, chart_id: str, height: str = "500px"):
    """
    Create a responsive chart container with an empty placeholder chart.
    
    Args:
        title (str): The title of the chart
        chart_id (str): The ID to be used for client-side targeting
        height (str): The height of the chart container
        
    Returns:
        rx.Component: A container component with an empty Plotly chart
    """
    return rx.box(
        rx.heading(title, color="black", size="4"),
        rx.center(
            rx.plotly(
                figure=create_empty_chart(),
                id=chart_id,  
                height=height,
                width="100%",
            ),
            height=height,
            width="100%",
        ),
        width="100%",
        padding="1.5em",
        background="white",
        border_radius="md",
        border="1px solid #EEE",
        margin_top="1.5em",
        margin_bottom="1.5em",
    )
