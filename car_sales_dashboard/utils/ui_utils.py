"""
UI utilities for error handling and fallback components.
"""
import reflex as rx
from car_sales_dashboard.exceptions import ChartBuildError
from car_sales_dashboard.utils.logging_config import logger


def create_chart_error_component(error: ChartBuildError, height: str = "400px") -> rx.Component:
    """
    Create a user-friendly error component when chart building fails.
    
    This replaces silent failure with fake charts, showing users there's an issue
    while preserving debugging information in logs.
    
    Args:
        error: The ChartBuildError that occurred
        height: Height of the error component to match expected chart size
        
    Returns:
        rx.Component: Error display component
    """
    # Log the full error details for debugging
    logger.error(f"Chart build failed - {error.chart_type}: {error.original_error}")
    if error.data_info:
        logger.error(f"Data context: {error.data_info}")
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("⚠️", font_size="2em", color="#ff6b6b"),
                rx.text(
                    f"Failed to render {error.chart_type} chart", 
                    font_weight="bold",
                    color="#d63384",
                    font_size="1.1em"
                ),
                justify="center",
                align="center",
                spacing="2"
            ),
            rx.text(
                "See application logs for details",
                color="#6c757d", 
                font_size="0.9em",
                text_align="center"
            ),
            rx.text(
                "Please check your data or contact support if this persists",
                color="#6c757d",
                font_size="0.8em", 
                text_align="center",
                margin_top="0.5em"
            ),
            justify="center",
            align="center",
            spacing="3",
            height="100%"
        ),
        height=height,
        width="100%",
        border="2px dashed #dee2e6",
        border_radius="8px",
        background="rgba(248, 249, 250, 0.8)",
        display="flex",
        align_items="center",
        justify_content="center",
        padding="2em"
    )


def create_data_error_component(message: str, height: str = "200px") -> rx.Component:
    """
    Create an error component for data-related issues.
    
    Args:
        message: Error message to display
        height: Height of the error component
        
    Returns:
        rx.Component: Error display component
    """
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("📊", font_size="1.5em", color="#ffc107"),
                rx.text(
                    "Data Issue",
                    font_weight="bold", 
                    color="#856404",
                    font_size="1em"
                ),
                justify="center",
                align="center",
                spacing="2"
            ),
            rx.text(
                message,
                color="#856404",
                font_size="0.9em",
                text_align="center"
            ),
            justify="center",
            align="center", 
            spacing="2",
            height="100%"
        ),
        height=height,
        width="100%",
        border="1px solid #ffeaa7",
        border_radius="6px",
        background="rgba(255, 243, 205, 0.3)",
        display="flex",
        align_items="center",
        justify_content="center",
        padding="1em"
    )
