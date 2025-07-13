"""
Data Validation and Input Sanitization Module

Provides comprehensive validation and sanitization for all user inputs,
data uploads, and system parameters to ensure data integrity and security.
"""

import re
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, date
import logging
from ..exceptions import DataValidationError

logger = logging.getLogger(__name__)


class InputSanitizer:
    """Handles sanitization of all user inputs"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 255, allow_special: bool = False) -> str:
        """Sanitize string input to prevent injection attacks"""
        if not isinstance(value, str):
            value = str(value)
        
        # Remove null bytes and control characters
        value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
        
        # Trim whitespace
        value = value.strip()
        
        # Limit length
        if len(value) > max_length:
            value = value[:max_length]
        
        # Remove potentially dangerous characters if not allowing special chars
        if not allow_special:
            value = re.sub(r'[<>"\';\\&]', '', value)
        
        return value
    
    @staticmethod
    def sanitize_numeric(value: Union[str, int, float], 
                        min_val: Optional[float] = None,
                        max_val: Optional[float] = None) -> float:
        """Sanitize and validate numeric input"""
        try:
            if isinstance(value, str):
                # Remove non-numeric characters except decimal point and negative sign
                value = re.sub(r'[^\d.-]', '', value)
                if value == '' or value == '-' or value == '.':
                    raise ValueError("Invalid numeric format")
            
            num_value = float(value)
            
            # Check for NaN or infinity
            if np.isnan(num_value) or np.isinf(num_value):
                raise ValueError("Invalid numeric value")
            
            # Apply bounds
            if min_val is not None and num_value < min_val:
                num_value = min_val
            if max_val is not None and num_value > max_val:
                num_value = max_val
                
            return num_value
            
        except (ValueError, TypeError) as e:
            raise DataValidationError(
                field_name="numeric_input",
                value=value,
                reason=f"Invalid numeric input: {value}"
            ) from e


class DataValidator:
    """Comprehensive data validation for the dashboard"""
    
    REQUIRED_COLUMNS = {
        'sales_data': ['date', 'sales_volume', 'gas_price', 'cpi', 'search_volume'],
        'predictions': ['date', 'predicted_sales', 'confidence_interval']
    }
    
    NUMERIC_COLUMNS = {
        'sales_data': ['sales_volume', 'gas_price', 'cpi', 'search_volume'],
        'predictions': ['predicted_sales', 'confidence_interval']
    }
    
    DATE_COLUMNS = ['date']
    
    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame, data_type: str = 'sales_data') -> Tuple[bool, List[str]]:
        """Validate DataFrame structure and content"""
        errors = []
        
        if df is None or df.empty:
            errors.append("DataFrame is empty or None")
            return False, errors
        
        # Check required columns
        required_cols = cls.REQUIRED_COLUMNS.get(data_type, [])
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")
        
        # Validate numeric columns
        numeric_cols = cls.NUMERIC_COLUMNS.get(data_type, [])
        for col in numeric_cols:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    errors.append(f"Column '{col}' must be numeric")
                elif df[col].isna().all():
                    errors.append(f"Column '{col}' contains only null values")
                elif (df[col] < 0).any():
                    errors.append(f"Column '{col}' contains negative values")
        
        # Validate date columns
        for col in cls.DATE_COLUMNS:
            if col in df.columns:
                try:
                    pd.to_datetime(df[col])
                except Exception:
                    errors.append(f"Column '{col}' contains invalid date format")
        
        # Check for duplicate dates
        if 'date' in df.columns:
            if df['date'].duplicated().any():
                errors.append("Dataset contains duplicate dates")
        
        # Data quality checks
        if len(df) < 10:
            errors.append("Dataset too small (minimum 10 records required)")
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_modifiers(cls, gas_price: float, cpi: float, search_volume: float) -> Tuple[bool, List[str]]:
        """Validate scenario modifier values"""
        errors = []
        
        # Gas price modifier validation
        if not 0.1 <= gas_price <= 3.0:
            errors.append(f"Gas price modifier must be between 0.1 and 3.0, got {gas_price}")
        
        # CPI modifier validation  
        if not 0.1 <= cpi <= 3.0:
            errors.append(f"CPI modifier must be between 0.1 and 3.0, got {cpi}")
        
        # Search volume modifier validation
        if not 0.1 <= search_volume <= 3.0:
            errors.append(f"Search volume modifier must be between 0.1 and 3.0, got {search_volume}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_date_range(cls, start_date: Union[str, date], end_date: Union[str, date]) -> Tuple[bool, List[str]]:
        """Validate date range inputs"""
        errors = []
        
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start_date >= end_date:
                errors.append("Start date must be before end date")
            
            # Check if date range is reasonable (not too far in past/future)
            today = date.today()
            if start_date < date(2000, 1, 1):
                errors.append("Start date cannot be before year 2000")
            if end_date > date(today.year + 10, 12, 31):
                errors.append("End date cannot be more than 10 years in the future")
                
        except ValueError as e:
            errors.append(f"Invalid date format: {e}")
        
        return len(errors) == 0, errors


class FileValidator:
    """Validates uploaded files and their content"""
    
    ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.xls']
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    @classmethod
    def validate_file_upload(cls, file_path: str, file_size: int) -> Tuple[bool, List[str]]:
        """Validate file upload parameters"""
        errors = []
        
        # Check file extension
        file_ext = '.' + file_path.split('.')[-1].lower()
        if file_ext not in cls.ALLOWED_EXTENSIONS:
            errors.append(f"File type not allowed. Supported: {cls.ALLOWED_EXTENSIONS}")
        
        # Check file size
        if file_size > cls.MAX_FILE_SIZE:
            errors.append(f"File too large. Maximum size: {cls.MAX_FILE_SIZE / (1024*1024):.1f}MB")
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_csv_content(cls, file_path: str) -> Tuple[bool, List[str], Optional[pd.DataFrame]]:
        """Validate CSV file content and structure"""
        errors = []
        df = None
        
        try:
            # Try to read the file
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                errors.append("Unsupported file format")
                return False, errors, None
            
            # Validate the DataFrame
            is_valid, validation_errors = DataValidator.validate_dataframe(df)
            errors.extend(validation_errors)
            
        except Exception as e:
            errors.append(f"Error reading file: {str(e)}")
        
        return len(errors) == 0, errors, df


def sanitize_chart_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize chart configuration parameters"""
    sanitizer = InputSanitizer()
    
    # Sanitize string fields
    if 'title' in config:
        config['title'] = sanitizer.sanitize_string(config['title'], max_length=100)
    
    if 'x_label' in config:
        config['x_label'] = sanitizer.sanitize_string(config['x_label'], max_length=50)
    
    if 'y_label' in config:
        config['y_label'] = sanitizer.sanitize_string(config['y_label'], max_length=50)
    
    # Sanitize numeric fields
    if 'width' in config:
        config['width'] = sanitizer.sanitize_numeric(config['width'], min_val=200, max_val=2000)
    
    if 'height' in config:
        config['height'] = sanitizer.sanitize_numeric(config['height'], min_val=200, max_val=1500)
    
    return config


def sanitize_output(data: Any) -> Any:
    """Sanitize output data before sending to frontend"""
    if isinstance(data, dict):
        return {key: sanitize_output(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_output(item) for item in data]
    elif isinstance(data, str):
        # More thorough string sanitization for output
        sanitized = InputSanitizer.sanitize_string(data, allow_special=True)
        # Remove any remaining script-like content
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'<iframe[^>]*>.*?</iframe>', '', sanitized, flags=re.IGNORECASE)
        return sanitized
    elif isinstance(data, (int, float)):
        if np.isnan(data) or np.isinf(data):
            return None
        return data
    else:
        return data
