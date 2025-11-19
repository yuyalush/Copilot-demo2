# Testing Guide

This document describes the testing infrastructure for the Tokyo Weather & Time CLI project.

## Overview

The project uses **pytest** for all testing, with comprehensive unit tests, integration tests, and subprocess-based tests. Test coverage is maintained at 99%+ for all production code.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── test_weather.py                # Unit tests for weather API module
├── test_time_utils.py             # Unit tests for time utilities
├── test_cli.py                    # Integration tests for CLI main function
└── test_cli_integration.py        # Subprocess-based integration tests
```

## Test Categories

Tests are organized using pytest markers:

- **`@pytest.mark.unit`**: Unit tests that test individual functions in isolation
- **`@pytest.mark.integration`**: Integration tests that test multiple components together
- **`@pytest.mark.cli`**: Tests for CLI functionality
- **`@pytest.mark.api`**: Tests that involve API interactions (mocked)
- **`@pytest.mark.slow`**: Tests that take longer to run

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_weather.py
```

### Run Specific Test Class or Function
```bash
pytest tests/test_weather.py::TestFetchWeather
pytest tests/test_weather.py::TestFetchWeather::test_fetch_weather_success
```

### Run Tests by Marker
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only CLI tests
pytest -m cli

# Run all except slow tests
pytest -m "not slow"
```

### Run Tests Matching Pattern
```bash
# Run all tests with "timeout" in the name
pytest -k timeout

# Run all tests with "api" in the name
pytest -k api
```

## Code Coverage

### Generate Coverage Report
```bash
pytest --cov=tokyoweather --cov-report=term-missing
```

### Generate HTML Coverage Report
```bash
pytest --cov=tokyoweather --cov-report=html
```

This creates a `htmlcov/` directory. Open `htmlcov/index.html` in a browser to view the detailed coverage report.

### Coverage Configuration
Coverage is configured in `pytest.ini` to:
- Include only the `tokyoweather` package
- Exclude test files and cache directories
- Show missing lines in coverage report

## Test Details

### Unit Tests: Weather Module (`test_weather.py`)

**Tests for `_parse_weather_response()`:**
- ✅ Valid API response parsing
- ✅ Value rounding (temperature, wind speed)
- ✅ Missing required fields
- ✅ Empty weather list
- ✅ Invalid data types

**Tests for `fetch_weather()`:**
- ✅ Successful weather fetch
- ✅ Custom city parameter
- ✅ Custom units parameter
- ✅ Custom timeout parameter
- ✅ Empty API key validation
- ✅ Network timeout error
- ✅ Connection error
- ✅ HTTP 401 (invalid API key)
- ✅ HTTP 404 (city not found)
- ✅ HTTP 500 (server error)
- ✅ General request exceptions

**Mocking Strategy:**
- All external API calls are mocked using `unittest.mock`
- No actual network requests are made during tests
- Mock responses simulate various API conditions

### Unit Tests: Time Utils Module (`test_time_utils.py`)

**Tests for `get_jst_time()`:**
- ✅ Returns datetime object
- ✅ Correct timezone (JST/UTC+9)
- ✅ Returns current time

**Tests for `format_jst_time()`:**
- ✅ Default argument (current time)
- ✅ Custom datetime argument
- ✅ Correct format: "YYYY-MM-DD HH:MM:SS JST"
- ✅ Various times (midnight, noon, late evening)

### Integration Tests: CLI Module (`test_cli.py`)

**Tests for `main()` function:**
- ✅ Successful execution with valid API key
- ✅ Missing API key (exit code 1)
- ✅ Empty API key string
- ✅ Whitespace-only API key
- ✅ Weather API errors (exit code 2)
- ✅ Invalid API key error
- ✅ Network timeout error
- ✅ City not found error
- ✅ Environment variable loading
- ✅ Output formatting

**Mocking Strategy:**
- `fetch_weather()` is mocked to simulate various conditions
- `format_jst_time()` is mocked for consistent test output
- Environment variables are patched using `@patch.dict()`
- Output is captured using pytest's `capsys` fixture

### Integration Tests: CLI Subprocess (`test_cli_integration.py`)

**Tests for subprocess execution:**
- ✅ CLI runs without API key (proper error)
- ✅ Module can be imported
- ✅ Main function exists and is callable
- ✅ Exit code 1 for missing API key
- ✅ Exit code 1 for empty API key
- ✅ Exit code 1 for whitespace-only API key
- ✅ Output includes JST timestamp
- ✅ Errors written to stderr
- ✅ Success output written to stdout

**Skipped Tests:**
- ⏭️ CLI with valid API key (requires network and real API key)

To run this test, set a valid `OPENWEATHER_API_KEY` environment variable and remove the skip marker:
```bash
OPENWEATHER_API_KEY=your_key pytest tests/test_cli_integration.py::TestCLISubprocess::test_cli_with_valid_api_key -v
```

## Writing New Tests

### Test Naming Conventions
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Unit Test
```python
import pytest
from tokyoweather.weather import fetch_weather, WeatherAPIError

