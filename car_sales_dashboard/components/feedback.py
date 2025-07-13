"""
User feedback components for the Car Sales Dashboard.

This module provides user-friendly feedback components for errors, 
loading states, and validation messages.
"""

import reflex as rx
from typing import Optional


def create_error_alert(
    message: str, 
    title: str = "Error", 
    dismissible: bool = True,
    variant: str = "warning"
) -> rx.Component:
    """
    Create a user-friendly error alert component.
    
    Args:
        message: The error message to display
        title: The alert title
        dismissible: Whether the alert can be dismissed
        variant: Alert style (warning, danger, info)
        
    Returns:
        Reflex alert component
    """
    icon_map = {
        "warning": "⚠️",
        "danger": "❌", 
        "info": "ℹ️",
        "success": "✅"
    }
    
    color_map = {
        "warning": "orange",
        "danger": "red",
        "info": "blue", 
        "success": "green"
    }
    
    icon = icon_map.get(variant, "⚠️")
    color = color_map.get(variant, "orange")
    
    return rx.box(
        rx.hstack(
            rx.text(icon, font_size="1.2em"),
            rx.vstack(
                rx.text(title, font_weight="bold", color=f"{color}.600"),
                rx.text(message, color=f"{color}.700", font_size="0.9em"),
                align_items="start",
                spacing="1"
            ),
            spacing="3",
            align_items="start"
        ),
        bg=f"{color}.50",
        border=f"1px solid",
        border_color=f"{color}.200",
        border_radius="md",
        padding="4",
        margin="2"
    )


def create_loading_spinner(message: str = "Loading...") -> rx.Component:
    """
    Create a loading spinner with message.
    
    Args:
        message: Loading message to display
        
    Returns:
        Reflex loading component
    """
    return rx.center(
        rx.vstack(
            rx.spinner(size="lg", color="blue.500"),
            rx.text(message, color="gray.600", font_size="sm"),
            spacing="3"
        ),
        padding="8"
    )


def create_validation_message(
    field_name: str,
    error_message: str,
    suggestion: Optional[str] = None
) -> rx.Component:
    """
    Create a validation error message for form fields.
    
    Args:
        field_name: Name of the field with validation error
        error_message: The validation error message
        suggestion: Optional suggestion for fixing the error
        
    Returns:
        Reflex validation message component
    """
    return rx.box(
        rx.vstack(
            rx.text(
                f"⚠️ {field_name}: {error_message}",
                color="red.600",
                font_size="sm",
                font_weight="medium"
            ),
            rx.cond(
                suggestion,
                rx.text(
                    f"💡 {suggestion}",
                    color="blue.600",
                    font_size="xs",
                    font_style="italic"
                )
            ),
            spacing="1",
            align_items="start"
        ),
        bg="red.50",
        border="1px solid",
        border_color="red.200",
        border_radius="sm",
        padding="2",
        margin_top="1"
    )


def create_success_message(message: str) -> rx.Component:
    """
    Create a success message component.
    
    Args:
        message: Success message to display
        
    Returns:
        Reflex success message component
    """
    return rx.box(
        rx.hstack(
            rx.text("✅", font_size="1.1em"),
            rx.text(message, color="green.700", font_weight="medium"),
            spacing="2"
        ),
        bg="green.50",
        border="1px solid",
        border_color="green.200",
        border_radius="md",
        padding="3",
        margin="2"
    )


def create_info_tooltip(
    content: str,
    tooltip_text: str,
    position: str = "top"
) -> rx.Component:
    """
    Create an informational tooltip component.
    
    Args:
        content: The content to show the tooltip on
        tooltip_text: The tooltip text
        position: Tooltip position (top, bottom, left, right)
        
    Returns:
        Reflex tooltip component
    """
    return rx.tooltip(
        rx.hstack(
            rx.text(content),
            rx.text("ℹ️", color="blue.500", font_size="0.8em"),
            spacing="1"
        ),
        label=tooltip_text,
        placement=position
    )


def create_chart_placeholder(chart_name: str, reason: str = "No data available") -> rx.Component:
    """
    Create a placeholder for charts when data is not available.
    
    Args:
        chart_name: Name of the chart
        reason: Reason why chart is not available
        
    Returns:
        Reflex placeholder component
    """
    return rx.center(
        rx.vstack(
            rx.text("📊", font_size="3em", color="gray.300"),
            rx.text(f"{chart_name} Chart", font_weight="bold", color="gray.600"),
            rx.text(reason, color="gray.500", font_size="sm", text_align="center"),
            rx.text(
                "Try adjusting your filters or selecting a different date range",
                color="gray.400",
                font_size="xs",
                text_align="center",
                font_style="italic"
            ),
            spacing="2",
            align_items="center"
        ),
        height="300px",
        border="2px dashed",
        border_color="gray.200",
        border_radius="lg",
        bg="gray.50"
    )


def create_data_quality_indicator(
    data_points: int,
    quality_score: float,
    recommendations: list[str] = None
) -> rx.Component:
    """
    Create a data quality indicator for forecasts.
    
    Args:
        data_points: Number of data points available
        quality_score: Quality score from 0-1
        recommendations: Optional list of recommendations
        
    Returns:
        Reflex data quality component
    """
    if quality_score >= 0.8:
        color = "green"
        icon = "✅"
        status = "Excellent"
    elif quality_score >= 0.6:
        color = "yellow"
        icon = "⚠️"
        status = "Good"
    else:
        color = "red"
        icon = "❌"
        status = "Poor"
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(icon),
                rx.text(f"Data Quality: {status}", font_weight="bold"),
                spacing="2"
            ),
            rx.text(f"Data Points: {data_points}", font_size="sm", color="gray.600"),
            rx.text(f"Quality Score: {quality_score:.1%}", font_size="sm", color="gray.600"),
            rx.cond(
                recommendations,
                rx.vstack(
                    rx.text("Recommendations:", font_size="sm", font_weight="medium"),
                    rx.vstack(
                        *[rx.text(f"• {rec}", font_size="xs") for rec in recommendations or []],
                        spacing="1"
                    ),
                    spacing="1"
                )
            ),
            spacing="2",
            align_items="start"
        ),
        bg=f"{color}.50",
        border="1px solid",
        border_color=f"{color}.200",
        border_radius="md",
        padding="3",
        margin="2",
        max_width="300px"
    )
