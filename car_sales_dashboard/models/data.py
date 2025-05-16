import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    """
    Generate synthetic car sales data with exogenous factors.
    
    Returns:
        pd.DataFrame: A DataFrame with synthetic sales data
    """
    # Define date range
    start_date = datetime(2015, 1, 1)
    dates = [start_date + timedelta(days=30*i) for i in range(36)]
    
    # Create base data
    data = {
        'date': dates,
        'year': [d.year for d in dates],
        'month': [d.month for d in dates],
        'sales': np.random.normal(15000, 3000, 36),  # Random sales data
        'unemployment': np.random.uniform(3.5, 7.5, 36),
        'gas_price': np.random.uniform(2.0, 4.5, 36),
        'cpi_energy': np.random.uniform(180, 250, 36),
        'cpi_all': np.random.uniform(220, 280, 36),
        'search_volume': np.random.uniform(40, 100, 36)
    }
    
    # Add seasonal effect
    for i, month in enumerate(data['month']):
        # Higher sales in spring and end of year
        if month in [3, 4, 5, 11, 12]:
            data['sales'][i] *= 1.2
        # Lower sales in winter
        elif month in [1, 2]:
            data['sales'][i] *= 0.8
            
        # Gas price effects
        if data['gas_price'][i] > 3.5:
            data['sales'][i] *= 0.9  # High gas prices reduce sales
            
        # Unemployment effects
        if data['unemployment'][i] > 6.0:
            data['sales'][i] *= 0.85  # High unemployment reduces sales
    
    df = pd.DataFrame(data)
    
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
                    
                    # Create new row
                    new_row = row.copy()
                    new_row['sales'] = row['sales'] * sales_modifier * np.random.uniform(0.8, 1.2)
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
            
            # Create new row
            new_row = row.copy()
            new_row['sales'] = row['sales'] * sales_modifier * np.random.uniform(0.9, 1.1)
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
            
            # Create new row
            new_row = row.copy()
            new_row['sales'] = row['sales'] * sales_modifier * np.random.uniform(0.9, 1.1)
            new_row['model_year'] = year
            
            year_data.append(new_row)
    
    complete_df = pd.DataFrame(year_data)
    
    # Save to CSV if data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    csv_path = os.path.join(data_dir, 'synthetic_car_sales.csv')
    complete_df.to_csv(csv_path, index=False)
    
    return complete_df


def load_data():
    """
    Load data from CSV file if it exists, otherwise generate sample data.
    
    Returns:
        pd.DataFrame: A DataFrame with car sales data
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    csv_path = os.path.join(data_dir, 'synthetic_car_sales.csv')
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path, parse_dates=['date'])
    else:
        return generate_sample_data()