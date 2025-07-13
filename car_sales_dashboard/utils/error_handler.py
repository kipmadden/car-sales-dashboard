"""
Enhanced error handling utilities for the Car Sales Dashboard.

This module provides comprehensive error handling, user feedback, and 
graceful degradation strategies for production deployment.
"""

import traceback
from typing import Dict, Any, Optional, Callable, Union
import functools
import logging
from car_sales_dashboard.exceptions import (
    ChartBuildError, 
    DataValidationError, 
    ModelTrainingError, 
    ConfigurationError
)

logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    Centralized error handling with user-friendly feedback and logging.
    """
    
    # Error type mappings for user-friendly messages
    ERROR_MESSAGES = {
        'chart_build': "Unable to generate chart. Please check your data selection and try again.",
        'data_validation': "The provided data is invalid. Please review your inputs.",
        'model_training': "Forecasting model initialization failed. Please try refreshing the page.",
        'configuration': "Application configuration error. Please contact support.",
        'network': "Network connection issue. Please check your internet connection.",
        'permission': "Insufficient permissions. Please contact your administrator.",
        'generic': "An unexpected error occurred. Please try again or contact support."
    }
    
    @staticmethod
    def handle_chart_error(
        chart_type: str, 
        error: Exception, 
        data_info: str = "",
        fallback_chart: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Handle chart building errors with graceful fallback.
        
        Args:
            chart_type: Type of chart that failed
            error: The original exception
            data_info: Information about the data that caused the error
            fallback_chart: Optional fallback chart generation function
            
        Returns:
            Either the fallback chart or an error chart display
        """
        # Log the detailed error for debugging
        logger.error(f"Chart build failed [{chart_type}]: {error}", exc_info=True)
        if data_info:
            logger.error(f"Data context: {data_info}")
        
        # Try fallback chart if provided
        if fallback_chart:
            try:
                logger.info(f"Attempting fallback chart for {chart_type}")
                return fallback_chart()
            except Exception as fallback_error:
                logger.error(f"Fallback chart also failed: {fallback_error}")
        
        # Return error chart as last resort
        return ErrorHandler._create_error_chart(chart_type, "chart_build")
    
    @staticmethod
    def handle_data_validation(
        field_name: str,
        value: Any,
        validator: Callable,
        suggestion: str = ""
    ) -> tuple[bool, Optional[str]]:
        """
        Handle data validation with helpful error messages.
        
        Args:
            field_name: Name of the field being validated
            value: Value to validate
            validator: Validation function that returns (is_valid, error_message)
            suggestion: Optional suggestion for fixing the issue
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            is_valid, error_message = validator(value)
            if not is_valid:
                logger.warning(f"Validation failed for {field_name}: {error_message}")
                user_message = f"Invalid {field_name}: {error_message}"
                if suggestion:
                    user_message += f" {suggestion}"
                return False, user_message
            return True, None
            
        except Exception as e:
            logger.error(f"Validation error for {field_name}: {e}", exc_info=True)
            return False, ErrorHandler.ERROR_MESSAGES['data_validation']
    
    @staticmethod
    def handle_model_error(
        model_type: str,
        error: Exception,
        data_shape: Optional[tuple] = None,
        retry_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Handle model training/prediction errors.
        
        Args:
            model_type: Type of model that failed
            error: The original exception
            data_shape: Shape of the data being processed
            retry_callback: Optional callback to retry the operation
            
        Returns:
            Error information dictionary
        """
        logger.error(f"Model error [{model_type}]: {error}", exc_info=True)
        if data_shape:
            logger.error(f"Data shape: {data_shape}")
        
        # Check if this is a known recoverable error
        if "insufficient data" in str(error).lower():
            return {
                "error": True,
                "message": "Not enough data to train the forecasting model. Please select a larger date range or fewer filters.",
                "recoverable": True,
                "suggestion": "Try reducing the number of filters or selecting a longer time period."
            }
        
        if "memory" in str(error).lower():
            return {
                "error": True,
                "message": "The dataset is too large to process. Please apply more filters to reduce the data size.",
                "recoverable": True,
                "suggestion": "Try filtering by specific regions, vehicle types, or date ranges."
            }
        
        # Generic model error
        return {
            "error": True,
            "message": ErrorHandler.ERROR_MESSAGES['model_training'],
            "recoverable": False,
            "suggestion": "Please refresh the page and try again. If the problem persists, contact support."
        }
    
    @staticmethod
    def _create_error_chart(chart_type: str, error_category: str) -> Dict[str, Any]:
        """
        Create a user-friendly error chart display.
        
        Args:
            chart_type: Type of chart that failed
            error_category: Category of error for appropriate messaging
            
        Returns:
            Plotly chart dictionary showing error message
        """
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        # Get appropriate error message
        message = ErrorHandler.ERROR_MESSAGES.get(error_category, ErrorHandler.ERROR_MESSAGES['generic'])
        
        # Add error message as annotation
        fig.add_annotation(
            text=f"⚠️ {message}",
            xref="paper", yref="paper",
            x=0.5, y=0.6,
            showarrow=False,
            font=dict(color="#d63384", size=18, family="Arial"),
            align="center"
        )
        
        # Add suggestion annotation
        fig.add_annotation(
            text="Try adjusting your filters or refreshing the page",
            xref="paper", yref="paper",
            x=0.5, y=0.4,
            showarrow=False,
            font=dict(color="#6c757d", size=14, family="Arial"),
            align="center"
        )
        
        # Style the error chart
        fig.update_layout(
            title=f"{chart_type} - Temporarily Unavailable",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400,
            paper_bgcolor="rgba(248, 249, 250, 0.9)",
            plot_bgcolor="rgba(248, 249, 250, 0.9)",
            font=dict(color="black"),
            margin=dict(t=60, b=40, l=40, r=40)
        )
        
        return fig.to_dict()


