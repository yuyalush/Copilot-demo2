#!/usr/bin/env python3
"""
Demo script for tokyoweather modules.
This shows how to use the weather and time utilities.
"""

import os
from tokyoweather.weather import fetch_weather, WeatherAPIError
from tokyoweather.time_utils import format_jst_time


def main():
    """Demonstrate weather and time module usage."""
    
    # Display current JST time
    print("=" * 50)
    print("Tokyo Time & Weather Information")
    print("=" * 50)
    print(f"Tokyo Time: {format_jst_time()}")
    print()
    
    # Try to fetch weather data
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("ERROR: OPENWEATHER_API_KEY environment variable not set.")
        print("Please set it to fetch weather data:")
        print("  export OPENWEATHER_API_KEY=your_api_key_here")
        return 1
    
    try:
        weather_data = fetch_weather(api_key=api_key)
        print(weather_data)
        print("=" * 50)
        return 0
    except WeatherAPIError as e:
        print(f"ERROR: Failed to fetch weather data: {e}")
        return 2


if __name__ == "__main__":
    exit(main())
