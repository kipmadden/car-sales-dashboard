import reflex as rx
import pandas as pd
import plotly.graph_objects as go

from car_sales_dashboard.components.charts import (
    create_sales_trend_chart,
    create_exogenous_variables_chart,
    create_vehicle_type_chart,
    create_region_chart,
    create_top_models_chart,
    create_state_map_chart,
    create_heatmap_chart
)
from car_sales_dashboard.models import load_data, ScenarioEngine
from pydantic import PrivateAttr
from car_sales_dashboard.utils.logging_config import logger, perf_logger
from car_sales_dashboard.exceptions import ChartBuildError, DataValidationError, ModelTrainingError
# Temporarily disabled due to SSL import issue
# from car_sales_dashboard.utils.ui_utils import create_chart_error_component
from car_sales_dashboard.utils.error_handler import ErrorHandler, error_handler, validate_input, Validators
from car_sales_dashboard.utils.performance import (
    cached, 
    performance_monitor, 
    DataFrameOptimizer, 
    QueryOptimizer,
    clear_cache
)
from car_sales_dashboard.utils.validation import (
    DataValidator, 
    InputSanitizer, 
    sanitize_output, 
    sanitize_chart_config
)

# Load data with reproducible seeding and optimization (S5 remediation + Fix 3)
from rxconfig import DEFAULT_SEED

@performance_monitor("data_loading")
def load_optimized_data():
    """Load and optimize the initial dataset for better performance."""
    raw_df = load_data(seed=DEFAULT_SEED)
    
    # Optimize data types to reduce memory usage
    optimized_df = DataFrameOptimizer.optimize_dtypes(raw_df)
    
    logger.info(f"Loaded and optimized dataset: {optimized_df.shape} shape, "
                f"{optimized_df.memory_usage(deep=True).sum() / 1024 / 1024:.1f}MB")
    
    return optimized_df

