"""
pytest Configuration File

Configures pytest for comprehensive testing of the Car Sales Dashboard.
"""

import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test configuration - conditional plugin loading
pytest_plugins = []

# Try to load optional plugins
try:
    import pytest_html
    pytest_plugins.append("pytest_html")  # HTML reporting
except ImportError:
    pass

try:
    import pytest_cov
    pytest_plugins.append("pytest_cov")   # Coverage reporting
except ImportError:
    pass

try:
    import pytest_timeout
    pytest_plugins.append("pytest_timeout")  # Timeout support
except ImportError:
    pass

try:
    import pytest_xdist
    pytest_plugins.append("pytest_xdist")  # Parallel execution
except ImportError:
    pass

# Pytest markers
def pytest_configure(config):
    """Configure pytest with custom markers and settings"""
    
    # Custom markers
    config.addinivalue_line(
        "markers", "unit: Unit tests - fast, isolated tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests - test component interaction"
    )
    config.addinivalue_line(
        "markers", "performance: Performance tests - may take longer to run"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests - long-running tests (>30s)"
    )
    config.addinivalue_line(
        "markers", "smoke: Smoke tests - basic functionality verification"
    )
    config.addinivalue_line(
        "markers", "regression: Regression tests - prevent known issues"
    )
    config.addinivalue_line(
        "markers", "load: Load tests - high resource usage tests"
    )
    
    # Set test environment
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "WARNING"  # Reduce log noise during tests


# Test discovery and collection
def pytest_collection_modifyitems(config, items):
    """Automatically categorize tests based on naming conventions"""
    
    for item in items:
        # Auto-mark based on test class names
        if "TestIntegration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "TestPerformance" in item.nodeid or "TestLoad" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        elif "TestUnit" in item.nodeid or any(cls in item.nodeid for cls in 
                                            ["TestData", "TestError", "TestValidation", "TestChart"]):
            item.add_marker(pytest.mark.unit)
        
        # Auto-mark smoke tests
        if "test_smoke" in item.name or "test_basic" in item.name:
            item.add_marker(pytest.mark.smoke)
        
        # Auto-mark slow tests
        if "test_large" in item.name or "test_stress" in item.name or "benchmark" in item.name:
            item.add_marker(pytest.mark.slow)


# Fixtures
@pytest.fixture(scope="session")
def test_config():
    """Session-wide test configuration"""
    return {
        "test_data_size": 1000,
        "performance_threshold_ms": 100,
        "memory_threshold_mb": 50,
        "temp_dir": Path("/tmp/dashboard_tests"),
        "mock_api_responses": True
    }


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(test_config):
    """Setup test environment before all tests"""
    
    # Create temporary directories
    temp_dir = test_config["temp_dir"]
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup test data directory
    test_data_dir = temp_dir / "data"
    test_data_dir.mkdir(exist_ok=True)
    
    # Setup test logs directory
    test_logs_dir = temp_dir / "logs"
    test_logs_dir.mkdir(exist_ok=True)
    
    yield
    
    # Cleanup after all tests
    import shutil
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_sales_data():
    """Generate sample sales data for testing"""
    try:
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        return TestDataGenerator.generate_sales_data(100, seed=42)
    except ImportError:
        # Fallback if testing framework not available
        import pandas as pd
        import numpy as np
        
        np.random.seed(42)
        dates = pd.date_range("2023-01-01", periods=100, freq="D")
        sales = np.random.randint(50, 200, 100)
        
        return pd.DataFrame({
            "date": dates,
            "sales_volume": sales,
            "gas_price": np.random.uniform(3.0, 5.0, 100),
            "cpi": np.random.uniform(200, 250, 100)
        })


@pytest.fixture
def mock_chart_data():
    """Mock chart data for testing"""
    return {
        "data": [
            {
                "x": ["2023-01", "2023-02", "2023-03"],
                "y": [100, 120, 110],
                "type": "scatter",
                "mode": "lines+markers",
                "name": "Sales"
            }
        ],
        "layout": {
            "title": "Mock Sales Chart",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Sales Volume"}
        }
    }


@pytest.fixture
def performance_threshold():
    """Performance testing thresholds"""
    return {
        "max_execution_time_ms": 1000,
        "max_memory_usage_mb": 100,
        "min_success_rate": 95.0
    }


