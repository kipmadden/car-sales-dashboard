"""
Chart components that can be rendered with client-side data.

This module provides a custom chart component that can be rendered with data
from client-side effects to avoid EventHandler errors. This approach separates
the UI structure from the data loading logic.
"""

import reflex as rx

def responsive_chart_container(title: str, chart_id: str, height: str = "500px"):
    """
    Create a responsive chart container that will be updated by client-side effects.
    
    Args:
        title (str): The title of the chart
        chart_id (str): The ID to be used for client-side targeting
        height (str): The height of the chart container
        
    Returns:
        rx.Component: A container component that will render a Plotly chart
    """
    return rx.box(
        rx.heading(title, color="black", size="4"),
        rx.center(
            rx.plotly(
                id=chart_id,  # Important: This ID will be targeted by client-side effects
                height=height,
                width="100%",  # Make the chart responsive
            ),
            rx.html("""
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        // This ensures we have a placeholder until the real chart arrives
                        const plotDiv = document.getElementById('__placeholder__');
                        if (plotDiv) {
                            console.log('Setting up chart placeholder for: ' + plotDiv.id);
                        }
                    });
                </script>
            """),
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
