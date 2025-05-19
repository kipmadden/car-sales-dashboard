"""
Simplified chart component for static rendering.

This module provides a simplified chart component for static rendering,
removing complex client-side effects and using direct state values instead.
"""

import reflex as rx
import plotly.graph_objects as go
import pandas as pd

def create_static_chart(title: str, chart_data: dict = None, height: str = "500px"):
    """
    Create a static chart container with the provided chart data.
    
    Args:
        title (str): The title of the chart
        chart_data (dict): The Plotly figure data as a dictionary
        height (str): The height of the chart container
        
    Returns:
        rx.Component: A container component with a static Plotly chart
    """
    # Create a fallback empty chart if no data is provided
    if not chart_data:
        chart_data = create_empty_chart()
    
    return rx.box(
        rx.heading(title, color="black", size="4"),
        rx.center(
            rx.plotly(
                figure=chart_data,
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
