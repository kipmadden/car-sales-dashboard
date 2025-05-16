import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract base class for forecasting models"""
    
    @abstractmethod
    def train(self, X, y):
        """Train the model"""
        pass
    
    @abstractmethod
    def predict(self, X):
        """Make predictions"""
        pass


class LinearRegressionModel(BaseModel):
    """Linear regression model for forecasting"""
    
    def __init__(self):
        self.model = LinearRegression()
    
    def train(self, X, y):
        """Train the model"""
        self.model.fit(X, y)
    
    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X)


class RandomForestModel(BaseModel):
    """Random forest model for forecasting"""
    
    def __init__(self, n_estimators=100, max_depth=None):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
    
    def train(self, X, y):
        """Train the model"""
        self.model.fit(X, y)
    
    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X)


class ScenarioEngine:
    """Engine for generating sales forecasts based on exogenous variables"""
    
    def __init__(self, model_type="linear"):
        """
        Initialize the scenario engine
        
        Args:
            model_type (str): Type of model to use ("linear" or "forest")
        """
        if model_type == "linear":
            self.model = LinearRegressionModel()
        elif model_type == "forest":
            self.model = RandomForestModel()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def train(self, data):
        """
        Train the model on historical data
        
        Args:
            data (pd.DataFrame): Historical data with sales and exogenous variables
        """
        # Group by date to get monthly aggregates
        monthly_data = self._aggregate_monthly_data(data)
        
        # Prepare features and target
        X = monthly_data[['unemployment', 'gas_price', 'cpi_all', 'search_volume']].values
        y = monthly_data['sales'].values
        
        # Train the model
        self.model.train(X, y)
        
        # Store the training data for reference
        self.training_data = monthly_data
    
    def forecast(self, data, 
                unemployment_modifier=1.0, 
                gas_price_modifier=1.0, 
                cpi_modifier=1.0, 
                search_volume_modifier=1.0,
                months_ahead=6):
        """
        Generate a forecast based on exogenous variable modifiers
        
        Args:
            data (pd.DataFrame): Historical data
            unemployment_modifier (float): Modifier for unemployment rate
            gas_price_modifier (float): Modifier for gas prices
            cpi_modifier (float): Modifier for consumer price index
            search_volume_modifier (float): Modifier for search volume
            months_ahead (int): Number of months to forecast
        
        Returns:
            pd.DataFrame: Combined historical and forecast data
        """
        # Aggregate monthly data
        monthly_data = self._aggregate_monthly_data(data)
        
        # Set is_forecast flag for historical data
        monthly_data['is_forecast'] = False
        
        # Get last values to base forecast on
        last_values = monthly_data.iloc[-1]
        last_date = last_values['date']
        
        # Generate future dates
        future_dates = [last_date + timedelta(days=30*i) for i in range(1, months_ahead+1)]
        
        # Create forecast data with modified exogenous variables
        forecast_data = []
        
        for i, date in enumerate(future_dates):
            # Apply modifiers with increasing effect over time
            time_factor = 1.0 + (i * 0.05)  # Increase effect over time
            
            # Apply modifiers to exogenous variables
            unemployment = last_values['unemployment'] * unemployment_modifier * time_factor
            gas_price = last_values['gas_price'] * gas_price_modifier * time_factor
            cpi = last_values['cpi_all'] * cpi_modifier * time_factor
            search_volume = last_values['search_volume'] * search_volume_modifier * time_factor
            
            # Predict sales using the model
            features = np.array([[unemployment, gas_price, cpi, search_volume]])
            predicted_sales = self.model.predict(features)[0]
            
            # Add seasonal adjustment
            month = date.month
            if month in [3, 4, 5, 11, 12]:  # Spring and year-end
                predicted_sales *= 1.2
            elif month in [1, 2]:  # Winter
                predicted_sales *= 0.8
            
            # Create forecast record
            forecast_data.append({
                'date': date,
                'year': date.year,
                'month': date.month,
                'sales': predicted_sales,
                'unemployment': unemployment,
                'gas_price': gas_price,
                'cpi_all': cpi,
                'search_volume': search_volume,
                'is_forecast': True
            })
        
        # Combine historical and forecast data
        combined_data = pd.concat([
            monthly_data, 
            pd.DataFrame(forecast_data)
        ]).reset_index(drop=True)
        
        return combined_data
    
    def _aggregate_monthly_data(self, data):
        """
        Aggregate data to monthly level
        
        Args:
            data (pd.DataFrame): Raw data
        
        Returns:
            pd.DataFrame: Aggregated monthly data
        """
        # Group by date to get monthly totals/averages
        monthly_sales = data.groupby('date')['sales'].sum().reset_index()
        monthly_unemployment = data.groupby('date')['unemployment'].mean().reset_index()
        monthly_gas_price = data.groupby('date')['gas_price'].mean().reset_index()
        monthly_cpi = data.groupby('date')['cpi_all'].mean().reset_index()
        monthly_search = data.groupby('date')['search_volume'].mean().reset_index()
        
        # Extract year and month
        monthly_sales['year'] = monthly_sales['date'].dt.year
        monthly_sales['month'] = monthly_sales['date'].dt.month
        
        # Create a combined dataset
        monthly_data = pd.DataFrame({
            'date': monthly_sales['date'],
            'year': monthly_sales['year'],
            'month': monthly_sales['month'],
            'sales': monthly_sales['sales'],
            'unemployment': monthly_unemployment['unemployment'],
            'gas_price': monthly_gas_price['gas_price'],
            'cpi_all': monthly_cpi['cpi_all'],
            'search_volume': monthly_search['search_volume']
        })
        
        return monthly_data