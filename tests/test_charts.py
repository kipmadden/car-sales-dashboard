"""Unit tests for chart generation functionality."""
import pytest
import pandas as pd
from unittest.mock import patch

from car_sales_dashboard.components.charts import (
    create_sales_trend_chart,
    create_exogenous_variables_chart,
    generate_sample_data
)
from car_sales_dashboard.exceptions import ChartBuildError


class TestChartGeneration:
    """Test chart generation functionality."""
    
    def test_generate_sample_data(self):
        """Test sample data generation."""
        data = generate_sample_data(n_points=12, seed=42)
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 12
        assert not data.empty
    
    def test_generate_sample_data_reproducibility(self):
        """Test that sample data generation is reproducible."""
        data1 = generate_sample_data(n_points=24, seed=123)
        data2 = generate_sample_data(n_points=24, seed=123)
        
        pd.testing.assert_frame_equal(data1, data2)
    
    def test_create_sales_trend_chart_valid_data(self):
        """Test sales trend chart creation with valid data."""
        data = generate_sample_data(n_points=12, seed=42)
        
        chart = create_sales_trend_chart(data)
        
        assert isinstance(chart, dict)
        assert 'data' in chart
        assert 'layout' in chart
    
    def test_create_sales_trend_chart_empty_data(self):
        """Test sales trend chart creation with empty data."""
        empty_data = pd.DataFrame()
        
        with pytest.raises(ChartBuildError) as exc_info:
            create_sales_trend_chart(empty_data)
        
        assert "Sales Trend" in str(exc_info.value)
    
    def test_create_exogenous_variables_chart_valid_data(self):
        """Test exogenous variables chart creation with valid data."""
        data = generate_sample_data(n_points=12, seed=42)
        
        chart = create_exogenous_variables_chart(data)
        
        assert isinstance(chart, dict)
        assert 'data' in chart
        assert 'layout' in chart
    
    def test_create_exogenous_variables_chart_empty_data(self):
        """Test exogenous variables chart creation with empty data."""
        empty_data = pd.DataFrame()
        
        with pytest.raises(ChartBuildError) as exc_info:
            create_exogenous_variables_chart(empty_data)
        
        assert "Exogenous Variables" in str(exc_info.value)
    
    def test_chart_error_handling(self):
        """Test chart error handling with malformed data."""
        # Create data missing required columns
        bad_data = pd.DataFrame({'wrong_column': [1, 2, 3]})
        
        with pytest.raises(ChartBuildError):
            create_sales_trend_chart(bad_data)


class TestChartConfiguration:
    """Test chart configuration and settings."""
    
    def test_sample_data_columns(self):
        """Test that sample data has all required columns."""
        data = generate_sample_data(seed=42)
        
        required_columns = [
            'date', 'sales', 'unemployment', 'gas_price',
            'cpi_all', 'search_volume', 'is_forecast'
        ]
        
        for col in required_columns:
            assert col in data.columns, f"Missing column: {col}"
    
    def test_sample_data_bounds(self):
        """Test that sample data respects bounds."""
        from rxconfig import DATA_BOUNDS
        
        data = generate_sample_data(seed=42)
        
        # Check bounds for key variables
        bounds_to_test = ['sales', 'unemployment', 'gas_price', 'cpi_all', 'search_volume']
        
        for col in bounds_to_test:
            if col in data.columns:
                min_val = data[col].min()
                max_val = data[col].max()
                bounds = DATA_BOUNDS[col]
                
                assert min_val >= bounds['min'], f"{col} minimum {min_val} below bound {bounds['min']}"
                assert max_val <= bounds['max'], f"{col} maximum {max_val} above bound {bounds['max']}"
