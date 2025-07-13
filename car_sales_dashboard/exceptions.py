"""
Custom exceptions for the Car Sales Dashboard application.
"""

class ChartBuildError(Exception):
    """
    Custom exception raised when chart creation fails.
    
    This exception bubbles up to the UI layer to show users
    that chart rendering failed while preserving the root cause
    for debugging in logs.
    """
    
    def __init__(self, chart_type: str, original_error: Exception, data_info: str = ""):
        """
        Initialize ChartBuildError.
        
        Args:
            chart_type: The type of chart that failed to build
            original_error: The original exception that caused the failure
            data_info: Optional information about the data that caused the failure
        """
        self.chart_type = chart_type
        self.original_error = original_error
        self.data_info = data_info
        
        # Create a descriptive error message
        error_msg = f"Failed to build {chart_type} chart: {str(original_error)}"
        if data_info:
            error_msg += f" (Data: {data_info})"
            
        super().__init__(error_msg)
        
    def __str__(self):
        return f"ChartBuildError[{self.chart_type}]: {self.original_error}"


class DataValidationError(Exception):
    """
    Custom exception raised when data validation fails.
    
    Used to validate user inputs, data integrity, and business logic constraints.
    """
    
    def __init__(self, field_name: str, value, reason: str, suggestion: str = ""):
        """
        Initialize DataValidationError.
        
        Args:
            field_name: The name of the field that failed validation
            value: The invalid value that was provided
            reason: Why the validation failed
            suggestion: Optional suggestion for fixing the issue
        """
        self.field_name = field_name
        self.value = value
        self.reason = reason
        self.suggestion = suggestion
        
        error_msg = f"Invalid {field_name}: {reason}"
        if suggestion:
            error_msg += f" Suggestion: {suggestion}"
            
        super().__init__(error_msg)


class ModelTrainingError(Exception):
    """
    Custom exception raised when ML model training fails.
    
    Used to handle forecast model initialization and training issues.
    """
    
    def __init__(self, model_type: str, error_details: str, data_shape: tuple = None):
        """
        Initialize ModelTrainingError.
        
        Args:
            model_type: The type of model that failed to train
            error_details: Detailed error information
            data_shape: Optional shape of the training data
        """
        self.model_type = model_type
        self.error_details = error_details
        self.data_shape = data_shape
        
        error_msg = f"Failed to train {model_type} model: {error_details}"
        if data_shape:
            error_msg += f" (Data shape: {data_shape})"
            
        super().__init__(error_msg)


class ConfigurationError(Exception):
    """
    Custom exception raised when application configuration is invalid.
    
    Used for environment variables, settings, and deployment configuration issues.
    """
    
    def __init__(self, config_key: str, issue: str, expected: str = ""):
        """
        Initialize ConfigurationError.
        
        Args:
            config_key: The configuration key that is problematic
            issue: Description of the configuration issue
            expected: Optional description of expected configuration
        """
        self.config_key = config_key
        self.issue = issue
        self.expected = expected
        
        error_msg = f"Configuration error for '{config_key}': {issue}"
        if expected:
            error_msg += f" Expected: {expected}"
            
        super().__init__(error_msg)
