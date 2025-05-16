import reflex as rx
import pandas as pd

from car_sales_dashboard.models import load_data, ScenarioEngine
from car_sales_dashboard.components import (
    create_sales_trend_chart,
    create_vehicle_type_chart,
    create_region_chart,
    create_exogenous_impact_chart,
    create_top_models_chart,
    create_state_map_chart,
    create_heatmap_chart
)

# Load data
df = load_data()


class DashboardState(rx.State):
    """State for the dashboard application"""
    
    # Data states
    filtered_data: pd.DataFrame = df
    forecast_data: pd.DataFrame = pd.DataFrame()
    
    # Filter states
    selected_regions: list = []
    selected_states: list = []
    selected_vehicle_types: list = []
    selected_makes: list = []
    selected_models: list = []
    selected_years: list = []
    
    # Model states
    model_type: str = "Linear Regression"
    scenario_engine: ScenarioEngine = ScenarioEngine(model_type="linear")
    
    # Exogenous variable states
    unemployment_modifier: float = 1.0
    gas_price_modifier: float = 1.0
    cpi_modifier: float = 1.0
    search_volume_modifier: float = 1.0
    forecast_months: int = 6
    
    # UI states
    show_table: bool = False
    active_tab: str = "sales"
    
    # Initialize when page loads
    def on_load(self):
        """Called when the page loads"""
        self.filter_data()
        self.train_model()
        self.generate_forecast()
    
    def filter_data(self):
        """Filter data based on selections"""
        filtered = df.copy()
        
        # Apply region filter
        if self.selected_regions:
            filtered = filtered[filtered['region'].isin(self.selected_regions)]
        
        # Apply state filter
        if self.selected_states:
            filtered = filtered[filtered['state'].isin(self.selected_states)]
        
        # Apply vehicle type filter
        if self.selected_vehicle_types:
            filtered = filtered[filtered['vehicle_type'].isin(self.selected_vehicle_types)]
        
        # Apply make filter
        if self.selected_makes:
            filtered = filtered[filtered['make'].isin(self.selected_makes)]
        
        # Apply model filter
        if self.selected_models:
            filtered = filtered[filtered['model'].isin(self.selected_models)]
        
        # Apply year filter
        if self.selected_years:
            filtered = filtered[filtered['model_year'].isin(self.selected_years)]
        
        # Update filtered data
        self.filtered_data = filtered
        
        # Update model and forecast after filtering
        self.train_model()
        self.generate_forecast()
    
    def train_model(self):
        """Train the forecasting model with filtered data"""
        # Initialize model based on selected type
        model_type = "linear" if self.model_type == "Linear Regression" else "forest"
        self.scenario_engine = ScenarioEngine(model_type=model_type)
        
        # Train the model if we have data
        if not self.filtered_data.empty:
            self.scenario_engine.train(self.filtered_data)
    
    def generate_forecast(self):
        """Generate forecast based on selected modifiers"""
        # Generate forecast if we have data
        if not self.filtered_data.empty:
            self.forecast_data = self.scenario_engine.forecast(
                self.filtered_data,
                unemployment_modifier=self.unemployment_modifier,
                gas_price_modifier=self.gas_price_modifier,
                cpi_modifier=self.cpi_modifier,
                search_volume_modifier=self.search_volume_modifier,
                months_ahead=self.forecast_months
            )
    
    # Filter update handlers
    def update_regions(self, regions):
        """Update selected regions"""
        self.selected_regions = regions
        self.filter_data()
    
    def update_states(self, states):
        """Update selected states"""
        self.selected_states = states
        self.filter_data()
    
    def update_vehicle_types(self, types):
        """Update selected vehicle types"""
        self.selected_vehicle_types = types
        self.filter_data()
    
    def update_makes(self, makes):
        """Update selected makes"""
        self.selected_makes = makes
        self.filter_data()
    
    def update_models(self, models):
        """Update selected models"""
        self.selected_models = models
        self.filter_data()
    
    def update_years(self, years):
        """Update selected years"""
        self.selected_years = years
        self.filter_data()
    
    # Exogenous variable update handlers
    def update_unemployment(self, value):
        """Update unemployment modifier"""
        self.unemployment_modifier = value
        self.generate_forecast()
    
    def update_gas_price(self, value):
        """Update gas price modifier"""
        self.gas_price_modifier = value
        self.generate_forecast()
    
    def update_cpi(self, value):
        """Update CPI modifier"""
        self.cpi_modifier = value
        self.generate_forecast()
    
    def update_search_volume(self, value):
        """Update search volume modifier"""
        self.search_volume_modifier = value
        self.generate_forecast()
    
    def update_forecast_months(self, value):
        """Update forecast months"""
        self.forecast_months = value
        self.generate_forecast()
    
    def update_model_type(self, value):
        """Update model type"""
        self.model_type = value
        self.train_model()
        self.generate_forecast()
    
    # UI update handlers
    def toggle_table(self):
        """Toggle table visibility"""
        self.show_table = not self.show_table
    
    def set_active_tab(self, tab):
        """Set active tab"""
        self.active_tab = tab
    
    # Chart creation methods
    def get_sales_trend_chart(self):
        """Get sales trend chart"""
        return create_sales_trend_chart(self.forecast_data)
    
    def get_vehicle_type_chart(self):
        """Get vehicle type chart"""
        return create_vehicle_type_chart(self.filtered_data)
    
    def get_region_chart(self):
        """Get region chart"""
        return create_region_chart(self.filtered_data)
    
    def get_exogenous_impact_chart(self):
        """Get exogenous impact chart"""
        return create_exogenous_impact_chart(self.forecast_data)
    
    def get_top_models_chart(self):
        """Get top models chart"""
        return create_top_models_chart(self.filtered_data)
    
    def get_state_map_chart(self):
        """Get state map chart"""
        return create_state_map_chart(self.filtered_data)
    
    def get_sales_by_month_chart(self):
        """Get sales by month heatmap"""
        return create_heatmap_chart(self.filtered_data, x_col='month', y_col='vehicle_type')