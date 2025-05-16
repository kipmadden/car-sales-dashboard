# Import key classes and functions for easier access
from car_sales_dashboard.models.data import generate_sample_data, load_data
from car_sales_dashboard.models.scenario_engine import ScenarioEngine, LinearRegressionModel, RandomForestModel

# This makes it possible to import directly from the models package
# For example: from models import ScenarioEngine, load_data