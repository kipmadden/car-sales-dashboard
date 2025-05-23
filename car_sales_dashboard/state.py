import reflex as rx
import pandas as pd
import plotly.graph_objects as go

from car_sales_dashboard.components.exogenous_chart import create_exogenous_figure
from car_sales_dashboard.models import load_data, ScenarioEngine
from pydantic import PrivateAttr
from car_sales_dashboard.components import (
    create_sales_trend_chart,
    create_vehicle_type_chart,
    create_region_chart,
    create_exogenous_impact_chart,
    create_top_models_chart,
    create_state_map_chart,
    create_heatmap_chart,
)

# Load data
df = load_data()


class DashboardState(rx.State):
    """State for the dashboard application"""
    
    # Data states stored as JSON-serializable lists
    filtered_data: list[dict] = df.to_dict("records")
    forecast_data: list[dict] = []

    # Private DataFrame storage
    _filtered_df: pd.DataFrame = PrivateAttr(default=df)
    _forecast_df: pd.DataFrame = PrivateAttr(default_factory=pd.DataFrame)
    
    # Filter states
    selected_regions: list = []
    selected_states: list = []
    selected_vehicle_types: list = []
    selected_makes: list = []
    selected_models: list = []
    selected_years: list = []
    
    # Model states
    model_type: str = "Linear Regression"
    _scenario_engine: ScenarioEngine = PrivateAttr()
    
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the scenario engine
        self._scenario_engine = ScenarioEngine(model_type="linear")
    
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
        self._filtered_df = filtered
        self.filtered_data = filtered.to_dict("records")
        
        # Update model and forecast after filtering
        self.train_model()
        self.generate_forecast()
        
    def train_model(self):
        """Train the forecasting model with filtered data"""
        # Initialize model based on selected type
        model_type = "linear" if self.model_type == "Linear Regression" else "forest"
        self._scenario_engine = ScenarioEngine(model_type=model_type)
        
        # Train the model if we have data - safely check if attribute exists and if dataframe is empty
        try:
            if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
                self._scenario_engine.train(self._filtered_df)
        except AttributeError:
            # Handle case where _filtered_df might not be accessible
            pass
    
    def generate_forecast(self):
        """Generate forecast based on selected modifiers"""
        # Generate forecast if we have data - safely check if attribute exists and if dataframe is empty
        try:
            if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
                # Log the current modifiers being used
                print(f"Generating forecast with modifiers: unemployment={self.unemployment_modifier}, " 
                      f"gas_price={self.gas_price_modifier}, cpi={self.cpi_modifier}, "
                      f"search_volume={self.search_volume_modifier}, months={self.forecast_months}")
                
                forecast_df = self._scenario_engine.forecast(
                    self._filtered_df,
                    unemployment_modifier=self.unemployment_modifier,
                    gas_price_modifier=self.gas_price_modifier,
                    cpi_modifier=self.cpi_modifier,
                    search_volume_modifier=self.search_volume_modifier,
                    months_ahead=self.forecast_months
                )
                
                # Update both the private DataFrame and the public serializable list
                self._forecast_df = forecast_df
                self.forecast_data = forecast_df.to_dict("records")
                
                # Log success information for debugging
                print(f"Forecast generated successfully with {len(self.forecast_data)} records")
            else:
                print("Cannot generate forecast: No filtered data available")
                self._forecast_df = pd.DataFrame()
                self.forecast_data = []
        except Exception as e:
            # Handle any errors during forecast generation
            print(f"Error generating forecast: {e}")
            import traceback
            traceback.print_exc()
            self._forecast_df = pd.DataFrame()
            self.forecast_data = []
    
    # Filter update handlers
    def update_regions(self, regions):
        """Update selected regions"""
        # Ensure regions is a list, even if a single string is passed
        if regions and isinstance(regions, str):
            self.selected_regions = [regions]
        else:
            self.selected_regions = regions
        self.filter_data()
    
    def update_states(self, states):
        """Update selected states"""
        # Ensure states is a list, even if a single string is passed
        if states and isinstance(states, str):
            self.selected_states = [states]
        else:
            self.selected_states = states
        self.filter_data()
    
    def update_vehicle_types(self, types):
        """Update selected vehicle types"""
        # Ensure types is a list, even if a single string is passed
        if types and isinstance(types, str):
            self.selected_vehicle_types = [types]
        else:
            self.selected_vehicle_types = types
        self.filter_data()
    
    def update_makes(self, makes):
        """Update selected makes"""
        # Ensure makes is a list, even if a single string is passed
        if makes and isinstance(makes, str):
            self.selected_makes = [makes]
        else:
            self.selected_makes = makes
        self.filter_data()
    def update_models(self, models):
        """Update selected models"""
        # Ensure models is a list, even if a single string is passed
        if models and isinstance(models, str):
            self.selected_models = [models]
        else:
            self.selected_models = models
        self.filter_data()
    
    def update_years(self, years):
        """Update selected years"""
        # Years are provided as strings from the UI; convert to integers for
        # filtering against the numeric ``model_year`` column.
        try:
            self.selected_years = [int(y) for y in years]
        except Exception as e:
            # Handle conversion error, e.g., log or set to empty
            print(f"Error converting years: {e}")
            self.selected_years = []
        self.filter_data()

    # Exogenous variable update handlers
    def update_unemployment(self, value):
        """Update unemployment modifier"""
        # Convert value to float if it's a list (common issue with sliders in Reflex)
        if isinstance(value, list) and len(value) > 0:
            value = float(value[0])
        self.unemployment_modifier = float(value)
        self.generate_forecast()

    def update_gas_price(self, value):
        """Update gas price modifier"""
        # Convert value to float if it's a list
        if isinstance(value, list) and len(value) > 0:
            value = float(value[0])
        value = float(value)
        print(f"Updating gas price modifier to {value}")
        self.gas_price_modifier = value
        # Force forecast regeneration with explicit logging
        print("Generating new forecast after gas price update")
        self.generate_forecast()
    
    def update_cpi(self, value):
        """Update CPI modifier"""
        # Convert value to float if it's a list
        if isinstance(value, list) and len(value) > 0:
            value = float(value[0])
        self.cpi_modifier = float(value)
        self.generate_forecast()
    
    def update_search_volume(self, value):
        """Update search volume modifier"""
        # Convert value to float if it's a list
        if isinstance(value, list) and len(value) > 0:
            value = float(value[0])
        self.search_volume_modifier = float(value)
        self.generate_forecast()

    def update_forecast_months(self, value):
        """Update forecast months"""
        # Convert value to int if it's a list
        if isinstance(value, list) and len(value) > 0:
            value = int(value[0])
        self.forecast_months = int(value)
        self.generate_forecast()
    
    def update_model_type(self, value):
        """Update model type"""
        self.model_type = value
        self.train_model()
        self.generate_forecast()
    def update_active_tab(self, tab: str):
        """Update the active tab."""
        print(f"Tab changed to: {tab}")  # Debug print
        self.active_tab = tab
        # Force re-evaluation of charts for the new tab
        self.filter_data()

    # UI update handlers
    def toggle_table(self, value: bool):
        """Toggle the table visibility in the dashboard UI."""
        print(f"Toggling table visibility to: {value}")
        self.show_table = value
        # No need to regenerate forecast or filter data, just update the UI state

    # Chart creation methods - these must be decorated with @rx.var with type annotations    
    @rx.var
    def get_sales_trend_chart(self) -> dict:
        """Get sales trend chart"""
        # Check if _forecast_df is initialized before using it
        if hasattr(self, "_forecast_df") and isinstance(self._forecast_df, pd.DataFrame) and not self._forecast_df.empty:
            # Add debug print
            print(f"Forecast DF shape: {self._forecast_df.shape}")
            print(f"Forecast DF columns: {self._forecast_df.columns.tolist()}")
            print(f"First 3 rows: {self._forecast_df.head(3).to_dict('records')}")
            
            # Generate a sample chart if the real one fails
            try:
                return create_sales_trend_chart(self._forecast_df)
            except Exception as e:
                print(f"Error creating sales trend chart: {str(e)}")
                # Create a fallback chart
                import plotly.graph_objects as go
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines', name='Sample Data'))
                fig.update_layout(
                    title='Sample Chart (Error in main chart)',
                    xaxis_title='Date',
                    yaxis_title='Sales',
                    font=dict(color='black'),
                )
                return fig.to_dict()
        else:
            print("No forecast data available for chart")
            return {}

    @rx.var
    def get_vehicle_type_chart(self) -> dict:
        """Get vehicle type chart"""
        if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
            return create_vehicle_type_chart(self._filtered_df)
        else:
            return {}
    
    @rx.var
    def get_region_chart(self) -> dict:
        """Get region chart"""
        if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
            return create_region_chart(self._filtered_df)
        else:
            return {}

    @rx.var
    def get_exogenous_impact_chart(self) -> dict:
        """Get exogenous impact chart"""
        if hasattr(self, "_forecast_df") and isinstance(self._forecast_df, pd.DataFrame) and not self._forecast_df.empty:
            return create_exogenous_impact_chart(self._forecast_df)
        else:
            return {}
    
    @rx.var
    def get_exogenous_figure(self) -> go.Figure:
        """Get exogenous variable chart as a Plotly Figure."""
        print(f"get_exogenous_figure with gas_price={self.gas_price_modifier}")
        return create_exogenous_figure(
            "Exogenous Variable Trends",
            self.forecast_data
        )


    # @rx.var
    # def get_exogenous_variable_chart(self) -> rx.Component:
    #     """Get exogenous variable chart - returns a component for direct use in UI"""
    #     print(f"Creating exogenous variable chart with gas_price={self.gas_price_modifier}")
    #     # Use directly in UI - returns the component, not just the figure data
    #     return create_exogenous_chart(
    #         "Exogenous Variable Trends",
    #         self.forecast_data,  # This is a Var and will trigger updates when it changes
    #         height="500px"
    #     )
    
    @rx.var
    def get_top_models_chart(self) -> dict:
        """Get top models chart"""
        if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
            return create_top_models_chart(self._filtered_df)
        else:
            return {}
    
    @rx.var
    def get_state_map_chart(self) -> dict:
        """Get state map chart"""
        if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
            return create_state_map_chart(self._filtered_df)
        else:
            return {}
    
    @rx.var
    def get_sales_by_month_chart(self) -> dict:
        """Get sales by month heatmap"""
        if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
            return create_heatmap_chart(self._filtered_df, x_col='month', y_col='vehicle_type')
        else:
            return {}
