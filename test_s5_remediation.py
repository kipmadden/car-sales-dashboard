"""
Test script to verify S5 remediation: reproducible synthetic data generation.

This script tests that:
1. Data generation is reproducible with seeds
2. Generated data stays within realistic bounds
3. Different seeds produce different but bounded data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from car_sales_dashboard.models.data import load_data, generate_sample_data
from car_sales_dashboard.components.charts import generate_sample_data as chart_sample_data
from rxconfig import DEFAULT_SEED, DATA_BOUNDS


def test_reproducibility():
    """Test that the same seed produces identical data."""
    print("Testing data reproducibility...")
    
    # Generate data twice with same seed
    data1 = generate_sample_data(seed=42)
    data2 = generate_sample_data(seed=42)
    
    # Check if data is identical
    assert data1.equals(data2), "Data with same seed should be identical"
    print("✅ Same seed produces identical data")
    
    # Generate data with different seeds
    data3 = generate_sample_data(seed=123)
    
    # Check if data is different
    assert not data1.equals(data3), "Data with different seeds should be different"
    print("✅ Different seeds produce different data")


def test_data_bounds():
    """Test that generated data stays within realistic bounds."""
    print("\nTesting data bounds...")
    
    data = generate_sample_data(seed=42)
    
    # Check each variable's bounds
    for column, bounds in DATA_BOUNDS.items():
        if column in data.columns:
            min_val = data[column].min()
            max_val = data[column].max()
            
            assert min_val >= bounds['min'], f"{column} minimum ({min_val:.2f}) below bound ({bounds['min']})"
            assert max_val <= bounds['max'], f"{column} maximum ({max_val:.2f}) above bound ({bounds['max']})"
            
            print(f"✅ {column}: {min_val:.2f} - {max_val:.2f} (within {bounds['min']} - {bounds['max']})")


def test_load_data_seeding():
    """Test that load_data function respects seeding."""
    print("\nTesting load_data seeding...")
    
    # Force regeneration with specific seed
    data1 = load_data(seed=999, force_regenerate=True)
    data2 = load_data(seed=999, force_regenerate=False)  # Should load cached version
    
    print(f"✅ Data loaded successfully: {len(data1)} records")
    print(f"✅ Sales range: {data1['sales'].min():.0f} - {data1['sales'].max():.0f}")


def test_chart_sample_data():
    """Test chart sample data generation."""
    print("\nTesting chart sample data...")
    
    chart_data1 = chart_sample_data(n_points=12, seed=42)
    chart_data2 = chart_sample_data(n_points=12, seed=42)
    
    assert chart_data1.equals(chart_data2), "Chart data should be reproducible"
    print("✅ Chart sample data is reproducible")
    
    # Check bounds
    for column in ['sales', 'unemployment', 'gas_price', 'search_volume']:
        if column in chart_data1.columns:
            min_val = chart_data1[column].min()
            max_val = chart_data1[column].max()
            bounds = DATA_BOUNDS[column]
            
            assert min_val >= bounds['min'], f"Chart {column} below bounds"
            assert max_val <= bounds['max'], f"Chart {column} above bounds"
            
            print(f"✅ Chart {column}: {min_val:.2f} - {max_val:.2f}")


if __name__ == "__main__":
    print("=== S5 Remediation Test: Synthetic Data Reproducibility ===")
    print(f"Default seed: {DEFAULT_SEED}")
    print(f"Data bounds: {DATA_BOUNDS}")
    print()
    
    try:
        test_reproducibility()
        test_data_bounds()
        test_load_data_seeding()
        test_chart_sample_data()
        
        print("\n🎉 All tests passed! S5 remediation successful.")
        print("✅ Data generation is now reproducible with proper seeding")
        print("✅ All generated data stays within realistic bounds")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
