"""
Weather API client for fetching Tokyo weather information.
"""

import requests
from typing import Optional
from .models import WeatherData


OPENWEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITY = "Tokyo"
DEFAULT_UNITS = "metric"  # Celsius for temperature, m/s for wind


class WeatherAPIError(Exception):
    """Exception raised for weather API related errors."""
    pass


def fetch_weather(
    api_key: str,
    city: str = DEFAULT_CITY,
    units: str = DEFAULT_UNITS,
    timeout: int = 10
) -> WeatherData:
    """
    Fetch current weather data from OpenWeatherMap API.
    
    Args:
        api_key: OpenWeatherMap API key
        city: City name (default: "Tokyo")
        units: Unit system - "metric", "imperial", or "standard" (default: "metric")
        timeout: Request timeout in seconds (default: 10)
    
    Returns:
        WeatherData: Structured weather information
    
    Raises:
        WeatherAPIError: If the API request fails or returns invalid data
    """
    if not api_key:
        raise WeatherAPIError("API key cannot be empty")
    
    params = {
        "q": city,
        "appid": api_key,
        "units": units
    }
    
    try:
        response = requests.get(
            OPENWEATHER_API_BASE_URL,
            params=params,
            timeout=timeout
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise WeatherAPIError(f"Request timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError:
        raise WeatherAPIError("Failed to connect to weather service")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise WeatherAPIError("Invalid API key")
        elif response.status_code == 404:
            raise WeatherAPIError(f"City '{city}' not found")
        else:
            raise WeatherAPIError(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        raise WeatherAPIError(f"Request failed: {e}")
    
    return _parse_weather_response(response.json())


def _parse_weather_response(data: dict) -> WeatherData:
    """
    Parse OpenWeatherMap API response into WeatherData object.
    
    Args:
        data: JSON response from OpenWeatherMap API
    
    Returns:
        WeatherData: Structured weather information
    
    Raises:
        WeatherAPIError: If the response format is unexpected
    """
    try:
        weather_list = data.get("weather", [])
        if not weather_list:
            raise KeyError("weather list is empty")
        
        description = weather_list[0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        return WeatherData(
            description=description,
            temperature=round(temperature, 1),
            humidity=humidity,
            wind_speed=round(wind_speed, 1),
            raw_data=data
        )
    except (KeyError, IndexError, TypeError) as e:
        raise WeatherAPIError(f"Unexpected API response format: {e}")
