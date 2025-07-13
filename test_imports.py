#!/usr/bin/env python3
"""
Test script to verify import functionality without triggering SSL issues.
This script tests the chart components without importing the full state module.
"""

def test_chart_imports():
    """Test that chart components can be imported safely"""
    try:
        print("Testing chart imports...")
        from car_sales_dashboard.components.charts import (
            create_sales_trend_chart,
            create_vehicle_type_chart,
            create_region_chart,
            create_top_models_chart,
            create_state_map_chart,
            create_heatmap_chart,
            create_exogenous_variables_chart
        )
        print("✅ Chart imports successful!")
        return True
    except Exception as e:
        print(f"❌ Chart import failed: {e}")
        return False

def test_data_loading():
    """Test that data loading works"""
    try:
        print("Testing data loading...")
        from car_sales_dashboard.models import load_data
        from rxconfig import DEFAULT_SEED
        df = load_data(seed=DEFAULT_SEED)
        print(f"✅ Data loading successful! Shape: {df.shape}")
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_chart_creation():
    """Test creating a simple chart without Reflex state"""
    try:
        print("Testing chart creation...")
        from car_sales_dashboard.components.charts import create_sales_trend_chart
        from car_sales_dashboard.models import load_data
        from rxconfig import DEFAULT_SEED
        
        # Load sample data
        df = load_data(seed=DEFAULT_SEED)
        
        # Create a simple forecast-like DataFrame
        import pandas as pd
        forecast_data = df.head(10).copy()
        forecast_data['prediction'] = forecast_data['sales'] * 1.1
        forecast_data['date'] = pd.date_range('2024-01-01', periods=10, freq='M')
        
        # Test chart creation
        chart_dict = create_sales_trend_chart(forecast_data)
        print(f"✅ Chart creation successful! Chart has {len(chart_dict)} keys")
        return True
    except Exception as e:
        print(f"❌ Chart creation failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Car Sales Dashboard Import Test ===")
    
    tests = [
        test_data_loading,
        test_chart_imports,
        test_chart_creation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
        print()
    
    print("=== Test Summary ===")
    if all(results):
        print("🎉 All tests passed! Fix 1 implementation is working correctly.")
    else:
        print("⚠️ Some tests failed. See details above.")
        
    print(f"Results: {sum(results)}/{len(results)} tests passed")
