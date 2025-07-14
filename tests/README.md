# Testing Configuration and Documentation

## Overview

This directory contains comprehensive testing infrastructure for the Car Sales Dashboard project. The testing framework is designed to ensure code quality, performance, and reliability across all dashboard components.

## Test Structure

### Test Categories

- **Unit Tests** (`test_dashboard_components.py`): Fast, isolated tests for individual components
- **Integration Tests**: Tests for component interaction and data flow
- **Performance Tests**: Benchmarking and load testing utilities
- **End-to-End Tests**: Complete user workflow validation

### Test Framework Components

1. **Testing Framework** (`car_sales_dashboard/utils/testing_framework.py`)
   - `TestDataGenerator`: Realistic test data creation
   - `PerformanceProfiler`: Execution timing and memory profiling
   - `CodeQualityChecker`: Static code analysis
   - `TestRunner`: Comprehensive test execution orchestration

2. **Performance Testing** (`car_sales_dashboard/utils/performance_testing.py`)
   - `LoadTestRunner`: Concurrent user simulation
   - `BenchmarkSuite`: Component performance benchmarking
   - Memory and CPU profiling tools

3. **Pytest Configuration** (`conftest.py`)
   - Custom fixtures and markers
   - Test environment setup
   - Parallel execution configuration

## Running Tests

### Quick Start

```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest -m unit
python -m pytest -m integration
python -m pytest -m performance

# Run with coverage
python -m pytest --cov=car_sales_dashboard --cov-report=html

# Run with HTML report
python -m pytest --html=reports/test_report.html --self-contained-html
```

### Advanced Test Execution

```bash
# Run comprehensive test suite with framework
python car_sales_dashboard/utils/testing_framework.py --test-type all --output test_results.md

# Run performance benchmarks
python car_sales_dashboard/utils/performance_testing.py --test-type benchmark --output benchmark_results.json

# Run load tests
python car_sales_dashboard/utils/performance_testing.py --test-type load --users 20 --duration 120
```

### Test Markers

- `@pytest.mark.unit`: Fast unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.performance`: Performance benchmarks
- `@pytest.mark.slow`: Long-running tests
- `@pytest.mark.smoke`: Basic functionality tests
- `@pytest.mark.regression`: Regression prevention tests
- `@pytest.mark.load`: High resource usage tests

## Test Configuration

### Environment Variables

- `TESTING=true`: Enables test mode
- `LOG_LEVEL=WARNING`: Reduces log noise during testing
- `RUN_PERFORMANCE_TESTS=true`: Enables performance tests in CI
- `CI=true`: Adjusts test behavior for CI environment

### Configuration Files

- `conftest.py`: Pytest configuration and fixtures
- `pytest.ini`: Pytest settings and options
- `pyproject.toml`: Project testing configuration

## Performance Testing

### Benchmarking

The benchmark suite measures:
- Data operation performance (generation, filtering, aggregation)
- Chart creation performance with various data sizes
- Validation operation performance
- Memory usage patterns

### Load Testing

Load tests simulate:
- Concurrent user sessions
- Dashboard data loading under load
- Chart generation performance under stress
- Memory and CPU usage under load

### Performance Thresholds

Default performance thresholds:
- Response time: < 1000ms
- Memory usage: < 50MB per operation
- Success rate: > 95%
- Error rate: < 5%

## Code Quality

### Quality Metrics

The testing framework checks:
- Code complexity (cyclomatic complexity)
- Function and class length
- Comment ratio
- Import dependencies
- Error handling coverage

### Quality Standards

- Maximum line length: 100 characters
- Maximum function length: 50 lines
- Maximum class length: 200 lines
- Minimum test coverage: 80%
- Maximum cognitive complexity: 15

## Test Data

### Data Generation

Test data is generated to simulate realistic scenarios:
- Time series sales data with trends and seasonality
- Exogenous variables (gas prices, CPI, search volume)
- Multiple vehicle types, regions, and models
- Forecast data with confidence intervals

### Data Validation

All test data undergoes validation:
- Schema compliance checking
- Data type validation
- Range and constraint validation
- Consistency checks

## Continuous Integration

### CI Pipeline Tests

The CI pipeline runs:
1. Unit tests (fast feedback)
2. Integration tests
3. Code quality analysis
4. Coverage reporting
5. Performance regression tests (optional)

### Test Reports

Generated reports include:
- HTML test results with details
- Coverage reports with line-by-line analysis
- Performance benchmark results
- Code quality metrics

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **SSL/Network Issues**: Tests avoid external network calls
3. **Memory Issues**: Adjust test data sizes for resource-constrained environments
4. **Timeout Issues**: Use appropriate test markers for slow tests

### Debug Mode

```bash
# Run tests with verbose output
python -m pytest -v -s

# Run specific test with debugging
python -m pytest tests/test_dashboard_components.py::TestDataGeneration::test_sales_data_generation -v -s

# Run with pdb debugger
python -m pytest --pdb
```

## Best Practices

### Writing Tests

1. **Isolation**: Each test should be independent
2. **Clarity**: Test names should clearly describe what is being tested
3. **Coverage**: Aim for high test coverage of critical paths
4. **Performance**: Keep unit tests fast (< 1 second)
5. **Reliability**: Tests should be deterministic and repeatable

### Test Organization

1. **Grouping**: Organize tests by component or functionality
2. **Fixtures**: Use fixtures for common test setup
3. **Parametrization**: Use parametrized tests for multiple scenarios
4. **Markers**: Apply appropriate markers for test categorization

### Maintenance

1. **Regular Updates**: Keep tests updated with code changes
2. **Refactoring**: Refactor tests when code structure changes
3. **Performance**: Monitor test execution times
4. **Dependencies**: Keep test dependencies minimal and current

## Integration with Development

### Pre-commit Hooks

Tests can be integrated with pre-commit hooks:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest
        language: system
        args: ["-m", "not slow"]
        pass_filenames: false
        always_run: true
```

### IDE Integration

Most IDEs support pytest integration:
- VS Code: Python Test Explorer
- PyCharm: Built-in pytest runner
- Vim/Neovim: pytest plugins

### Development Workflow

Recommended testing workflow:
1. Write failing test (TDD approach)
2. Implement minimal code to pass test
3. Refactor while keeping tests green
4. Run full test suite before committing
5. Use performance tests for optimization

## Future Enhancements

Planned testing improvements:
- Visual regression testing for charts
- API contract testing
- Database integration testing
- Browser automation testing
- Property-based testing with Hypothesis
