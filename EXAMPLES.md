# Example Usage

This document demonstrates how to use the tokyoweather modules.

## Time Utilities

```python
from tokyoweather.time_utils import get_jst_time, format_jst_time

# Get current JST time as datetime object
jst_time = get_jst_time()
print(jst_time)  # 2025-11-19 16:09:16.123456+09:00

# Format current JST time as string
formatted = format_jst_time()
print(formatted)  # 2025-11-19 16:09:16 JST

# Format a specific datetime
from datetime import datetime, timezone, timedelta
jst = timezone(timedelta(hours=9))
specific_time = datetime(2025, 11, 19, 15, 30, 0, tzinfo=jst)
print(format_jst_time(specific_time))  # 2025-11-19 15:30:00 JST
```

## Weather API

```python
import os
from tokyoweather.weather import fetch_weather, WeatherAPIError

# Get API key from environment variable
api_key = os.getenv("OPENWEATHER_API_KEY")

try:
    # Fetch weather for Tokyo (default)
    weather = fetch_weather(api_key=api_key)
    
    print(f"Weather: {weather.description}")
    print(f"Temperature: {weather.temperature} °C")
    print(f"Humidity: {weather.humidity} %")
    print(f"Wind Speed: {weather.wind_speed} m/s")
    
    # Or use the __str__ method
    print(weather)
    
except WeatherAPIError as e:
    print(f"Error: {e}")
```

### Fetch Weather for Other Cities

```python
# Fetch weather for Osaka
weather = fetch_weather(api_key=api_key, city="Osaka")

# Use imperial units (Fahrenheit, mph)
weather = fetch_weather(api_key=api_key, units="imperial")

# Custom timeout (default is 10 seconds)
weather = fetch_weather(api_key=api_key, timeout=30)
```

## Complete Example

```python
#!/usr/bin/env python3
import os
from tokyoweather.weather import fetch_weather, WeatherAPIError
from tokyoweather.time_utils import format_jst_time

def main():
    # Display current time
    print(f"Tokyo Time: {format_jst_time()}")
    
    # Fetch and display weather
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("ERROR: OPENWEATHER_API_KEY not set")
        return 1
    
    try:
        weather = fetch_weather(api_key=api_key)
        print(weather)
        return 0
    except WeatherAPIError as e:
        print(f"ERROR: {e}")
        return 2

if __name__ == "__main__":
    exit(main())
```

## Error Handling

The `fetch_weather` function raises `WeatherAPIError` for various failure scenarios:

- **Empty API key**: `"API key cannot be empty"`
- **Network timeout**: `"Request timed out after N seconds"`
- **Connection error**: `"Failed to connect to weather service"`
- **Invalid API key** (401): `"Invalid API key"`
- **City not found** (404): `"City 'X' not found"`
- **HTTP errors**: `"HTTP error: ..."`
- **Invalid response format**: `"Unexpected API response format: ..."`

## Testing

Run the tests:

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=tokyoweather --cov-report=term-missing

# Run specific test file
pytest tests/test_weather.py -v
```

## Data Models

The `WeatherData` class provides structured access to weather information:

```python
from tokyoweather.models import WeatherData

weather = WeatherData(
    description="clear sky",
    temperature=18.2,
    humidity=55,
    wind_speed=3.4,
    raw_data=None  # Optional: raw API response
)

# Access attributes
print(weather.description)   # "clear sky"
print(weather.temperature)   # 18.2
print(weather.humidity)      # 55
print(weather.wind_speed)    # 3.4

# String representation
print(weather)
# Output:
# Weather: clear sky
# Temperature: 18.2 °C
# Humidity: 55 %
# Wind: 3.4 m/s
```
