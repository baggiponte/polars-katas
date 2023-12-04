from typing import Optional
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
import os

def download_weather_data(start_date: str= '2023-01-01', end_date: str = '2023-11-27') -> Optional[pd.DataFrame]:
    # Coordinates for New York City
    latitude: float = 40.7128
    longitude: float = -74.0060

    # Setting up the API parameters
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': start_date,
        'end_date': end_date,
        "hourly": ["temperature_2m", "precipitation_probability", "precipitation"],
        # "daily": ["temperature_2m_max", "temperature_2m_min"],
        "timezone": "Europe/Berlin"
    }
    
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # API endpoint
    url = 'https://api.open-meteo.com/v1/forecast'
    
    try:
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
        
        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s"),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["precipitation"] = hourly_precipitation

        df = pd.DataFrame(data = hourly_data)
        print(df.shape)
        print(df.head())
        
        print("Weather data downloaded and saved to CSV successfully.")
        
        return df

    except Exception as e:
        print("An error occurred:", e)
        
        return None

# Run the function
if __name__ == "__main__":
    df = download_weather_data()
    
    # Define the path to save the file
    data_dir = os.path.join("..", "data", "weather")
    file_path = os.path.join(data_dir, "weather_data.csv")

    # Check if the directory exists, if not, create it
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Save the content to csv
    df.to_csv(file_path, sep=";", index=True)
    