# Test data cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_cache():
    """Clean up cache before and after each test"""
    try:
        from car_sales_dashboard.utils.performance import MemoryCache
        cache = MemoryCache()
        cache.clear()
        yield
        cache.clear()
    except ImportError:
        yield


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration for each test"""
    import logging
    
    # Store original level
    original_level = logging.root.level
    
    # Set test logging level
    logging.root.setLevel(logging.WARNING)
    
    yield
    
    # Restore original level
    logging.root.setLevel(original_level)


# Test reporting hooks (only if pytest-html is available)
try:
    import pytest_html
    
    def pytest_html_report_title(report):
        """Customize HTML report title"""
        report.title = "Car Sales Dashboard - Test Report"

    def pytest_html_results_summary(prefix, summary, postfix):
        """Customize HTML report summary"""
        prefix.extend([
            "<h2>Car Sales Dashboard Test Results</h2>",
            f"<p>Test execution completed at: {pytest.current_timestamp}</p>"
        ])

except ImportError:
    # pytest-html not available, skip HTML report customization
    pass


def pytest_sessionstart(session):
    """Actions to perform at start of test session"""
    import time
    pytest.current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n🧪 Starting Car Sales Dashboard test suite...")


def pytest_sessionfinish(session, exitstatus):
    """Actions to perform at end of test session"""
    if exitstatus == 0:
        print("✅ All tests passed successfully!")
    else:
        print(f"❌ Test suite finished with exit status: {exitstatus}")


# Timeout configuration (only if pytest-timeout is available)
try:
    import pytest_timeout
    
    def pytest_timeout_set_timer(item, timeout):
        """Set custom timeout for specific test types"""
        
        # Longer timeout for performance tests
        if "performance" in [mark.name for mark in item.iter_markers()]:
            return 300  # 5 minutes
        
        # Longer timeout for integration tests
        if "integration" in [mark.name for mark in item.iter_markers()]:
            return 120  # 2 minutes
        
        # Default timeout for unit tests
        return 30  # 30 seconds

except ImportError:
    # pytest-timeout not available, skip timeout configuration
    pass


# Parallel execution configuration (only if pytest-xdist is available)
try:
    import pytest_xdist
    
    def pytest_configure_node(node):
        """Configure worker nodes for parallel testing"""
        if hasattr(node, 'workerinput'):
            # Worker node configuration
            node.workerinput['test_worker_id'] = node.workerinput.get('workerinput', {}).get('workerid', 'master')

except ImportError:
    # pytest-xdist not available, skip parallel execution configuration
    pass


# Custom test outcome handling
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Customize test reporting"""
    outcome = yield
    report = outcome.get_result()
    
    # Add custom information to test reports
    if report.when == "call":
        # Add execution time to report
        if hasattr(report, 'duration'):
            if report.duration > 5.0:  # Flag slow tests
                report.longrepr_custom = f"⚠️  Long execution time: {report.duration:.2f}s"
        
        # Add memory usage if available
        if hasattr(item, '_memory_usage'):
            report.memory_usage = item._memory_usage


# Skip conditions
def pytest_runtest_setup(item):
    """Setup conditions for running tests"""
    
    # Skip performance tests in CI if not explicitly requested
    if "performance" in [mark.name for mark in item.iter_markers()]:
        if os.environ.get("CI") and not os.environ.get("RUN_PERFORMANCE_TESTS"):
            pytest.skip("Performance tests skipped in CI")
    
    # Skip load tests if insufficient resources
    if "load" in [mark.name for mark in item.iter_markers()]:
        import psutil
        if psutil.virtual_memory().available < 1024 * 1024 * 1024:  # 1GB
            pytest.skip("Insufficient memory for load tests")


# Test parametrization helpers
def pytest_generate_tests(metafunc):
    """Generate parametrized test cases"""
    
    # Parametrize data size tests
    if "data_size" in metafunc.fixturenames:
        sizes = [100, 1000] if os.environ.get("CI") else [100, 1000, 5000]
        metafunc.parametrize("data_size", sizes)
    
    # Parametrize chart types
    if "chart_type" in metafunc.fixturenames:
        chart_types = ["line", "bar", "scatter", "heatmap"]
        metafunc.parametrize("chart_type", chart_types)


# Custom assertions
def pytest_assertrepr_compare(op, left, right):
    """Custom assertion representations"""
    
    if isinstance(left, dict) and isinstance(right, dict) and op == "==":
        # Custom representation for chart data comparison
        if "data" in left and "layout" in left:
            return [
                "Chart data comparison failed:",
                f"  Left keys: {list(left.keys())}",
                f"  Right keys: {list(right.keys())}",
                f"  Data length difference: {len(left.get('data', [])) - len(right.get('data', []))}"
            ]
