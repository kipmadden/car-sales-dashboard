"""
Logging configuration for the Car Sales Dashboard.

This module provides centralized logging configuration with support for:
- Different log levels (DEBUG, INFO, WARNING, ERROR)
- Console and file output
- Production vs development modes
- Performance monitoring
"""
import logging
import logging.handlers
import os
import sys
from typing import Optional
from pathlib import Path


class DashboardLogger:
    """Centralized logger for the car sales dashboard application."""
    
    _instance: Optional['DashboardLogger'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'DashboardLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.setup_logging()
            self._initialized = True
    
    def setup_logging(self, debug_mode: bool = None) -> None:
        """
        Set up logging configuration for the application.
        
        Args:
            debug_mode: If True, enables DEBUG level logging. 
                       If None, checks environment variables.
        """
        # Determine debug mode from environment or parameter
        if debug_mode is None:
            debug_mode = os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes', 'on')
        
        # Set log level based on debug mode
        log_level = logging.DEBUG if debug_mode else logging.INFO
        
        # Create logs directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Clear any existing handlers
        root_logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            fmt='%(levelname)s - %(name)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING if not debug_mode else logging.DEBUG)
        console_handler.setFormatter(simple_formatter if not debug_mode else detailed_formatter)
        root_logger.addHandler(console_handler)
        
        # File handler for all logs
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_dir / 'dashboard.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
        # Error file handler for errors and above
        error_handler = logging.handlers.RotatingFileHandler(
            filename=log_dir / 'dashboard_errors.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
        
        # Configure specific loggers to reduce noise from dependencies
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
        logging.getLogger('plotly').setLevel(logging.WARNING)
        logging.getLogger('pandas').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('reflex').setLevel(logging.INFO)
        
        # Log the configuration
        logger = self.get_logger('dashboard.logging')
        logger.info(f"Logging configured - Debug mode: {debug_mode}, Level: {logging.getLevelName(log_level)}")
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger instance for the specified module.
        
        Args:
            name: Name of the logger (typically __name__ of the module)
            
        Returns:
            Logger instance configured for the dashboard
        """
        return logging.getLogger(name)
    
    def set_debug_mode(self, enabled: bool) -> None:
        """
        Enable or disable debug mode at runtime.
        
        Args:
            enabled: Whether to enable debug mode
        """
        level = logging.DEBUG if enabled else logging.INFO
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Update console handler level
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                handler.setLevel(logging.DEBUG if enabled else logging.WARNING)
        
        logger = self.get_logger('dashboard.logging')
        logger.info(f"Debug mode {'enabled' if enabled else 'disabled'}")


# Global logger instance
_dashboard_logger = DashboardLogger()


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance for the current module.
    
    Args:
        name: Name of the logger. If None, uses the caller's module name.
        
    Returns:
        Logger instance
        
    Usage:
        logger = get_logger(__name__)
        logger.info("This is an info message")
        logger.debug("This is a debug message")
        logger.error("This is an error message")
    """
    if name is None:
        # Try to get the caller's module name
        import inspect
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back
            name = caller_frame.f_globals.get('__name__', 'dashboard')
        finally:
            del frame
    
    return _dashboard_logger.get_logger(name)


def enable_debug_mode() -> None:
    """Enable debug mode for more verbose logging."""
    _dashboard_logger.set_debug_mode(True)


def disable_debug_mode() -> None:
    """Disable debug mode for production logging."""
    _dashboard_logger.set_debug_mode(False)


def setup_logging(debug_mode: bool = None) -> None:
    """
    Set up logging configuration. Can be called multiple times.
    
    Args:
        debug_mode: Whether to enable debug mode
    """
    _dashboard_logger.setup_logging(debug_mode)


# Performance monitoring utilities
class PerformanceLogger:
    """Helper class for performance monitoring and logging."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_function_call(self, func_name: str, **kwargs) -> None:
        """Log a function call with parameters."""
        params = ', '.join(f"{k}={v}" for k, v in kwargs.items())
        self.logger.debug(f"Calling {func_name}({params})")
    
    def log_data_operation(self, operation: str, data_info: str) -> None:
        """Log data operations like filtering, forecasting, etc."""
        self.logger.info(f"Data operation: {operation} - {data_info}")
    
    def log_chart_creation(self, chart_type: str, data_shape: tuple = None, success: bool = True) -> None:
        """Log chart creation operations."""
        shape_info = f" (data shape: {data_shape})" if data_shape else ""
        status = "succeeded" if success else "failed"
        self.logger.info(f"Chart creation {status}: {chart_type}{shape_info}")
    
    def log_user_action(self, action: str, details: str = None) -> None:
        """Log user interactions."""
        detail_info = f" - {details}" if details else ""
        self.logger.info(f"User action: {action}{detail_info}")


def get_performance_logger(name: str = None) -> PerformanceLogger:
    """Get a performance logger for monitoring operations."""
    logger = get_logger(name)
    return PerformanceLogger(logger)


# Module-level logger instances for easy importing
logger = get_logger('dashboard')
perf_logger = get_performance_logger('dashboard.performance')
