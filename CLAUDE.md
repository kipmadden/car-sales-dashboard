# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive ML dashboard for car sales forecasting built with Reflex (Python full-stack framework) and SARIMAX time series models. The application allows real-time manipulation of exogenous variables to see their impact on sales forecasts.

## Essential Commands

### Development
```bash
# Start development server
reflex run

# Windows development with SSL fixes
run_reflex.bat

# Unix/Linux development
./run_reflex.sh
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=car_sales_dashboard --cov-report=html

# Run specific test categories
pytest -m unit        # Unit tests only
pytest -m integration # Integration tests
pytest -m performance # Performance tests
pytest -m smoke      # Quick smoke tests
```

### Building & Deployment
```bash
# Docker build and run
docker-compose up --build

# Production deployment
./deploy.sh

# Compile requirements (when updating dependencies)
./scripts/compile-requirements.sh
```

### Code Quality
```bash
# Format code
black car_sales_dashboard/
isort car_sales_dashboard/

# Type checking
mypy car_sales_dashboard/

# Linting
flake8 car_sales_dashboard/
```

## Architecture & Key Patterns

### Application Structure
The app follows a modular architecture with clear separation of concerns:

- **State Management**: Centralized in `car_sales_dashboard/state.py` using Reflex's reactive state system. All UI updates flow through state mutations.

- **Component Organization**: 
  - `components/charts.py`: Plotly-based interactive charts that respond to state changes
  - `components/controls.py`: User input controls (sliders, dropdowns) that modify exogenous variables
  - `components/tables.py`: Data tables with filtering and sorting
  - `components/exogenous_chart.py`: Specialized chart for exogenous variable visualization

- **ML Pipeline**: `models/scenario_engine.py` implements SARIMAX forecasting with:
  - Model training and caching
  - Real-time prediction with exogenous variable manipulation
  - Batch processing for performance

- **Data Flow**: 
  1. User adjusts controls → State updates
  2. State change triggers model recalculation
  3. New predictions update charts
  4. UI re-renders with new data

### Reflex Framework Patterns
- Components are Python functions returning Reflex components
- State mutations must be done through class methods decorated with appropriate handlers
- Use `rx.State` for reactive state management
- Database operations use SQLite through `rxconfig.py` configuration

### Performance Optimizations
- Redis caching for model predictions (in production)
- Batch processing for multiple scenario calculations
- Debounced user input to prevent API flooding
- Lazy loading of heavy components

## Critical Configuration

### Python Version
Requires Python 3.10+ (supports 3.10, 3.11, 3.12). Check `pyproject.toml` for exact constraints.

### Environment Configuration
- **Development**: Uses SQLite database, no Redis required
- **Production**: Requires Redis for caching, configured in `rxconfig.py`
- **Docker**: All services configured in `docker-compose.yml`

### Database
SQLite database at `sqlite:///auto_sales.db` - automatically created on first run.

## Development Guidelines

### When Adding Features
1. New ML models: Extend `models/scenario_engine.py` following SARIMAX pattern
2. New visualizations: Add to `components/charts.py` using Plotly
3. New controls: Add to `components/controls.py` with state bindings
4. New data sources: Modify `models/data.py` data loading logic

### Testing Requirements
- All new features must include tests in `tests/` directory
- Use appropriate pytest markers (unit, integration, etc.)
- Maintain code quality score above 85/100
- Ensure all tests pass before committing

### Error Handling
- Use `car_sales_dashboard/exceptions.py` for custom exceptions
- Implement proper error boundaries in UI components
- Log errors using configured logging in `utils/logging_config.py`

### Type Safety
- Always include type hints for function parameters and returns
- Use TypedDict for complex data structures
- Run mypy before committing changes

## Common Issues & Solutions

### SSL Certificate Issues (Windows)
Run `run_reflex.bat` which includes SSL certificate fixes.

### Model Training Performance
If model training is slow, check Redis connection in production or consider increasing cache TTL in `models/scenario_engine.py`.

### Frontend Not Updating
Ensure state mutations are done through proper Reflex state methods and not direct assignment.

### Docker Build Failures
Check Python version compatibility and ensure all requirements are properly pinned in `requirements/base.txt`.