@pytest.mark.unit
def test_fetch_weather_empty_api_key():
    """Test that empty API key raises WeatherAPIError."""
    with pytest.raises(WeatherAPIError) as exc_info:
        fetch_weather(api_key="")
    assert "API key cannot be empty" in str(exc_info.value)
```

### Example Integration Test
```python
import pytest
from unittest.mock import patch
from tokyoweather.__main__ import main

@pytest.mark.integration
@patch("tokyoweather.__main__.fetch_weather")
@patch("tokyoweather.__main__.format_jst_time")
@patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test_key"})
def test_main_success(mock_format_time, mock_fetch, capsys):
    """Test main function with successful execution."""
    mock_format_time.return_value = "2025-11-19 15:42:07 JST"
    mock_fetch.return_value = sample_weather_data
    
    exit_code = main()
    
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Tokyo Time:" in captured.out
```

### Mocking Guidelines
1. **Mock external dependencies**: Always mock API calls, file I/O, and network requests
2. **Use fixtures**: Create reusable fixtures for common test data
3. **Patch at the right level**: Patch where the function is used, not where it's defined
4. **Verify mock calls**: Use `assert_called_once()`, `assert_called_with()`, etc.

## Continuous Integration

### Local CI Simulation
Run the same checks that CI would run:
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest -v

# Check coverage
pytest --cov=tokyoweather --cov-report=term-missing

# Ensure coverage is above threshold
pytest --cov=tokyoweather --cov-fail-under=95
```

### Pre-commit Checklist
Before committing code, ensure:
- [ ] All tests pass: `pytest`
- [ ] Coverage is maintained: `pytest --cov=tokyoweather`
- [ ] No new linting errors (if linter is configured)
- [ ] New features have corresponding tests
- [ ] Test names are descriptive

## Troubleshooting

### Issue: Tests fail with `ModuleNotFoundError`
**Solution:** Ensure you're running tests from the project root directory and dependencies are installed:
```bash
cd /path/to/Copilot-demo2
pip install -r requirements.txt
pytest
```

### Issue: Import errors in tests
**Solution:** Check that `pytest.ini` includes `pythonpath = .` to add the current directory to Python path.

### Issue: Mocked tests still making network requests
**Solution:** Ensure you're patching at the correct location. Patch where the function is imported, not where it's defined:
```python
# Correct
@patch("tokyoweather.weather.requests.get")

# Incorrect (if imported as `from tokyoweather.weather import fetch_weather`)
@patch("requests.get")
```

### Issue: Tests pass locally but fail in CI
**Solution:** Check for:
- Environment variable differences
- File path assumptions (use `Path` from `pathlib`)
- Timezone differences (tests should use explicit timezones)
- Python version differences

## Test Maintenance

### When to Update Tests
- **Adding new features**: Write tests first (TDD) or immediately after
- **Fixing bugs**: Add a regression test that would have caught the bug
- **Refactoring code**: Ensure tests still pass; update if behavior changed
- **Changing APIs**: Update integration tests to match new interfaces

### Test Code Quality
- Keep tests simple and focused
- One assertion per test (generally)
- Use descriptive test names that explain what is being tested
- Add docstrings to explain complex test logic
- Avoid test interdependencies (each test should run independently)

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

## Test Statistics

As of the latest commit:
- **Total Tests**: 42 (32 original + 10 new integration tests)
- **Test Coverage**: 99%+ (83/84 statements)
- **Test Execution Time**: < 5 seconds
- **Mocked API Calls**: 100% (no real network requests)

---

For questions or issues with testing, please open an issue on the GitHub repository.
