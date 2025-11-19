"""
Unit tests for CLI main function.
"""

import pytest
from unittest.mock import patch, Mock
from copy import deepcopy
import sys
from tokyoweather.__main__ import main
from tokyoweather.weather import WeatherAPIError
from tokyoweather.models import WeatherData


# Sample weather data for testing
SAMPLE_WEATHER_DATA = WeatherData(
    description="clear sky",
    temperature=18.2,
    humidity=55,
    wind_speed=3.4
)


class TestCLIMain:
    """Tests for main CLI function."""
    
    @patch("tokyoweather.__main__.fetch_weather")
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test_key"})
    def test_main_success(self, mock_format_time, mock_fetch, capsys):
        """Test main function with successful execution."""
        # Setup mocks
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        mock_fetch.return_value = SAMPLE_WEATHER_DATA
        
        # Run main
        exit_code = main()
        
        # Verify exit code
        assert exit_code == 0
        
        # Verify fetch_weather was called
        mock_fetch.assert_called_once_with(api_key="test_key")
        
        # Verify output
        captured = capsys.readouterr()
        assert "Tokyo Time: 2025-11-19 15:42:07 JST" in captured.out
        assert "Weather: clear sky" in captured.out
        assert "Temperature: 18.2 °C" in captured.out
        assert "Humidity: 55 %" in captured.out
        assert "Wind: 3.4 m/s" in captured.out
    
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {}, clear=True)
    def test_main_missing_api_key(self, mock_format_time, capsys):
        """Test main function with missing API key."""
        # Setup mock
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        
        # Run main
        exit_code = main()
        
        # Verify exit code
        assert exit_code == 1
        
        # Verify output
        captured = capsys.readouterr()
        assert "Tokyo Time: 2025-11-19 15:42:07 JST" in captured.out
        assert "ERROR: OPENWEATHER_API_KEY environment variable not set" in captured.err
        assert "export OPENWEATHER_API_KEY" in captured.err
    
    @patch("tokyoweather.__main__.fetch_weather")
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test_key"})
    def test_main_weather_api_error(self, mock_format_time, mock_fetch, capsys):
        """Test main function with weather API error."""
        # Setup mocks
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        mock_fetch.side_effect = WeatherAPIError("Failed to connect to weather service")
        
        # Run main
        exit_code = main()
        
        # Verify exit code
        assert exit_code == 2
        
        # Verify output
        captured = capsys.readouterr()
        assert "Tokyo Time: 2025-11-19 15:42:07 JST" in captured.out
        assert "ERROR: Failed to fetch weather data" in captured.err
        assert "Failed to connect to weather service" in captured.err
    
    @patch("tokyoweather.__main__.fetch_weather")
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "invalid_key"})
    def test_main_invalid_api_key(self, mock_format_time, mock_fetch, capsys):
        """Test main function with invalid API key."""
        # Setup mocks
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        mock_fetch.side_effect = WeatherAPIError("Invalid API key")
        
        # Run main
        exit_code = main()
        
        # Verify exit code
        assert exit_code == 2
        
        # Verify output
        captured = capsys.readouterr()
        assert "Tokyo Time: 2025-11-19 15:42:07 JST" in captured.out
        assert "ERROR: Failed to fetch weather data" in captured.err
        assert "Invalid API key" in captured.err
    
    @patch("tokyoweather.__main__.fetch_weather")
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test_key"})
    def test_main_network_timeout(self, mock_format_time, mock_fetch, capsys):
        """Test main function with network timeout."""
        # Setup mocks
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        mock_fetch.side_effect = WeatherAPIError("Request timed out after 10 seconds")
        
        # Run main
        exit_code = main()
        
        # Verify exit code
        assert exit_code == 2
        
        # Verify output
        captured = capsys.readouterr()
        assert "Tokyo Time: 2025-11-19 15:42:07 JST" in captured.out
        assert "ERROR: Failed to fetch weather data" in captured.err
        assert "timed out" in captured.err
    
    @patch("tokyoweather.__main__.fetch_weather")
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test_key"})
    def test_main_city_not_found(self, mock_format_time, mock_fetch, capsys):
        """Test main function with city not found error."""
        # Setup mocks
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        mock_fetch.side_effect = WeatherAPIError("City 'Tokyo' not found")
        
        # Run main
        exit_code = main()
        
        # Verify exit code
        assert exit_code == 2
        
        # Verify output
        captured = capsys.readouterr()
        assert "Tokyo Time: 2025-11-19 15:42:07 JST" in captured.out
        assert "ERROR: Failed to fetch weather data" in captured.err
        assert "not found" in captured.err


class TestEnvironmentVariableHandling:
    """Tests for environment variable handling and security."""
    
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {}, clear=True)
    def test_missing_env_var_returns_exit_code_1(self, mock_format_time, capsys):
        """Test that missing API key returns exit code 1 (config error)."""
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        
        exit_code = main()
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "ERROR: OPENWEATHER_API_KEY environment variable not set" in captured.err
    
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": ""})
    def test_empty_env_var_returns_exit_code_1(self, mock_format_time, capsys):
        """Test that empty API key is treated as missing."""
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        
        exit_code = main()
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "ERROR: OPENWEATHER_API_KEY environment variable not set" in captured.err
    
    @patch("tokyoweather.__main__.fetch_weather")
    @patch("tokyoweather.__main__.format_jst_time")
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "   "})
    def test_whitespace_only_env_var_returns_exit_code_1(self, mock_format_time, mock_fetch, capsys):
        """Test that whitespace-only API key is treated as missing."""
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        
        exit_code = main()
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "ERROR: OPENWEATHER_API_KEY environment variable not set" in captured.err
    
    @patch("tokyoweather.__main__.fetch_weather")
    @patch("tokyoweather.__main__.format_jst_time")
    @patch("tokyoweather.__main__.load_dotenv")
    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "valid_key"})
    def test_dotenv_loaded_at_startup(self, mock_load_dotenv, mock_format_time, mock_fetch, capsys):
        """Test that load_dotenv is called to load .env file."""
        mock_format_time.return_value = "2025-11-19 15:42:07 JST"
        mock_fetch.return_value = SAMPLE_WEATHER_DATA
        
        main()
        
        # Verify load_dotenv was called
        mock_load_dotenv.assert_called_once()
