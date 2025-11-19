"""
Unit tests for weather module.
"""

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.api]
from unittest.mock import patch, Mock
from copy import deepcopy
import requests
from tokyoweather.weather import (
    fetch_weather,
    _parse_weather_response,
    WeatherAPIError,
    OPENWEATHER_API_BASE_URL,
    DEFAULT_CITY
)
from tokyoweather.models import WeatherData


# Sample API response for testing
SAMPLE_API_RESPONSE = {
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "main": {
        "temp": 18.2,
        "feels_like": 17.5,
        "temp_min": 16.0,
        "temp_max": 20.0,
        "pressure": 1013,
        "humidity": 55
    },
    "wind": {
        "speed": 3.4,
        "deg": 180
    },
    "name": "Tokyo"
}


class TestParseWeatherResponse:
    """Tests for _parse_weather_response function."""
    
    def test_parse_valid_response(self):
        """Test parsing a valid API response."""
        result = _parse_weather_response(deepcopy(SAMPLE_API_RESPONSE))
        
        assert isinstance(result, WeatherData)
        assert result.description == "clear sky"
        assert result.temperature == 18.2
        assert result.humidity == 55
        assert result.wind_speed == 3.4
    
    def test_parse_rounds_values(self):
        """Test that temperature and wind speed are rounded."""
        data = deepcopy(SAMPLE_API_RESPONSE)
        data["main"]["temp"] = 18.256
        data["wind"]["speed"] = 3.456
        
        result = _parse_weather_response(data)
        
        assert result.temperature == 18.3
        assert result.wind_speed == 3.5
    
    def test_parse_missing_weather_field(self):
        """Test parsing fails when weather field is missing."""
        data = deepcopy(SAMPLE_API_RESPONSE)
        del data["weather"]
        
        with pytest.raises(WeatherAPIError) as exc_info:
            _parse_weather_response(data)
        assert "Unexpected API response format" in str(exc_info.value)
    
    def test_parse_empty_weather_list(self):
        """Test parsing fails when weather list is empty."""
        data = deepcopy(SAMPLE_API_RESPONSE)
        data["weather"] = []
        
        with pytest.raises(WeatherAPIError) as exc_info:
            _parse_weather_response(data)
        assert "weather list is empty" in str(exc_info.value)
    
    def test_parse_missing_main_field(self):
        """Test parsing fails when main field is missing."""
        data = deepcopy(SAMPLE_API_RESPONSE)
        del data["main"]
        
        with pytest.raises(WeatherAPIError) as exc_info:
            _parse_weather_response(data)
        assert "Unexpected API response format" in str(exc_info.value)
    
    def test_parse_missing_wind_field(self):
        """Test parsing fails when wind field is missing."""
        data = deepcopy(SAMPLE_API_RESPONSE)
        del data["wind"]
        
        with pytest.raises(WeatherAPIError) as exc_info:
            _parse_weather_response(data)
        assert "Unexpected API response format" in str(exc_info.value)


class TestFetchWeather:
    """Tests for fetch_weather function."""
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_success(self, mock_get):
        """Test successful weather fetch."""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        # Use deepcopy to avoid side effects from other tests
        mock_response.json.return_value = deepcopy(SAMPLE_API_RESPONSE)
        mock_get.return_value = mock_response
        
        # Call function
        result = fetch_weather(api_key="test_key")
        
        # Verify request was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][0] == OPENWEATHER_API_BASE_URL
        assert call_args[1]["params"]["q"] == DEFAULT_CITY
        assert call_args[1]["params"]["appid"] == "test_key"
        assert call_args[1]["params"]["units"] == "metric"
        
        # Verify result
        assert isinstance(result, WeatherData)
        assert result.description == "clear sky"
        assert result.temperature == 18.2
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_with_custom_city(self, mock_get):
        """Test fetch weather with custom city."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = deepcopy(SAMPLE_API_RESPONSE)
        mock_get.return_value = mock_response
        
        fetch_weather(api_key="test_key", city="Osaka")
        
        call_args = mock_get.call_args
        assert call_args[1]["params"]["q"] == "Osaka"
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_with_custom_units(self, mock_get):
        """Test fetch weather with custom units."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = deepcopy(SAMPLE_API_RESPONSE)
        mock_get.return_value = mock_response
        
        fetch_weather(api_key="test_key", units="imperial")
        
        call_args = mock_get.call_args
        assert call_args[1]["params"]["units"] == "imperial"
    
    def test_fetch_weather_empty_api_key(self):
        """Test fetch weather with empty API key."""
        with pytest.raises(WeatherAPIError) as exc_info:
            fetch_weather(api_key="")
        assert "API key cannot be empty" in str(exc_info.value)
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_timeout(self, mock_get):
        """Test fetch weather with timeout."""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(WeatherAPIError) as exc_info:
            fetch_weather(api_key="test_key")
        assert "timed out" in str(exc_info.value)
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_connection_error(self, mock_get):
        """Test fetch weather with connection error."""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        with pytest.raises(WeatherAPIError) as exc_info:
            fetch_weather(api_key="test_key")
        assert "Failed to connect" in str(exc_info.value)
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_invalid_api_key(self, mock_get):
        """Test fetch weather with invalid API key (401)."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        with pytest.raises(WeatherAPIError) as exc_info:
            fetch_weather(api_key="invalid_key")
        assert "Invalid API key" in str(exc_info.value)
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_city_not_found(self, mock_get):
        """Test fetch weather with city not found (404)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        with pytest.raises(WeatherAPIError) as exc_info:
            fetch_weather(api_key="test_key", city="InvalidCity")
        assert "not found" in str(exc_info.value)
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_http_error(self, mock_get):
        """Test fetch weather with general HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server Error")
        mock_get.return_value = mock_response
        
        with pytest.raises(WeatherAPIError) as exc_info:
            fetch_weather(api_key="test_key")
        assert "HTTP error" in str(exc_info.value)
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_request_exception(self, mock_get):
        """Test fetch weather with general request exception."""
        mock_get.side_effect = requests.exceptions.RequestException("Unknown error")
        
        with pytest.raises(WeatherAPIError) as exc_info:
            fetch_weather(api_key="test_key")
        assert "Request failed" in str(exc_info.value)
    
    @patch("tokyoweather.weather.requests.get")
    def test_fetch_weather_custom_timeout(self, mock_get):
        """Test fetch weather respects custom timeout parameter."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = deepcopy(SAMPLE_API_RESPONSE)
        mock_get.return_value = mock_response
        
        fetch_weather(api_key="test_key", timeout=30)
        
        call_args = mock_get.call_args
        assert call_args[1]["timeout"] == 30
