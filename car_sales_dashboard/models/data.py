import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from scipy.stats import truncnorm
from typing import Dict, Any, Optional

# Import configuration
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from rxconfig import DEFAULT_SEED, DATA_BOUNDS

# Import logging
from car_sales_dashboard.utils.logging_config import logger


def clamp_value(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value to be within specified bounds."""
    return max(min_val, min(max_val, value))


def generate_bounded_random(
    distribution: str, 
    size: int, 
    bounds: Dict[str, float], 
    **kwargs
) -> np.ndarray:
    """
    Generate random values within realistic bounds using truncated normal distribution.
    
    Args:
        distribution: Type of distribution ('normal', 'uniform')
        size: Number of values to generate
        bounds: Dictionary with 'min' and 'max' keys
        **kwargs: Additional parameters for the distribution
        
    Returns:
        np.ndarray: Array of bounded random values
    """
    min_val = bounds['min']
    max_val = bounds['max']
    
    if distribution == 'normal':
        # Use truncated normal distribution for more realistic data
        mean = kwargs.get('mean', (min_val + max_val) / 2)
        std = kwargs.get('std', (max_val - min_val) / 6)  # 99.7% within bounds
        
        # Standardize parameters for truncnorm
        a = (min_val - mean) / std
        b = (max_val - mean) / std
        
        values = truncnorm.rvs(a, b, loc=mean, scale=std, size=size)
        
    elif distribution == 'uniform':
        values = np.random.uniform(min_val, max_val, size)
        
    else:
        raise ValueError(f"Unsupported distribution: {distribution}")
    
    # Ensure all values are within bounds (safety check)
    return np.array([clamp_value(v, min_val, max_val) for v in values])


def generate_sample_data(seed: Optional[int] = None) -> pd.DataFrame:
    """
    Generate synthetic car sales data with exogenous factors.
    
    Args:
        seed: Random seed for reproducible data generation
    
    Returns:
        pd.DataFrame: A DataFrame with synthetic sales data
    """
    # Set seed for reproducibility (S5 remediation)
    if seed is None:
        seed = DEFAULT_SEED
    
    np.random.seed(seed)
    logger.info(f"Generating synthetic data with seed: {seed}")
    
    # Define date range
    start_date = datetime(2015, 1, 1)
    dates = [start_date + timedelta(days=30*i) for i in range(36)]
    
    # Generate realistic exogenous variables with proper bounds
    sales_base = generate_bounded_random(
        'normal', 36, DATA_BOUNDS['sales'], 
        mean=15000, std=3000
    )
    
    unemployment = generate_bounded_random(
        'normal', 36, DATA_BOUNDS['unemployment'],
        mean=5.5, std=1.2
    )
    
    gas_price = generate_bounded_random(
        'normal', 36, DATA_BOUNDS['gas_price'],
        mean=3.0, std=0.8
    )
    
    cpi_energy = generate_bounded_random(
        'normal', 36, DATA_BOUNDS['cpi_energy'],
        mean=215, std=25
    )
    
    cpi_all = generate_bounded_random(
        'normal', 36, DATA_BOUNDS['cpi_all'],
        mean=250, std=15
    )
    
    search_volume = generate_bounded_random(
        'normal', 36, DATA_BOUNDS['search_volume'],
        mean=70, std=20
    )
    
    # Create base data with bounded random variables
    data = {
        'date': dates,
        'year': [d.year for d in dates],
        'month': [d.month for d in dates],
        'sales': sales_base,
        'unemployment': unemployment,
        'gas_price': gas_price,
        'cpi_energy': cpi_energy,
        'cpi_all': cpi_all,
        'search_volume': search_volume
    }
    
    # Apply economic effects with clamping to maintain realistic bounds
    for i, month in enumerate(data['month']):
        sales_modifier = 1.0
        
        # Seasonal effects
        if month in [3, 4, 5, 11, 12]:  # Spring and holiday season
            sales_modifier *= 1.2
        elif month in [1, 2]:  # Winter slowdown
            sales_modifier *= 0.8
            
        # Gas price effects (bounded)
        if data['gas_price'][i] > 3.5:
            sales_modifier *= 0.9  # High gas prices reduce sales
            
        # Unemployment effects (bounded)
        if data['unemployment'][i] > 6.0:
            sales_modifier *= 0.85  # High unemployment reduces sales
        
        # Apply modifier and clamp result
        new_sales = data['sales'][i] * sales_modifier
        data['sales'][i] = clamp_value(new_sales, DATA_BOUNDS['sales']['min'], DATA_BOUNDS['sales']['max'])
    
    df = pd.DataFrame(data)
    logger.debug(f"Generated base data with {len(df)} time periods")
    
    # Add vehicle categories and regions for filtering
    vehicle_types = ['Sedan', 'SUV', 'Truck', 'Compact']
    regions = ['North', 'South', 'East', 'West']
    states = {
        'North': ['NY', 'PA', 'MI', 'IL', 'OH', 'WI', 'MN'],
        'South': ['TX', 'FL', 'GA', 'NC', 'SC', 'TN', 'AL'],
        'East': ['MA', 'CT', 'RI', 'NJ', 'DE', 'MD', 'VA'],
        'West': ['CA', 'WA', 'OR', 'NV', 'AZ', 'CO', 'UT']
    }
    
    # Expand the dataframe to include different vehicle types and regions
    expanded_data = []
    
    for _, row in df.iterrows():
        for vehicle in vehicle_types:
            for region in regions:
                for state in states[region]:
                    # Create variation in sales by vehicle type, region, and state
                    sales_modifier = 1.0
                    
                    # Vehicle type modifiers
                    if vehicle == 'SUV':
                        sales_modifier *= 1.4  # SUVs sell more
                    elif vehicle == 'Truck':
                        sales_modifier *= 1.2  # Trucks sell well too
                    elif vehicle == 'Compact':
                        sales_modifier *= 0.7  # Compacts sell less
                    
                    # Region modifiers
                    if region == 'West':
                        sales_modifier *= 1.3  # West buys more cars
                    elif region == 'South':
                        sales_modifier *= 1.2  # South buys more cars
                    elif region == 'East':
                        sales_modifier *= 0.9  # East buys fewer cars
                    
                    # State population approximation modifier
                    if state in ['CA', 'TX', 'NY', 'FL']:
                        sales_modifier *= 2.0  # Big states have more sales
                    elif state in ['RI', 'DE', 'WY', 'VT']:
                        sales_modifier *= 0.3  # Small states have fewer sales
                    
                    # Gas price affects different vehicles differently
                    if row['gas_price'] > 3.5:
                        if vehicle in ['SUV', 'Truck']:
                            sales_modifier *= 0.85  # High gas prices affect large vehicles more
                        elif vehicle == 'Compact':
                            sales_modifier *= 1.1  # Compacts do better with high gas prices
                    
                    # Create new row with bounded random variation
                    new_row = row.copy()
                    
                    # Apply modifier with bounded random noise
                    base_sales = row['sales'] * sales_modifier
                    random_factor = np.random.uniform(0.8, 1.2)
                    final_sales = base_sales * random_factor
                    
                    # Clamp to realistic bounds
                    new_row['sales'] = clamp_value(final_sales, DATA_BOUNDS['sales']['min'], DATA_BOUNDS['sales']['max'])
                    new_row['vehicle_type'] = vehicle
                    new_row['region'] = region
                    new_row['state'] = state
                    
                    expanded_data.append(new_row)
    
    expanded_df = pd.DataFrame(expanded_data)
    
    # Add make and model information
    makes = {
        'Sedan': ['Toyota Camry', 'Honda Accord', 'Hyundai Elantra', 'Ford Fusion'],
        'SUV': ['Toyota RAV4', 'Honda CR-V', 'Ford Explorer', 'Chevy Tahoe'],
        'Truck': ['Ford F-150', 'Chevy Silverado', 'Ram 1500', 'Toyota Tundra'],
        'Compact': ['Toyota Corolla', 'Honda Civic', 'Hyundai Accent', 'Ford Focus']
    }
    
    # Add make and model
    make_model_data = []
    for _, row in expanded_df.iterrows():
        vehicle_type = row['vehicle_type']
        for make_model in makes[vehicle_type]:
            make = make_model.split()[0]
            model = " ".join(make_model.split()[1:])
            
            # Create variation by make/model
            sales_modifier = 1.0
            
            # Some makes are more popular
            if make in ['Toyota', 'Honda']:
                sales_modifier *= 1.2
            elif make in ['Ford', 'Chevy']:
                sales_modifier *= 1.1
                
            # Specific models adjustments
            if make_model in ['Toyota Camry', 'Honda Civic', 'Ford F-150']:
                sales_modifier *= 1.3  # Best sellers
            
            # Create new row with bounded random variation
            new_row = row.copy()
            
            # Apply modifier with bounded random noise
            base_sales = row['sales'] * sales_modifier
            random_factor = np.random.uniform(0.9, 1.1)
            final_sales = base_sales * random_factor
            
            # Clamp to realistic bounds
            new_row['sales'] = clamp_value(final_sales, DATA_BOUNDS['sales']['min'], DATA_BOUNDS['sales']['max'])
            new_row['make'] = make
            new_row['model'] = model
            
            make_model_data.append(new_row)
    
    final_df = pd.DataFrame(make_model_data)
    
    # Add years to model
    years = [2020, 2021, 2022, 2023]
    year_data = []
    
    for _, row in final_df.iterrows():
        for year in years:
            # Sales decline with age
            sales_modifier = 1.0
            age = 2024 - year
            sales_modifier *= (1.0 - (age * 0.15))  # Reduce sales by 15% per year of age
            
            # Create new row with bounded random variation
            new_row = row.copy()
            
            # Apply modifier with bounded random noise
            base_sales = row['sales'] * sales_modifier
            random_factor = np.random.uniform(0.9, 1.1)
            final_sales = base_sales * random_factor
            
            # Clamp to realistic bounds
            new_row['sales'] = clamp_value(final_sales, DATA_BOUNDS['sales']['min'], DATA_BOUNDS['sales']['max'])
            new_row['model_year'] = year
            
            year_data.append(new_row)
    
    complete_df = pd.DataFrame(year_data)
    
    # Add data quality logging
    logger.info(f"Generated synthetic dataset with {len(complete_df)} records")
    logger.debug(f"Sales range: {complete_df['sales'].min():.0f} - {complete_df['sales'].max():.0f}")
    logger.debug(f"Unemployment range: {complete_df['unemployment'].min():.2f}% - {complete_df['unemployment'].max():.2f}%")
    logger.debug(f"Gas price range: ${complete_df['gas_price'].min():.2f} - ${complete_df['gas_price'].max():.2f}")
    
    # Save to CSV if data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    csv_path = os.path.join(data_dir, f'synthetic_car_sales_seed_{seed}.csv')
    complete_df.to_csv(csv_path, index=False)
    logger.info(f"Saved synthetic data to {csv_path}")
    
    return complete_df


def load_data(seed: Optional[int] = None, force_regenerate: bool = False) -> pd.DataFrame:
    """
    Load data from CSV file if it exists, otherwise generate sample data.
    
    Args:
        seed: Random seed for reproducible data generation
        force_regenerate: If True, regenerate data even if CSV exists
    
    Returns:
        pd.DataFrame: A DataFrame with car sales data
    """
    if seed is None:
        seed = DEFAULT_SEED
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    csv_path = os.path.join(data_dir, f'synthetic_car_sales_seed_{seed}.csv')
    
    # Load existing data if available and not forcing regeneration
    if os.path.exists(csv_path) and not force_regenerate:
        logger.info(f"Loading existing synthetic data from {csv_path}")
        df = pd.read_csv(csv_path, parse_dates=['date'])
        
        # Validate data bounds
        sales_min, sales_max = df['sales'].min(), df['sales'].max()
        if sales_min < DATA_BOUNDS['sales']['min'] or sales_max > DATA_BOUNDS['sales']['max']:
            logger.warning(f"Existing data has sales outside bounds ({sales_min:.0f}-{sales_max:.0f}), regenerating...")
            return generate_sample_data(seed)
            
        return df
    else:
        logger.info(f"Generating new synthetic data with seed {seed}")
        return generate_sample_data(seed)