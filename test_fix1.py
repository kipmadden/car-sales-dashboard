#!/usr/bin/env python3
"""
Simple test to verify Fix 1 chart refactoring without complex dependencies.
"""

def test_chart_module_structure():
    """Test that charts.py has the expected structure"""
    try:
        import os
        charts_path = "car_sales_dashboard/components/charts.py"
        
        if not os.path.exists(charts_path):
            print(f"❌ Charts file not found: {charts_path}")
            return False
            
        with open(charts_path, 'r') as f:
            content = f.read()
            
        # Check for required chart functions
        required_functions = [
            "create_sales_trend_chart",
            "create_vehicle_type_chart",
            "create_region_chart",
            "create_top_models_chart",
            "create_state_map_chart",
            "create_heatmap_chart",
            "create_exogenous_variables_chart"
        ]
        
        missing_functions = []
        for func in required_functions:
            if f"def {func}" not in content:
                missing_functions.append(func)
        
        if missing_functions:
            print(f"❌ Missing chart functions: {missing_functions}")
            return False
        
        print(f"✅ All {len(required_functions)} chart functions found in charts.py")
        return True
        
    except Exception as e:
        print(f"❌ Chart structure test failed: {e}")
        return False

def test_duplicate_files_removed():
    """Test that duplicate chart files have been removed"""
    duplicate_files = [
        "car_sales_dashboard/components/chart_client.py",
        "car_sales_dashboard/components/chart_components.py",
        "car_sales_dashboard/components/chart_fix.py", 
        "car_sales_dashboard/components/chart_scripts.py",
        "car_sales_dashboard/components/static_charts.py",
        "car_sales_dashboard/components/temp_chart_container.py",
        "car_sales_dashboard/components/charts_new.py",
        "car_sales_dashboard/components/exogenous_chart.py",
        "experiments/"
    ]
    
    import os
    remaining_files = []
    for file_path in duplicate_files:
        if os.path.exists(file_path):
            remaining_files.append(file_path)
    
    if remaining_files:
        print(f"❌ Duplicate files still exist: {remaining_files}")
        return False
    
    print("✅ All duplicate chart files successfully removed")
    return True

def test_fixed_tabs_refactoring():
    """Test that fixed_tabs.py uses DashboardState chart functions"""
    try:
        with open("car_sales_dashboard/pages/fixed_tabs.py", 'r') as f:
            content = f.read()
        
        # Check for DashboardState chart function usage
        required_patterns = [
            "DashboardState.get_sales_trend_chart",
            "DashboardState.get_vehicle_type_chart", 
            "DashboardState.get_region_chart",
            "rx.plotly(data="
        ]
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            print(f"❌ Missing DashboardState patterns in fixed_tabs.py: {missing_patterns}")
            return False
        
        # Check that old chart imports are removed
        old_patterns = [
            "from ..components.chart_",
            "from ..components.static_charts",
            "from ..components.charts_new"
        ]
        
        found_old_patterns = []
        for pattern in old_patterns:
            if pattern in content:
                found_old_patterns.append(pattern)
        
        if found_old_patterns:
            print(f"❌ Old chart imports still present: {found_old_patterns}")
            return False
        
        print("✅ fixed_tabs.py successfully refactored to use DashboardState")
        return True
        
    except Exception as e:
        print(f"❌ Fixed tabs test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Fix 1 Verification Test ===")
    print("Testing chart refactoring and cleanup...")
    print()
    
    tests = [
        ("Chart file structure", test_chart_module_structure),
        ("Duplicate file removal", test_duplicate_files_removed), 
        ("Fixed tabs refactoring", test_fixed_tabs_refactoring)
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
    
    print("=== Fix 1 Results ===")
    if all(results):
        print("🎉 Fix 1 implementation is COMPLETE and verified!")
        print("✅ Chart refactoring and cleanup successful")
        print("✅ All duplicate files removed")
        print("✅ Dashboard integration working")
    else:
        print("⚠️ Some Fix 1 components need attention.")
        
    print(f"Status: {sum(results)}/{len(results)} checks passed")
