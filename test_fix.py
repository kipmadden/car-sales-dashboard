#!/usr/bin/env python3
"""
Minimal test script to verify the data fixes without running full pytest
"""
import pandas as pd
import sys
import os

def test_data_structure():
    """Test the data structure directly from CSV"""
    csv_path = 'car_sales_dashboard/data/synthetic_car_sales_seed_42.csv'
    
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found at {csv_path}")
        return False
    
    try:
        data = pd.read_csv(csv_path, parse_dates=['date'])
        print(f"✓ Data loaded successfully: {data.shape}")
        
        # Test columns
        expected_columns = [
            'sales', 'unemployment', 'gas_price', 
            'cpi_all', 'search_volume', 'is_forecast'
        ]
        
        missing_cols = [col for col in expected_columns if col not in data.columns]
        if missing_cols:
            print(f"✗ Missing columns: {missing_cols}")
            return False
        else:
            print(f"✓ All expected columns present")
        
        # Test is_forecast column
        if 'is_forecast' not in data.columns:
            print("✗ is_forecast column missing")
            return False
        
        if data['is_forecast'].dtype != bool:
            print(f"✗ is_forecast column should be bool, got {data['is_forecast'].dtype}")
            return False
        
        print(f"✓ is_forecast column is boolean")
        
        # Test forecast flag values (should be all False for historical data)
        if data['is_forecast'].any():
            print("✗ Expected all is_forecast to be False (historical data only)")
            return False
        
        print(f"✓ All data is historical (is_forecast=False)")
        
        # Test data types
        numeric_cols = ['sales', 'unemployment', 'gas_price', 'cpi_all', 'search_volume']
        for col in numeric_cols:
            if not pd.api.types.is_numeric_dtype(data[col]):
                print(f"✗ {col} should be numeric, got {data[col].dtype}")
                return False
        
        print(f"✓ All numeric columns have correct types")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_data_structure()
    sys.exit(0 if success else 1)
