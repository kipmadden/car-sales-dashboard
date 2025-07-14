"""
Unit Tests for Car Sales Dashboard

Comprehensive unit testing module using pytest framework.
Tests core functionality without requiring Reflex imports.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestDataGeneration:
    """Test data generation and validation"""
    
    def test_sales_data_generation(self):
        """Test basic sales data generation"""
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        data = TestDataGenerator.generate_sales_data(rows=100, seed=42)
        
        # Check basic structure
        assert len(data) == 100
        assert 'date' in data.columns
        assert 'sales_volume' in data.columns
        assert 'gas_price' in data.columns
        
        # Check data types
        assert pd.api.types.is_datetime64_any_dtype(data['date'])
        assert pd.api.types.is_numeric_dtype(data['sales_volume'])
        assert pd.api.types.is_numeric_dtype(data['gas_price'])
        
        # Check value ranges
        assert data['sales_volume'].min() >= 0
        assert data['gas_price'].min() > 0
        assert data['gas_price'].max() < 10  # Reasonable gas price range
    
    def test_forecast_data_generation(self):
        """Test forecast data generation"""
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        # Generate historical data
        historical_data = TestDataGenerator.generate_sales_data(rows=365)
        
        # Generate forecast
        forecast_data = TestDataGenerator.generate_forecast_data(historical_data, forecast_months=6)
        
        # Check structure
        assert 'date' in forecast_data.columns
        assert 'predicted_sales' in forecast_data.columns
        assert 'confidence_lower' in forecast_data.columns
        assert 'confidence_upper' in forecast_data.columns
        
        # Check date continuity
        last_historical_date = historical_data['date'].max()
        first_forecast_date = forecast_data['date'].min()
        assert first_forecast_date > last_historical_date
        
        # Check confidence intervals
        assert (forecast_data['confidence_lower'] <= forecast_data['predicted_sales']).all()
        assert (forecast_data['predicted_sales'] <= forecast_data['confidence_upper']).all()
    
    def test_data_consistency(self):
        """Test data generation consistency with same seed"""
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        data1 = TestDataGenerator.generate_sales_data(rows=100, seed=42)
        data2 = TestDataGenerator.generate_sales_data(rows=100, seed=42)
        
        # Should be identical with same seed
        pd.testing.assert_frame_equal(data1, data2)
        
        # Different seeds should produce different data
        data3 = TestDataGenerator.generate_sales_data(rows=100, seed=123)
        assert not data1.equals(data3)


class TestDataValidation:
    """Test data validation functionality"""
    
    def test_input_sanitizer(self):
        """Test input sanitization"""
        from car_sales_dashboard.utils.validation import InputSanitizer
        
        # Test string sanitization
        clean_string = InputSanitizer.sanitize_string("   Hello World!   ")
        assert clean_string == "Hello World!"
        
        # Test malicious input
        malicious_input = "<script>alert('xss')</script>Hello"
        clean_string = InputSanitizer.sanitize_string(malicious_input)
        assert "<script>" not in clean_string
        assert "Hello" in clean_string
        
        # Test numeric sanitization
        assert InputSanitizer.sanitize_numeric("123.45") == 123.45
        assert InputSanitizer.sanitize_numeric("invalid") == 0.0
        assert InputSanitizer.sanitize_numeric("-10", min_value=0) == 0.0
        assert InputSanitizer.sanitize_numeric("1000", max_value=100) == 100.0
    
    def test_data_validator(self):
        """Test DataFrame validation"""
        from car_sales_dashboard.utils.validation import DataValidator
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        # Valid data
        valid_data = TestDataGenerator.generate_sales_data(100)
        is_valid, errors = DataValidator.validate_dataframe(valid_data, 'sales_data')
        assert is_valid
        assert len(errors) == 0
        
        # Invalid data - missing required columns
        invalid_data = pd.DataFrame({'wrong_column': [1, 2, 3]})
        is_valid, errors = DataValidator.validate_dataframe(invalid_data, 'sales_data')
        assert not is_valid
        assert len(errors) > 0
        
        # Empty data
        empty_data = pd.DataFrame()
        is_valid, errors = DataValidator.validate_dataframe(empty_data, 'sales_data')
        assert not is_valid
    
    def test_file_validator(self):
        """Test file validation"""
        from car_sales_dashboard.utils.validation import FileValidator
        
        # Test file size validation
        assert FileValidator.validate_file_size(1024, max_size_mb=1)  # 1KB < 1MB
        assert not FileValidator.validate_file_size(1024*1024*10, max_size_mb=1)  # 10MB > 1MB
        
        # Test file extension validation
        assert FileValidator.validate_file_extension("data.csv", ['.csv', '.xlsx'])
        assert not FileValidator.validate_file_extension("data.txt", ['.csv', '.xlsx'])


class TestErrorHandling:
    """Test error handling and recovery"""
    
    def test_validators(self):
        """Test validation functions"""
        from car_sales_dashboard.utils.error_handler import Validators
        
        # Test positive number validation
        assert Validators.positive_number(5.5) == 5.5
        assert Validators.positive_number(-1) == 0
        assert Validators.positive_number(0) == 0
        
        # Test date validation
        valid_date = "2023-01-01"
        assert Validators.valid_date(valid_date) == pd.to_datetime(valid_date)
        
        invalid_date = "invalid-date"
        assert Validators.valid_date(invalid_date) == pd.to_datetime("2023-01-01")
        
        # Test percentage validation
        assert Validators.percentage(0.5) == 0.5
        assert Validators.percentage(-0.1) == 0.0
        assert Validators.percentage(1.5) == 1.0
    
    def test_error_handler_chart_creation(self):
        """Test error handler chart creation"""
        from car_sales_dashboard.utils.error_handler import ErrorHandler
        
        # Test successful operation
        def successful_operation():
            return {"data": [1, 2, 3], "layout": {"title": "Test"}}
        
        result = ErrorHandler.handle_chart_error(successful_operation)
        assert result["data"] == [1, 2, 3]
        assert result["layout"]["title"] == "Test"
        
        # Test failed operation
        def failing_operation():
            raise ValueError("Test error")
        
        result = ErrorHandler.handle_chart_error(failing_operation)
        # Should return error chart structure
        assert "data" in result
        assert "layout" in result
        assert "Error" in str(result["layout"].get("title", ""))


class TestPerformance:
    """Test performance optimization features"""
    
    def test_memory_cache(self):
        """Test memory caching functionality"""
        from car_sales_dashboard.utils.performance import MemoryCache
        
        cache = MemoryCache(max_size=100)
        
        # Test basic set/get
        cache.set("key1", "value1", ttl=60)
        assert cache.get("key1") == "value1"
        
        # Test cache miss
        assert cache.get("nonexistent") is None
        
        # Test TTL expiration
        cache.set("temp_key", "temp_value", ttl=0.1)  # 0.1 second TTL
        import time
        time.sleep(0.2)
        assert cache.get("temp_key") is None
        
        # Test cache stats
        stats = cache.get_stats()
        assert "hits" in stats
        assert "misses" in stats
        assert "size" in stats
    
    def test_cached_decorator(self):
        """Test caching decorator"""
        from car_sales_dashboard.utils.performance import cached
        
        call_count = 0
        
        @cached(ttl=60)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call should execute function
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1
        
        # Second call should use cache
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Should not increment
        
        # Different argument should execute function
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count == 2
    
    def test_batch_processor(self):
        """Test batch processing functionality"""
        from car_sales_dashboard.utils.performance import BatchProcessor
        
        processor = BatchProcessor(batch_size=3, max_workers=2)
        
        # Simple processing function
        def process_item(x):
            return x * 2
        
        # Test batch processing
        items = [1, 2, 3, 4, 5, 6, 7]
        results = processor.process_items(items, process_item)
        
        expected = [2, 4, 6, 8, 10, 12, 14]
        assert results == expected


class TestChartComponents:
    """Test chart creation and rendering"""
    
    def test_chart_creation(self):
        """Test basic chart creation"""
        from car_sales_dashboard.components.charts import create_sales_trend_chart
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        # Generate test data
        test_data = TestDataGenerator.generate_sales_data(100)
        
        # Create chart
        chart_dict = create_sales_trend_chart(test_data)
        
        # Verify chart structure
        assert isinstance(chart_dict, dict)
        assert "data" in chart_dict
        assert "layout" in chart_dict
        
        # Verify data structure
        data = chart_dict["data"]
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verify layout structure
        layout = chart_dict["layout"]
        assert isinstance(layout, dict)
        assert "title" in layout
    
    def test_chart_error_handling(self):
        """Test chart error handling with invalid data"""
        from car_sales_dashboard.components.charts import create_sales_trend_chart
        
        # Test with empty data
        empty_data = pd.DataFrame()
        chart_dict = create_sales_trend_chart(empty_data)
        
        # Should return error chart
        assert isinstance(chart_dict, dict)
        assert "data" in chart_dict
        assert "layout" in chart_dict
        
        # Test with malformed data
        bad_data = pd.DataFrame({"wrong_column": [1, 2, 3]})
        chart_dict = create_sales_trend_chart(bad_data)
        
        # Should return error chart
        assert isinstance(chart_dict, dict)


class TestUIComponents:
    """Test UI component functionality"""
    
    def test_accessibility_config(self):
        """Test accessibility configuration"""
        from car_sales_dashboard.utils.ui_components import AccessibilityConfig
        
        config = AccessibilityConfig()
        
        # Test WCAG color compliance
        assert hasattr(config, 'colors')
        assert hasattr(config, 'fonts')
        assert hasattr(config, 'focus_styles')
        
        # Test responsive breakpoints
        breakpoints = config.get_responsive_breakpoints()
        assert 'mobile' in breakpoints
        assert 'tablet' in breakpoints
        assert 'desktop' in breakpoints
    
    def test_loading_states(self):
        """Test loading state components"""
        from car_sales_dashboard.utils.ui_components import LoadingStates
        
        # Test skeleton loader
        skeleton = LoadingStates.create_skeleton_loader()
        assert isinstance(skeleton, dict)
        
        # Test spinner
        spinner = LoadingStates.create_spinner()
        assert isinstance(spinner, dict)
        
        # Test progress bar
        progress = LoadingStates.create_progress_bar(progress=0.5)
        assert isinstance(progress, dict)
    
    def test_error_states(self):
        """Test error state components"""
        from car_sales_dashboard.utils.ui_components import ErrorStates
        
        # Test error message
        error_msg = ErrorStates.create_error_message("Test error", error_type="validation")
        assert isinstance(error_msg, dict)
        
        # Test retry component
        retry_comp = ErrorStates.create_retry_component("Retry action")
        assert isinstance(retry_comp, dict)


class TestIntegration:
    """Integration tests for component interaction"""
    
    def test_full_workflow(self):
        """Test complete data workflow"""
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        from car_sales_dashboard.utils.validation import DataValidator
        from car_sales_dashboard.components.charts import create_sales_trend_chart
        
        # Generate data
        data = TestDataGenerator.generate_sales_data(200)
        
        # Validate data
        is_valid, errors = DataValidator.validate_dataframe(data, 'sales_data')
        assert is_valid
        
        # Create chart
        chart = create_sales_trend_chart(data)
        assert isinstance(chart, dict)
        assert "data" in chart
        assert "layout" in chart
    
    def test_caching_integration(self):
        """Test caching with chart creation"""
        from car_sales_dashboard.utils.performance import cached
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        call_count = 0
        
        @cached(ttl=60)
        def create_cached_chart(data_size):
            nonlocal call_count
            call_count += 1
            data = TestDataGenerator.generate_sales_data(data_size)
            return {"data_points": len(data), "call_count": call_count}
        
        # First call
        result1 = create_cached_chart(100)
        assert result1["data_points"] == 100
        assert call_count == 1
        
        # Second call should use cache
        result2 = create_cached_chart(100)
        assert result2["data_points"] == 100
        assert call_count == 1  # No additional calls


# Pytest configuration and fixtures
@pytest.fixture
def sample_sales_data():
    """Fixture providing sample sales data"""
    from car_sales_dashboard.utils.testing_framework import TestDataGenerator
    return TestDataGenerator.generate_sales_data(100, seed=42)


@pytest.fixture
def sample_forecast_data(sample_sales_data):
    """Fixture providing sample forecast data"""
    from car_sales_dashboard.utils.testing_framework import TestDataGenerator
    return TestDataGenerator.generate_forecast_data(sample_sales_data, 6)


# Test configuration
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Test discovery
def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their class"""
    for item in items:
        if "TestIntegration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif any(cls in item.nodeid for cls in ["TestData", "TestError", "TestPerformance", "TestChart", "TestUI"]):
            item.add_marker(pytest.mark.unit)


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
