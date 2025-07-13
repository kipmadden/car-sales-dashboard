"""
Test Fix 4: Data Validation & Input Sanitization
Comprehensive testing of validation and sanitization features.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import tempfile
from car_sales_dashboard.utils.validation import (
    InputSanitizer, DataValidator, FileValidator,
    sanitize_chart_config, sanitize_output
)
from car_sales_dashboard.exceptions import DataValidationError

def test_input_sanitizer():
    """Test input sanitization functionality"""
    print("\n=== Testing Input Sanitizer ===")
    
    # Test string sanitization
    sanitizer = InputSanitizer()
    
    # Basic string sanitization
    dirty_string = "<script>alert('xss')</script>Hello World"
    clean_string = sanitizer.sanitize_string(dirty_string)
    assert "<script>" not in clean_string
    assert "Hello World" in clean_string
    print("✅ String sanitization removes dangerous characters")
    
    # Length limiting
    long_string = "A" * 300
    limited_string = sanitizer.sanitize_string(long_string, max_length=100)
    assert len(limited_string) == 100
    print("✅ String length limiting works")
    
    # Numeric sanitization with bounds
    clean_num = sanitizer.sanitize_numeric("2.5", min_val=0.1, max_val=3.0)
    assert clean_num == 2.5
    print("✅ Numeric sanitization preserves valid values")
    
    # Numeric bounds enforcement
    bounded_num = sanitizer.sanitize_numeric("5.0", min_val=0.1, max_val=3.0)
    assert bounded_num == 3.0
    print("✅ Numeric bounds enforcement works")
    
    # Invalid numeric handling
    try:
        sanitizer.sanitize_numeric("invalid")
        assert False, "Should have raised exception"
    except DataValidationError:
        print("✅ Invalid numeric input properly rejected")
    
    return True

def test_data_validator():
    """Test data validation functionality"""
    print("\n=== Testing Data Validator ===")
    
    # Create test DataFrame
    test_data = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=20, freq='ME'),
        'sales_volume': range(100, 120),
        'gas_price': [3.5 + i*0.1 for i in range(20)],
        'cpi': [200 + i*5 for i in range(20)],
        'search_volume': [50 + i*2 for i in range(20)]
    })
    
    # Test valid DataFrame
    is_valid, errors = DataValidator.validate_dataframe(test_data, 'sales_data')
    assert is_valid
    assert len(errors) == 0
    print("✅ Valid DataFrame passes validation")
    
    # Test missing columns
    invalid_data = test_data.drop('gas_price', axis=1)
    is_valid, errors = DataValidator.validate_dataframe(invalid_data, 'sales_data')
    assert not is_valid
    assert any("gas_price" in error for error in errors)
    print("✅ Missing columns properly detected")
    
    # Test modifier validation
    is_valid, errors = DataValidator.validate_modifiers(1.5, 2.0, 0.8)
    assert is_valid
    print("✅ Valid modifiers pass validation")
    
    # Test invalid modifiers
    is_valid, errors = DataValidator.validate_modifiers(5.0, 2.0, 0.8)
    assert not is_valid
    assert any("gas_price" in error.lower() or "gas" in error.lower() for error in errors)
    print("✅ Invalid modifiers properly rejected")
    
    # Test date range validation
    is_valid, errors = DataValidator.validate_date_range("2020-01-01", "2020-12-31")
    assert is_valid
    print("✅ Valid date range passes validation")
    
    # Test invalid date range
    is_valid, errors = DataValidator.validate_date_range("2020-12-31", "2020-01-01")
    assert not is_valid
    print("✅ Invalid date range properly rejected")
    
    return True

def test_file_validator():
    """Test file validation functionality"""
    print("\n=== Testing File Validator ===")
    
    # Test file extension validation
    is_valid, errors = FileValidator.validate_file_upload("test.csv", 1000)
    assert is_valid
    print("✅ Valid CSV file extension accepted")
    
    # Test invalid extension
    is_valid, errors = FileValidator.validate_file_upload("test.exe", 1000)
    assert not is_valid
    assert any("not allowed" in error for error in errors)
    print("✅ Invalid file extension rejected")
    
    # Test file size validation
    large_size = 100 * 1024 * 1024  # 100MB
    is_valid, errors = FileValidator.validate_file_upload("test.csv", large_size)
    assert not is_valid
    assert any("too large" in error for error in errors)
    print("✅ Oversized files rejected")
    
    # Test CSV content validation with temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        # Write valid CSV
        f.write("date,sales_volume,gas_price,cpi,search_volume\n")
        f.write("2020-01-01,100,3.5,200,50\n")
        f.write("2020-02-01,105,3.6,205,55\n")
        for i in range(8):  # Add more rows to meet minimum requirement
            f.write(f"2020-{3+i:02d}-01,{110+i},{3.7+i*0.1},{210+i*5},{60+i*5}\n")
        temp_file = f.name
    
    try:
        is_valid, errors, df = FileValidator.validate_csv_content(temp_file)
        assert is_valid
        assert df is not None
        assert len(df) >= 10
        print("✅ Valid CSV content accepted")
    finally:
        # Clean up with proper error handling
        try:
            os.unlink(temp_file)
        except (OSError, PermissionError):
            pass  # File cleanup failed, but test still passed
    
    return True

def test_chart_sanitization():
    """Test chart configuration sanitization"""
    print("\n=== Testing Chart Sanitization ===")
    
    # Test chart config sanitization
    dirty_config = {
        'title': '<script>alert("xss")</script>Sales Chart',
        'x_label': 'Date',
        'y_label': 'Sales<>',
        'width': 5000,  # Too large
        'height': 100   # Too small
    }
    
    clean_config = sanitize_chart_config(dirty_config)
    assert '<script>' not in clean_config['title']
    assert clean_config['width'] <= 2000
    assert clean_config['height'] >= 200
    print("✅ Chart configuration properly sanitized")
    
    # Test output sanitization
    dirty_data = {
        'values': [1, 2, float('inf'), 3],
        'labels': ['<script>bad</script>', 'good'],
        'nested': {
            'dangerous': '<iframe>evil</iframe>',
            'normal': 'safe'
        }
    }
    
    clean_data = sanitize_output(dirty_data)
    assert clean_data['values'][2] is None  # inf converted to None
    # Check that dangerous content is removed
    clean_str = str(clean_data)
    assert '<script>' not in clean_str
    assert '<iframe>' not in clean_str
    print("✅ Output data properly sanitized")
    
    return True

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\n=== Testing Edge Cases ===")
    
    # Test empty DataFrame validation
    empty_df = pd.DataFrame()
    is_valid, errors = DataValidator.validate_dataframe(empty_df)
    assert not is_valid
    assert any("empty" in error for error in errors)
    print("✅ Empty DataFrame properly rejected")
    
    # Test None input sanitization
    clean_none = sanitize_output(None)
    assert clean_none is None
    print("✅ None input handled safely")
    
    # Test numeric sanitization with NaN
    try:
        InputSanitizer.sanitize_numeric(float('nan'))
        assert False, "Should have raised exception"
    except DataValidationError:
        print("✅ NaN input properly rejected")
    
    # Test string sanitization with None
    clean_none_str = InputSanitizer.sanitize_string(None)
    assert clean_none_str == "None"
    print("✅ None string input handled safely")
    
    return True

def main():
    """Run all Fix 4 tests"""
    print("🔧 Testing Fix 4: Data Validation & Input Sanitization")
    print("=" * 60)
    
    tests = [
        ("Input Sanitizer", test_input_sanitizer),
        ("Data Validator", test_data_validator),
        ("File Validator", test_file_validator),
        ("Chart Sanitization", test_chart_sanitization),
        ("Edge Cases", test_edge_cases)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            if success:
                print(f"\n✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"🎯 Fix 4 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Fix 4: Data Validation & Input Sanitization - COMPLETE!")
        print("\n📋 Implemented Features:")
        print("  • Comprehensive input sanitization (strings, numbers)")
        print("  • DataFrame structure and content validation")
        print("  • File upload security validation")
        print("  • Chart configuration sanitization")
        print("  • Output data sanitization")
        print("  • Date range validation")
        print("  • Modifier bounds validation")
        print("  • Edge case handling")
        return True
    else:
        print("⚠️  Some tests failed. Fix 4 needs attention.")
        return False

if __name__ == "__main__":
    main()
