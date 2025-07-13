"""Unit tests for the data module."""
import pytest
import pandas as pd
import numpy as np

from car_sales_dashboard.models.data import load_data


class TestDataLoading:
    """Test data loading functionality."""
    
    def test_load_data_basic(self):
        """Test basic data loading functionality."""
        data = load_data(seed=42)
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert len(data) > 0
    
    def test_load_data_reproducibility(self):
        """Test that same seed produces identical data."""
        data1 = load_data(seed=123)
        data2 = load_data(seed=123)
        
        pd.testing.assert_frame_equal(data1, data2)
    
    def test_load_data_different_seeds(self):
        """Test that different seeds produce different data."""
        data1 = load_data(seed=42)
        data2 = load_data(seed=999)
        
        # Data should have same structure
        assert data1.shape == data2.shape
        assert list(data1.columns) == list(data2.columns)
        
        # But different values
        assert not data1.equals(data2)
    
    def test_data_columns(self):
        """Test that data contains expected columns."""
        data = load_data(seed=42)
        
        expected_columns = [
            'sales', 'unemployment', 'gas_price', 
            'cpi_all', 'search_volume', 'is_forecast'
        ]
        
        for col in expected_columns:
            assert col in data.columns, f"Missing column: {col}"
    
    def test_data_bounds(self):
        """Test that data stays within realistic bounds."""
        from rxconfig import DATA_BOUNDS
        
        data = load_data(seed=42)
        
        # Test sales bounds
        assert data['sales'].min() >= DATA_BOUNDS['sales']['min']
        assert data['sales'].max() <= DATA_BOUNDS['sales']['max']
        
        # Test unemployment bounds
        assert data['unemployment'].min() >= DATA_BOUNDS['unemployment']['min']
        assert data['unemployment'].max() <= DATA_BOUNDS['unemployment']['max']
        
        # Test gas price bounds
        assert data['gas_price'].min() >= DATA_BOUNDS['gas_price']['min']
        assert data['gas_price'].max() <= DATA_BOUNDS['gas_price']['max']
    
    def test_forecast_flag(self):
        """Test that forecast flag works correctly."""
        data = load_data(seed=42)
        
        assert 'is_forecast' in data.columns
        assert data['is_forecast'].dtype == bool
        
        # load_data should return only historical data (no forecast data)
        assert not data['is_forecast'].any()  # No forecast data
        assert not data['is_forecast'].all()  # All data is historical
    
    def test_data_types(self):
        """Test that data has correct types."""
        data = load_data(seed=42)
        
        # Numeric columns should be numeric
        numeric_cols = ['sales', 'unemployment', 'gas_price', 'cpi_all', 'search_volume']
        for col in numeric_cols:
            assert pd.api.types.is_numeric_dtype(data[col]), f"{col} should be numeric"
        
        # Boolean column should be boolean
        assert data['is_forecast'].dtype == bool
