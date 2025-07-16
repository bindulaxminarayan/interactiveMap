"""
Data processing utilities for the interactive map application.
"""

import re
import logging
import pandas as pd

def load_countries_data(file_path='data/countries.csv'):
    """Load and preprocess countries data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"--- Successfully loaded {file_path} ---")
        logging.info(f"Data contains {len(df)} rows.")
        
        # Convert GDP column to numeric
        df['gdp_numeric'] = df['gdp'].apply(convert_gdp_to_numeric)
        return df
        
    except FileNotFoundError:
        logging.error(f"!!! CRITICAL ERROR: File not found at '{file_path}'")
        logging.warn("!!! Please make sure the data file exists.")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def load_us_states_data(file_path='data/us.csv'):
    """Load and preprocess US states data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"--- Successfully loaded {file_path} ---")
        logging.info(f"Data contains {len(df)} rows.")
        return df
        
    except FileNotFoundError:
        logging.error(f"!!! CRITICAL ERROR: File not found at '{file_path}'")
        logging.warn("!!! Please make sure the data file exists.")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def load_world_physical_geography(file_path='data/world_physical_geography.csv'):
    """Load and preprocess US states data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"--- Successfully loaded {file_path} ---")
        logging.info(f"Data contains {len(df)} rows.")
        return df
        
    except FileNotFoundError:
        logging.error(f"!!! CRITICAL ERROR: File not found at '{file_path}'")
        logging.warn("!!! Please make sure the data file exists.")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def convert_gdp_to_numeric(gdp_str):
    """Convert GDP string format to numeric value in billions."""
    if pd.isna(gdp_str) or gdp_str == "No reliable data available":
        return 0
    
    # Remove $ and any extra spaces
    gdp_str = str(gdp_str).replace('$', '').replace(',', '').strip()
    
    # Extract number and unit
    pattern = r'([\d,.]+)\s*(Trillion|Billion|Million)?'
    match = re.search(pattern, gdp_str, re.IGNORECASE)
    
    if match:
        number_str = match.group(1).replace(',', '')
        unit = match.group(2)
        
        try:
            number = float(number_str)
            if unit and unit.lower() == 'trillion':
                return number * 1000  # Convert to billions
            elif unit and unit.lower() == 'million':
                return number / 1000  # Convert to billions
            else:  # Billion or no unit
                return number
        except ValueError:
            return 0
    return 0
