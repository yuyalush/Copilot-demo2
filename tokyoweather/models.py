"""
Data models for weather API responses.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherData:
    """
    Data class representing weather information.
    
    Attributes:
        description: Weather condition description (e.g., "clear sky", "light rain")
        temperature: Temperature in Celsius
        humidity: Humidity percentage
        wind_speed: Wind speed in m/s
        raw_data: Optional raw API response data
    """
    description: str
    temperature: float
    humidity: int
    wind_speed: float
    raw_data: Optional[dict] = None
    
    def __str__(self):
        """Human-readable string representation."""
        return (
            f"Weather: {self.description}\n"
            f"Temperature: {self.temperature} °C\n"
            f"Humidity: {self.humidity} %\n"
            f"Wind: {self.wind_speed} m/s"
        )