df = load_optimized_data()


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
    
    @performance_monitor("data_filtering")
    def filter_data(self):
        """Filter data based on selections with optimized performance"""
        # Build filter dictionary for efficient filtering
        filters = {}
        
        if self.selected_regions:
            filters['region'] = self.selected_regions
        if self.selected_states:
            filters['state'] = self.selected_states
        if self.selected_vehicle_types:
            filters['vehicle_type'] = self.selected_vehicle_types
        if self.selected_makes:
            filters['make'] = self.selected_makes
        if self.selected_models:
            filters['model'] = self.selected_models
        if self.selected_years:
            filters['model_year'] = self.selected_years
        
        # Use efficient filtering if filters exist
        if filters:
            filtered = QueryOptimizer.build_efficient_filter(df, filters)
        else:
            filtered = df.copy()
        
        logger.debug(f"Data filtering: {len(df)} → {len(filtered)} rows "
                    f"({len(filtered)/len(df)*100:.1f}% retained)")
        
        # Clear filter-dependent cache entries when data changes
        clear_cache("vehicle_type")
        clear_cache("region")
        clear_cache("top_models")
        clear_cache("state_map")
        clear_cache("heatmap")
        
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
    
    @performance_monitor("forecast_generation")
    def generate_forecast(self):
        """Generate forecast based on selected modifiers with cache invalidation"""
        # Clear forecast-related cache entries when generating new forecast
        clear_cache("sales_trend")
        clear_cache("exogenous")
        
        # Generate forecast if we have data - safely check if attribute exists and if dataframe is empty
        try:
            if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
                # Log the current modifiers being used
                logger.debug(f"Generating forecast with modifiers: unemployment={self.unemployment_modifier}, " 
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
                logger.info(f"Forecast generated successfully with {len(self.forecast_data)} records")
            else:
                logger.warning("Cannot generate forecast: No filtered data available")
                self._forecast_df = pd.DataFrame()
                self.forecast_data = []
        except Exception as e:
            # Handle any errors during forecast generation
            logger.error(f"Error generating forecast: {e}", exc_info=True)
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
            logger.error(f"Error converting years: {e}", exc_info=True)
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

    @validate_input(Validators.modifier_range, "Gas price modifier")
    def update_gas_price(self, value):
        """Update gas price modifier with enhanced validation"""
        try:
            # Sanitize input first
            sanitized_value = InputSanitizer.sanitize_numeric(value, min_val=0.1, max_val=3.0)
            
            # Validate using the comprehensive validator
            is_valid, errors = DataValidator.validate_modifiers(
                sanitized_value, self.cpi_modifier, self.search_volume_modifier
            )
            
            if not is_valid:
                raise DataValidationError(
                    field_name="gas_price_modifier",
                    value=value,
                    reason=f"Validation failed: {'; '.join(errors)}"
                )
            
            logger.debug(f"Updating gas price modifier to {sanitized_value}")
            perf_logger.log_user_action("gas_price_update", f"new_value={sanitized_value}")
            self.gas_price_modifier = sanitized_value
            
            # Clear related caches
            clear_cache("sales_trend")
            clear_cache("forecast_data")
            
            # Force forecast regeneration with explicit logging
            logger.debug("Generating new forecast after gas price update")
            self.generate_forecast()
            
        except (ValueError, TypeError, DataValidationError) as e:
            logger.error(f"Invalid gas price value: {value} - {e}")
            # Don't update the value if validation fails
            raise DataValidationError(
                field_name="gas_price_modifier",
                value=value,
                reason="Must be a valid number between 0.1 and 3.0"
            )
    
    @validate_input(Validators.modifier_range, "CPI modifier")
    def update_cpi(self, value):
        """Update CPI modifier with enhanced validation"""
        try:
            # Sanitize input first
            sanitized_value = InputSanitizer.sanitize_numeric(value, min_val=0.1, max_val=3.0)
            
            # Validate using the comprehensive validator
            is_valid, errors = DataValidator.validate_modifiers(
                self.gas_price_modifier, sanitized_value, self.search_volume_modifier
            )
            
            if not is_valid:
                raise DataValidationError(
                    field_name="cpi_modifier",
                    value=value,
                    reason=f"Validation failed: {'; '.join(errors)}"
                )
            
            logger.debug(f"Updating CPI modifier to {sanitized_value}")
            perf_logger.log_user_action("cpi_update", f"new_value={sanitized_value}")
            self.cpi_modifier = sanitized_value
            
            # Clear related caches
            clear_cache("sales_trend")
            clear_cache("forecast_data")
            
            self.generate_forecast()
            
        except (ValueError, TypeError, DataValidationError) as e:
            logger.error(f"Invalid CPI value: {value} - {e}")
            raise DataValidationError(
                field_name="cpi_modifier",
                value=value,
                reason="Must be a valid number between 0.1 and 3.0"
            )
    
    @validate_input(Validators.modifier_range, "Search volume modifier")
    def update_search_volume(self, value):
        """Update search volume modifier with enhanced validation"""
        try:
            # Sanitize input first
            sanitized_value = InputSanitizer.sanitize_numeric(value, min_val=0.1, max_val=3.0)
            
            # Validate using the comprehensive validator
            is_valid, errors = DataValidator.validate_modifiers(
                self.gas_price_modifier, self.cpi_modifier, sanitized_value
            )
            
            if not is_valid:
                raise DataValidationError(
                    field_name="search_volume_modifier",
                    value=value,
                    reason=f"Validation failed: {'; '.join(errors)}"
                )
            
            logger.debug(f"Updating search volume modifier to {sanitized_value}")
            perf_logger.log_user_action("search_volume_update", f"new_value={sanitized_value}")
            self.search_volume_modifier = sanitized_value
            
            # Clear related caches
            clear_cache("sales_trend")
            clear_cache("forecast_data")
            
            self.generate_forecast()
            
        except (ValueError, TypeError, DataValidationError) as e:
            logger.error(f"Invalid search volume value: {value} - {e}")
            raise DataValidationError(
                field_name="search_volume_modifier",
                value=value,
                reason="Must be a valid number between 0.1 and 3.0"
            )

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
        logger.debug(f"Tab changed to: {tab}")
        perf_logger.log_user_action("tab_change", f"new_tab={tab}")
        self.active_tab = tab
        # Force re-evaluation of charts for the new tab
        self.filter_data()

    # UI update handlers
    def toggle_table(self, value: bool):
        """Toggle the table visibility in the dashboard UI."""
        logger.debug(f"Toggling table visibility to: {value}")
        perf_logger.log_user_action("table_toggle", f"show_table={value}")
        self.show_table = value
        # No need to regenerate forecast or filter data, just update the UI state

    def _handle_chart_error(self, chart_type: str, error: Exception) -> dict:
        """
        Enhanced chart error handling with user-friendly feedback.
        
        Args:
            chart_type: Type of chart that failed
            error: The exception that occurred
            
        Returns:
            Dict representation of error chart with helpful messaging
        """
        # Use the enhanced error handler
        return ErrorHandler.handle_chart_error(
            chart_type=chart_type,
            error=error,
            data_info=f"Filtered data shape: {getattr(self, '_filtered_df', pd.DataFrame()).shape}"
        )
        fig = go.Figure()
        fig.add_annotation(
            text=f"⚠️ Failed to render {chart_type} chart<br>See application logs for details",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(color="#d63384", size=16),
            align="center"
        )
        fig.update_layout(
            title=f"{chart_type} Chart - Error",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400,
            paper_bgcolor="rgba(248, 249, 250, 0.8)",
            plot_bgcolor="rgba(248, 249, 250, 0.8)",
            font=dict(color="black"),
            annotations=[
                dict(
                    text="Please check your data or contact support if this persists",
                    xref="paper", yref="paper",
                    x=0.5, y=0.3,
                    showarrow=False,
                    font=dict(color="#6c757d", size=12)
                )
            ]
        )
        
        return fig.to_dict()

    # Chart creation methods - these must be decorated with @rx.var with type annotations    
    @rx.var
    @error_handler("chart_build", fallback_value={})
    def get_sales_trend_chart(self) -> dict:
        """Get sales trend chart with enhanced error handling and caching"""
        # Check if _forecast_df is initialized before using it
        if hasattr(self, "_forecast_df") and isinstance(self._forecast_df, pd.DataFrame) and not self._forecast_df.empty:
            # Create cache key based on data hash and modifiers
            data_hash = str(hash(tuple(self._forecast_df.values.flatten().tolist()[:100])))  # Sample for performance
            cache_key = f"sales_trend_{data_hash}_{self.gas_price_modifier}_{self.cpi_modifier}"
            
            # Use cached chart creation
            return self._create_cached_chart(
                chart_func=create_sales_trend_chart,
                data=self._forecast_df,
                cache_key=cache_key,
                chart_name="Sales Trend"
            )
        else:
            logger.warning("No forecast data available for chart")
            return ErrorHandler._create_error_chart(
                "Sales Trend", 
                "chart_build"
            )

    @performance_monitor("chart_creation")
    def _create_cached_chart(self, chart_func, data, cache_key: str, chart_name: str) -> dict:
        """
        Create charts with caching and output sanitization for improved performance and security.
        
        Args:
            chart_func: Chart creation function
            data: Data for chart creation (will be validated)
            cache_key: Unique cache key
            chart_name: Name of the chart for error handling
            
        Returns:
            Sanitized chart dictionary or error chart
        """
        # Validate input data
        if data is None or (isinstance(data, pd.DataFrame) and data.empty):
            logger.warning(f"Invalid data provided for {chart_name} chart")
            return ErrorHandler._create_error_chart(chart_name, "invalid_data")
        
        # Try to get from cache first
        from car_sales_dashboard.utils.performance import get_cache_instance
        cache = get_cache_instance()
        
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Using cached {chart_name} chart")
            # Sanitize cached output before returning
            return sanitize_output(cached_result)
        
        # Generate new chart
        try:
            logger.debug(f"Generating new {chart_name} chart - Data shape: {data.shape}")
            chart_result = chart_func(data)
            
            # Sanitize chart configuration if it's a dictionary
            if isinstance(chart_result, dict):
                chart_result = sanitize_chart_config(chart_result)
            
            # Sanitize all output data
            sanitized_result = sanitize_output(chart_result)
            
            # Cache the sanitized result for 5 minutes
            cache.set(cache_key, sanitized_result, ttl=300)
            logger.debug(f"Cached {chart_name} chart with key: {cache_key[:20]}...")
            
            return sanitized_result
            
        except Exception as e:
            logger.error(f"Failed to create {chart_name} chart: {e}")
            return ErrorHandler._create_error_chart(chart_name, "chart_build")

    @rx.var
    @error_handler("chart_build", fallback_value={})
    def get_vehicle_type_chart(self) -> dict:
        """Get vehicle type chart with enhanced error handling and caching"""
        if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
            # Create cache key based on filtered data
            data_hash = str(hash(tuple(self._filtered_df['vehicle_type'].value_counts().head(10).to_dict().items())))
            cache_key = f"vehicle_type_{data_hash}_{len(self._filtered_df)}"
            
            return self._create_cached_chart(
                chart_func=create_vehicle_type_chart,
                data=self._filtered_df,
                cache_key=cache_key,
                chart_name="Vehicle Type"
            )
        else:
            return ErrorHandler._create_error_chart("Vehicle Type", "chart_build")
    
    @rx.var
    @error_handler("chart_build", fallback_value={})
    def get_region_chart(self) -> dict:
        """Get region chart with enhanced error handling and caching"""
        if hasattr(self, "_filtered_df") and isinstance(self._filtered_df, pd.DataFrame) and not self._filtered_df.empty:
            # Create cache key based on filtered data
            data_hash = str(hash(tuple(self._filtered_df['region'].value_counts().to_dict().items())))
            cache_key = f"region_{data_hash}_{len(self._filtered_df)}"
            
            return self._create_cached_chart(
                chart_func=create_region_chart,
                data=self._filtered_df,
                cache_key=cache_key,
                chart_name="Region"
            )
            return create_region_chart(self._filtered_df)
        else:
            return ErrorHandler._create_error_chart("Region", "chart_build")

    @rx.var
    @error_handler("chart_build", fallback_value={})
    def get_exogenous_impact_chart(self) -> dict:
        """Get exogenous impact chart with enhanced error handling"""
        if hasattr(self, "_forecast_df") and isinstance(self._forecast_df, pd.DataFrame) and not self._forecast_df.empty:
            return create_exogenous_variables_chart(self._forecast_df)
        else:
            return ErrorHandler._create_error_chart("Exogenous Impact", "chart_build")
    
    @rx.var
    @error_handler("chart_build", fallback_value={})
    def get_exogenous_figure(self) -> dict:
        """Get exogenous variable chart with enhanced error handling"""
        logger.debug(f"get_exogenous_figure with gas_price={self.gas_price_modifier}")
        if hasattr(self, "_forecast_df") and isinstance(self._forecast_df, pd.DataFrame) and not self._forecast_df.empty:
            try:
                return create_exogenous_variables_chart(self._forecast_df)
            except ChartBuildError as e:
                return self._handle_chart_error("Exogenous Variables", e)
            except Exception as e:
                # Wrap unexpected errors in ChartBuildError
                chart_error = ChartBuildError("Exogenous Variables", e, f"DataFrame shape: {self._forecast_df.shape}")
                return self._handle_chart_error("Exogenous Variables", chart_error)
        else:
            logger.warning("No forecast data available for exogenous chart")
            # Return an informational chart for no data case
            fig = go.Figure()
            fig.add_annotation(
                text="📊 No forecast data available<br>Please generate a forecast first",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(color="#856404", size=16),
                align="center"
            )
            fig.update_layout(
                title="Exogenous Variables Chart",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                height=400,
                paper_bgcolor="rgba(255, 243, 205, 0.3)",
                plot_bgcolor="rgba(255, 243, 205, 0.3)",
                font=dict(color="black")
            )
            return fig.to_dict()


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
    
    @error_handler("file_upload", fallback_value=False)
    def validate_and_upload_data(self, file_path: str, file_size: int = 0) -> bool:
        """
        Validate and upload new data file with comprehensive security checks.
        
        Args:
            file_path: Path to the uploaded file
            file_size: Size of the file in bytes
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            from car_sales_dashboard.utils.validation import FileValidator
            
            # Validate file parameters
            is_valid_file, file_errors = FileValidator.validate_file_upload(file_path, file_size)
            if not is_valid_file:
                logger.error(f"File validation failed: {file_errors}")
                raise DataValidationError(
                    field_name="file_upload",
                    value=file_path,
                    reason=f"File validation errors: {'; '.join(file_errors)}"
                )
            
            # Validate file content
            is_valid_content, content_errors, df = FileValidator.validate_csv_content(file_path)
            if not is_valid_content:
                logger.error(f"File content validation failed: {content_errors}")
                raise DataValidationError(
                    field_name="file_content",
                    value=file_path,
                    reason=f"Content validation errors: {'; '.join(content_errors)}"
                )
            
            # If validation passes, update the data
            if df is not None:
                # Optimize the new DataFrame
                optimized_df = DataFrameOptimizer.optimize_dtypes(df)
                
                # Update state with new data
                self._filtered_df = optimized_df
                self.filtered_data = optimized_df.to_dict("records")
                
                # Clear all caches since data changed
                clear_cache()
                
                # Retrain model with new data
                self.train_model()
                self.generate_forecast()
                
                logger.info(f"Successfully uploaded and processed file: {file_path}")
                perf_logger.log_user_action("data_upload", f"file={file_path}, rows={len(df)}")
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {e}")
            return False

    @error_handler("date_filter", fallback_value=True)
    def validate_date_filter(self, start_date: str, end_date: str) -> bool:
        """
        Validate date range filter with comprehensive checks.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            True if dates are valid, False otherwise
        """
        try:
            # Sanitize date inputs
            start_date = InputSanitizer.sanitize_string(start_date, max_length=10)
            end_date = InputSanitizer.sanitize_string(end_date, max_length=10)
            
            # Validate date range
            is_valid, errors = DataValidator.validate_date_range(start_date, end_date)
            
            if not is_valid:
                logger.error(f"Date validation failed: {errors}")
                raise DataValidationError(
                    field_name="date_range",
                    value=f"{start_date} to {end_date}",
                    reason=f"Date validation errors: {'; '.join(errors)}"
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Date filter validation failed: {e}")
            return False
