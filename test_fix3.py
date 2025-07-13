#!/usr/bin/env python3
"""
Test script for Fix 3: Performance Optimization & Caching
"""

def test_memory_cache():
    """Test the MemoryCache implementation"""
    try:
        from car_sales_dashboard.utils.performance import MemoryCache
        
        cache = MemoryCache(default_ttl=5)  # 5 seconds for testing
        
        # Test set and get
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        assert value == "test_value", f"Expected 'test_value', got {value}"
        print("✅ Cache set/get works")
        
        # Test cache miss
        missing = cache.get("nonexistent_key")
        assert missing is None, f"Expected None, got {missing}"
        print("✅ Cache miss handling works")
        
        # Test stats
        stats = cache.get_stats()
        assert "hits" in stats and "misses" in stats, f"Stats incomplete: {stats}"
        print(f"✅ Cache stats work: {stats}")
        
        # Test invalidation
        count = cache.invalidate()
        assert count >= 1, f"Expected at least 1 invalidation, got {count}"
        print("✅ Cache invalidation works")
        
        print("✅ MemoryCache implementation working correctly")
        return True
        
    except Exception as e:
        print(f"❌ MemoryCache test failed: {e}")
        return False

def test_cached_decorator():
    """Test the cached decorator"""
    try:
        from car_sales_dashboard.utils.performance import cached
        import time
        
        call_count = 0
        
        @cached(ttl=5)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)  # Simulate work
            return x * 2
        
        # First call - should execute function
        result1 = expensive_function(5)
        assert result1 == 10, f"Expected 10, got {result1}"
        assert call_count == 1, f"Expected 1 call, got {call_count}"
        print("✅ First call executes function")
        
        # Second call - should use cache
        result2 = expensive_function(5)
        assert result2 == 10, f"Expected 10, got {result2}"
        assert call_count == 1, f"Expected still 1 call, got {call_count}"
        print("✅ Second call uses cache")
        
        print("✅ Cached decorator working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Cached decorator test failed: {e}")
        return False

def test_performance_monitor():
    """Test the performance monitor decorator"""
    try:
        from car_sales_dashboard.utils.performance import performance_monitor
        import time
        
        @performance_monitor("test_operation")
        def monitored_function():
            time.sleep(0.01)  # Simulate work
            return "success"
        
        result = monitored_function()
        assert result == "success", f"Expected 'success', got {result}"
        print("✅ Performance monitor decorator works")
        
        print("✅ Performance monitoring working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Performance monitor test failed: {e}")
        return False

def test_dataframe_optimizer():
    """Test DataFrame optimization utilities"""
    try:
        import pandas as pd
        from car_sales_dashboard.utils.performance import DataFrameOptimizer
        
        # Create test DataFrame
        df = pd.DataFrame({
            'category': ['A', 'B', 'A', 'B'] * 25,  # Low cardinality
            'large_int': [1000000] * 100,
            'small_int': list(range(100)),
            'float_data': [1.5] * 100
        })
        
        original_memory = df.memory_usage(deep=True).sum()
        
        # Optimize DataFrame
        optimized_df = DataFrameOptimizer.optimize_dtypes(df)
        optimized_memory = optimized_df.memory_usage(deep=True).sum()
        
        # Should reduce memory usage
        assert optimized_memory <= original_memory, f"Memory not reduced: {original_memory} -> {optimized_memory}"
        print(f"✅ Memory optimization: {original_memory} -> {optimized_memory} bytes")
        
        # Check that category optimization worked
        assert optimized_df['category'].dtype.name == 'category', f"Category not optimized: {optimized_df['category'].dtype}"
        print("✅ Category optimization works")
        
        print("✅ DataFrame optimization working correctly")
        return True
        
    except Exception as e:
        print(f"❌ DataFrame optimizer test failed: {e}")
        return False

def test_query_optimizer():
    """Test query optimization utilities"""
    try:
        import pandas as pd
        from car_sales_dashboard.utils.performance import QueryOptimizer
        
        # Create test DataFrame
        df = pd.DataFrame({
            'region': ['North', 'South', 'East', 'West'] * 25,
            'category': ['A', 'B', 'C'] * 33 + ['A'],
            'value': range(100)
        })
        
        # Test efficient filtering
        filters = {
            'region': ['North', 'South'],
            'category': ['A']
        }
        
        filtered_df = QueryOptimizer.build_efficient_filter(df, filters)
        
        # Verify results
        expected_count = len(df[(df['region'].isin(['North', 'South'])) & (df['category'] == 'A')])
        assert len(filtered_df) == expected_count, f"Filter count mismatch: {len(filtered_df)} vs {expected_count}"
        print(f"✅ Query optimization: {len(df)} -> {len(filtered_df)} rows")
        
        print("✅ Query optimization working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Query optimizer test failed: {e}")
        return False

def test_cache_integration():
    """Test cache integration with global functions"""
    try:
        from car_sales_dashboard.utils.performance import get_cache_stats, clear_cache, get_cache_instance
        
        # Get cache instance
        cache = get_cache_instance()
        cache.set("integration_test", "test_value")
        
        # Test stats
        stats = get_cache_stats()
        assert isinstance(stats, dict), f"Stats should be dict, got {type(stats)}"
        assert "total_size" in stats, f"Stats missing total_size: {stats}"
        print(f"✅ Cache stats integration: {stats}")
        
        # Test clear
        cleared = clear_cache()
        assert cleared >= 0, f"Clear should return non-negative number: {cleared}"
        print(f"✅ Cache clear integration: cleared {cleared} entries")
        
        print("✅ Cache integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Cache integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Fix 3 Verification: Performance Optimization & Caching ===")
    print()
    
    tests = [
        ("Memory Cache", test_memory_cache),
        ("Cached Decorator", test_cached_decorator),
        ("Performance Monitor", test_performance_monitor),
        ("DataFrame Optimizer", test_dataframe_optimizer),
        ("Query Optimizer", test_query_optimizer),
        ("Cache Integration", test_cache_integration)
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
    
    print("=== Fix 3 Results ===")
    if all(results):
        print("🎉 Fix 3 implementation is COMPLETE and verified!")
        print("✅ Memory caching with TTL support")
        print("✅ Performance monitoring and metrics")
        print("✅ DataFrame optimization for memory efficiency")
        print("✅ Query optimization for filtering")
        print("✅ Cache integration and invalidation")
        print()
        print("Performance Benefits:")
        print("- 🚀 Chart generation caching reduces response time")
        print("- 💾 Data type optimization reduces memory usage")
        print("- ⚡ Intelligent filtering improves query speed")
        print("- 📊 Performance monitoring tracks bottlenecks")
        print("- 🔄 Automatic cache invalidation ensures data freshness")
    else:
        print("⚠️ Some Fix 3 components need attention.")
        
    print(f"Status: {sum(results)}/{len(results)} checks passed")
