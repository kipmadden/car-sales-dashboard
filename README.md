# Car Sales Dashboard with Exogenous Variable Simulation

An interactive Reflex-based dashboard that allows for exploring the impact of exogenous factors like gas prices and unemployment rates on automotive sales. The dashboard includes geo filters, vehicle category breakdowns, and adjustable economic variables.

## Features

- **Interactive Exogenous Variable Sliders**: Adjust gas prices, unemployment rates, CPI, and search volume to see their impact on sales forecasts
- **Geographic Filtering**: Filter by region, state, and urban areas
- **Vehicle Category Filtering**: Filter by vehicle type, make, model, and year
- **Multiple Visualization Types**: Sales trends, geographic distributions, and vehicle type breakdowns
- **Modular Architecture**: Easily swap ML models and extend functionality
- **Tabs-Based Interface**: Organized sections for different analysis views

## Project Structure

```
car_sales_dashboard/
├── rxconfig.py                # Reflex app configuration
├── app.py                     # Main app module initializing the Reflex App
├── state.py                   # Contains AppState class with state variables and handlers
├── components/                # UI component modules
│   ├── __init__.py            # Package exports
│   ├── controls.py            # UI components for inputs (sliders, dropdowns, etc.)
│   ├── charts.py              # Functions to create Plotly figures
│   └── tables.py              # Functions to create table components
├── models/                    # ML and data modeling modules
│   ├── __init__.py            # Package exports
│   ├── scenario_engine.py     # Forecasting models (linear regression, random forest)
│   └── data.py                # Data loading and generation utilities
└── pages/                     # Page layout modules
    ├── __init__.py            # Package exports
    └── index.py               # Main dashboard page layout
```

## Installation

1. Install the required packages:

```bash
pip install reflex pandas numpy scikit-learn plotly
```

2. Clone this repository:

```bash
git clone <repository-url>
cd car_sales_dashboard
```

3. Run the application:

```bash
reflex run
```

4. Open your browser and go to http://localhost:3000

## Extending the Dashboard

### Adding New Models

To add a new forecasting model:

1. Create a new class that inherits from `BaseModel` in `models/scenario_engine.py`
2. Implement the `train` and `predict` methods
3. Add your model to the model selection in `components/controls.py`
4. Update the model initialization in `state.py`

### Adding New Visualizations

To add a new chart:

1. Create a new chart function in `components/charts.py`
2. Add a corresponding method in `state.py` to prepare the data
3. Add the chart to the appropriate tab in `pages/index.py`

## Data Source

The dashboard currently uses synthetic data generated in `models/data.py`. To use your own data:

1. Create a CSV file with your data
2. Update the `load_data` function in `models/data.py` to load your data
3. Ensure your data has the same column structure or adjust the code accordingly

## License

This project is licensed under the MIT License - see the LICENSE file for details.