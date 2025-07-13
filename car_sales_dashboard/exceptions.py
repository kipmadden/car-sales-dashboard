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