def error_handler(error_type: str = "generic", fallback_value: Any = None):
    """
    Decorator for automatic error handling with logging and user feedback.
    
    Args:
        error_type: Type of error for appropriate user messaging
        fallback_value: Value to return if the function fails
        
    Usage:
        @error_handler("chart_build", fallback_value={})
        def create_chart():
            # chart creation logic
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the error with full context
                logger.error(
                    f"Error in {func.__name__}: {e}",
                    exc_info=True,
                    extra={
                        'function': func.__name__,
                        'function_args': str(args)[:200],  # Renamed to avoid conflict
                        'function_kwargs': str(kwargs)[:200],  # Renamed to avoid conflict
                        'error_type': error_type
                    }
                )
                
                # Return appropriate fallback
                if error_type == "chart_build":
                    return ErrorHandler._create_error_chart(
                        func.__name__.replace('create_', '').replace('_chart', '').title(),
                        error_type
                    )
                
                return fallback_value
        
        return wrapper
    return decorator


def validate_input(validator: Callable, error_message: str = "Invalid input"):
    """
    Decorator for input validation with consistent error handling.
    
    Args:
        validator: Function that takes the first argument and returns (is_valid, message)
        error_message: Custom error message for validation failures
        
    Usage:
        @validate_input(lambda x: (x > 0, "Value must be positive"))
        def process_value(value):
            # processing logic
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if args:  # Validate first argument
                is_valid, validation_message = validator(args[0])
                if not is_valid:
                    error_msg = f"{error_message}: {validation_message}"
                    logger.warning(f"Input validation failed in {func.__name__}: {error_msg}")
                    raise DataValidationError(
                        field_name=func.__name__,
                        value=args[0],
                        reason=validation_message
                    )
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Specific validators for common use cases
class Validators:
    """Common validation functions for dashboard inputs."""
    
    @staticmethod
    def positive_number(value: Union[int, float]) -> tuple[bool, str]:
        """Validate that a number is positive."""
        try:
            num = float(value)
            if num <= 0:
                return False, "must be greater than 0"
            return True, ""
        except (ValueError, TypeError):
            return False, "must be a valid number"
    
    @staticmethod
    def date_range(value: Any) -> tuple[bool, str]:
        """Validate date range inputs."""
        if not value:
            return False, "date range cannot be empty"
        # Add more specific date validation as needed
        return True, ""
    
    @staticmethod
    def percentage(value: Union[int, float]) -> tuple[bool, str]:
        """Validate percentage values (0-100)."""
        try:
            num = float(value)
            if not (0 <= num <= 100):
                return False, "must be between 0 and 100"
            return True, ""
        except (ValueError, TypeError):
            return False, "must be a valid percentage"
    
    @staticmethod
    def modifier_range(value: Union[int, float]) -> tuple[bool, str]:
        """Validate modifier values (typically 0.1 to 3.0)."""
        try:
            num = float(value)
            if not (0.1 <= num <= 3.0):
                return False, "must be between 0.1 and 3.0"
            return True, ""
        except (ValueError, TypeError):
            return False, "must be a valid modifier value"
