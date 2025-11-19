#!/usr/bin/env python3
"""
Tokyo Weather & Time CLI entry point.

This module provides a command-line interface to display Tokyo's current time
and weather information. Run with: python -m tokyoweather
"""

import os
import sys
from dotenv import load_dotenv
from .weather import fetch_weather, WeatherAPIError
from .time_utils import format_jst_time


def main():
    """
    Main CLI function to display Tokyo time and weather.
    
    Exit codes:
        0: Success
        1: Configuration error (missing API key)
        2: Network/API failure
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Display current JST time
    print(f"Tokyo Time: {format_jst_time()}")
    
    # Get API key from environment
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("ERROR: OPENWEATHER_API_KEY environment variable not set.", file=sys.stderr)
        print("Please set your API key:", file=sys.stderr)
        print("  export OPENWEATHER_API_KEY=your_api_key_here", file=sys.stderr)
        return 1
    
    # Fetch and display weather data
    try:
        weather_data = fetch_weather(api_key=api_key)
        print(weather_data)
        return 0
    except WeatherAPIError as e:
        print(f"ERROR: Failed to fetch weather data: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
