# Testing Configuration and Documentation

## Overview

This directory contains unit tests for the Car Sales Dashboard project using pytest. The tests ensure code quality and reliability across data loading and chart generation components.

## Test Structure

### Test Files

- **`test_data.py`**: Unit tests for data loading and validation
- **`test_charts.py`**: Unit tests for chart generation functionality

### Test Configuration

- **Pytest Configuration** (`conftest.py`): Custom fixtures and markers
- **Pytest Settings** (`pytest.ini`): Test execution configuration

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_data.py

# Run with coverage report
pytest --cov=car_sales_dashboard --cov-report=html

# Run specific test category
pytest -m unit
pytest -m integration
pytest -m smoke
```

### Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit`: Fast unit tests
- `@pytest.mark.integration`: Integration tests  
- `@pytest.mark.performance`: Performance benchmarks
- `@pytest.mark.smoke`: Basic functionality tests

## Test Coverage

### Data Module Tests

**test_data.py** covers:
- Data loading functionality
- Data reproducibility with seeds
- Data validation (types, bounds, columns)
- Data consistency checks

### Chart Module Tests

**test_charts.py** covers:
- Chart generation with valid data
- Error handling for invalid data
- Sample data generation
- Chart configuration and bounds

## Best Practices

### Writing Tests

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Descriptive Names**: Use clear test names that describe what is being tested
3. **Arrange-Act-Assert**: Follow the AAA pattern for test structure
4. **Use Fixtures**: Leverage pytest fixtures for common test setup
5. **Mock External Dependencies**: Avoid network calls and external dependencies

### Running Tests Locally

Before committing code:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=car_sales_dashboard

# Check for errors
pytest --tb=short
```

## Continuous Integration

The CI pipeline runs all tests automatically on push and pull requests, ensuring code quality and preventing regressions.
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
