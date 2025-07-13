#!/usr/bin/env python3
"""
Simple test for S5 remediation - Synthetic Data Reproducibility.

This test validates the S5 implementation without Reflex dependencies.
"""
import os
import sys
import pandas as pd
import numpy as np

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test imports without Reflex dependencies
try:
    from car_sales_dashboard.models.data import load_data
    print("✅ Successfully imported load_data from models.data")
except ImportError as e:
    print(f"❌ Failed to import load_data: {e}")
    sys.exit(1)

def test_data_reproducibility():
    """Test that the same seed produces identical data."""
    print("\n=== Testing Data Reproducibility ===")
    
    # Test 1: Same seed should produce identical data
    data1 = load_data(seed=42)
    data2 = load_data(seed=42)
    
    if data1.equals(data2):
        print("✅ Same seed produces identical data")
    else:
        print("❌ Same seed produces different data")
        return False
    
    # Test 2: Different seeds should produce different data
    data3 = load_data(seed=123)
    
    if not data1.equals(data3):
        print("✅ Different seeds produce different data")
    else:
        print("❌ Different seeds produce identical data")
        return False
    
    return True

def test_data_bounds():
    """Test that generated data stays within realistic bounds."""
    print("\n=== Testing Data Bounds ===")
    
    data = load_data(seed=42)
    
    # Import bounds configuration
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from rxconfig import DATA_BOUNDS
    
    bounds_tests = [
        ('sales', 'Sales'),
        ('unemployment', 'Unemployment Rate'),
        ('gas_price', 'Gas Price'),
        ('cpi_all', 'Consumer Price Index'),
        ('search_volume', 'Search Volume')
    ]
    
    all_passed = True
    
    for col, name in bounds_tests:
        if col in data.columns:
            min_val = data[col].min()
            max_val = data[col].max()
            bounds = DATA_BOUNDS[col]
            
            if min_val >= bounds['min'] and max_val <= bounds['max']:
                print(f"✅ {name}: {min_val:.2f} - {max_val:.2f} (within bounds {bounds['min']} - {bounds['max']})")
            else:
                print(f"❌ {name}: {min_val:.2f} - {max_val:.2f} (outside bounds {bounds['min']} - {bounds['max']})")
                all_passed = False
        else:
            print(f"⚠️  Column '{col}' not found in data")
    
    return all_passed

def test_seeding_consistency():
    """Test that seeding works consistently across multiple calls."""
    print("\n=== Testing Seeding Consistency ===")
    
    # Generate multiple datasets with the same seed
    datasets = [load_data(seed=999) for _ in range(3)]
    
    # Check if all datasets are identical
    all_identical = all(datasets[0].equals(ds) for ds in datasets[1:])
    
    if all_identical:
        print("✅ Multiple calls with same seed produce identical results")
        return True
    else:
        print("❌ Multiple calls with same seed produce different results")
        return False

def main():
    """Run all S5 remediation tests."""
    print("Starting S5 Remediation Tests")
    print("=" * 50)
    
    tests = [
        test_data_reproducibility,
        test_data_bounds,
        test_seeding_consistency
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All S5 remediation tests PASSED!")
        print("✅ Synthetic data reproducibility is working correctly")
        return True
    else:
        print("❌ Some tests FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
