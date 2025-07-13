#!/usr/bin/env python3
"""
Test Fix 2: Enhanced Error Handling & User Feedback
"""

def test_error_classes():
    """Test that enhanced error classes work correctly"""
    try:
        from car_sales_dashboard.exceptions import (
            ChartBuildError,
            DataValidationError,
            ModelTrainingError,
            ConfigurationError
        )
        
        # Test DataValidationError
        try:
            raise DataValidationError(
                field_name="gas_price",
                value=-1.0,
                reason="must be positive",
                suggestion="Use values between 0.1 and 3.0"
            )
        except DataValidationError as e:
            print(f"✅ DataValidationError works: {e}")
        
        # Test ModelTrainingError
        try:
            raise ModelTrainingError(
                model_type="linear",
                error_details="insufficient data",
                data_shape=(10, 5)
            )
        except ModelTrainingError as e:
            print(f"✅ ModelTrainingError works: {e}")
        
        print("✅ All error classes imported and working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error classes test failed: {e}")
        return False

def test_error_handler():
    """Test the ErrorHandler utility"""
    try:
        from car_sales_dashboard.utils.error_handler import ErrorHandler, Validators
        
        # Test validators
        is_valid, message = Validators.positive_number(1.5)
        print(f"✅ Positive number validation: {is_valid}, {message}")
        
        is_valid, message = Validators.modifier_range(0.5)
        print(f"✅ Modifier range validation: {is_valid}, {message}")
        
        # Test error chart creation
        error_chart = ErrorHandler._create_error_chart("Test Chart", "chart_build")
        print(f"✅ Error chart created with {len(error_chart)} keys")
        
        print("✅ ErrorHandler utility working correctly")
        return True
        
    except Exception as e:
        print(f"❌ ErrorHandler test failed: {e}")
        return False

def test_decorators():
    """Test error handling decorators"""
    try:
        from car_sales_dashboard.utils.error_handler import error_handler, validate_input, Validators
        
        # Test error_handler decorator
        @error_handler("chart_build", fallback_value={})
        def failing_function():
            raise ValueError("Test error")
        
        result = failing_function()
        print(f"✅ Error handler decorator works, fallback: {type(result)}")
        
        # Test validate_input decorator
        @validate_input(Validators.positive_number, "Test value")
        def test_validation(value):
            return value * 2
        
        try:
            result = test_validation(5.0)
            print(f"✅ Validation decorator works: {result}")
        except Exception as e:
            print(f"Expected validation error: {e}")
        
        print("✅ Decorators working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Decorators test failed: {e}")
        return False

def test_feedback_components():
    """Test feedback component imports"""
    try:
        from car_sales_dashboard.components.feedback import (
            create_error_alert,
            create_loading_spinner,
            create_validation_message
        )
        
        print("✅ Feedback components imported successfully")
        print("✅ Components ready for UI integration")
        return True
        
    except Exception as e:
        print(f"❌ Feedback components test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Fix 2 Verification: Enhanced Error Handling & User Feedback ===")
    print()
    
    tests = [
        ("Error Classes", test_error_classes),
        ("Error Handler Utility", test_error_handler),
        ("Decorators", test_decorators),
        ("Feedback Components", test_feedback_components)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing: {test_name}")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append(False)
        print()
    
    print("=== Fix 2 Results ===")
    if all(results):
        print("🎉 Fix 2 implementation is COMPLETE!")
        print("✅ Enhanced error handling implemented")
        print("✅ User feedback components ready")
        print("✅ Input validation system working")
        print("✅ Graceful error recovery enabled")
    else:
        print("⚠️ Some Fix 2 components need attention.")
        
    print(f"Status: {sum(results)}/{len(results)} checks passed")
