# Tokyo Weather & Time CLI

A lightweight Python command-line interface (CLI) tool that prints the current local time in Tokyo (JST) and the latest weather conditions retrieved from a public weather API.

---
## Features
- Display current Tokyo time (JST)
- Fetch current weather (temperature, condition, humidity, etc.) via a weather API (e.g. OpenWeatherMap)
- Clean, human-readable default output
- JSON output mode (planned)
- Graceful error handling (network/API/environment variable issues)
- Tested with `pytest`
- Extensible modular design (`weather.py`, `time_utils.py`, `cli.py` etc.)

---
## Requirements
- Python: >= 3.10 (recommended)
- Dependencies:
  - `requests`
  - `python-dotenv` (optional, for local development convenience)
  - `pytest` (development/testing)

Install dependencies (after creating a virtual environment):
```bash
pip install -r requirements.txt
```
(If `requirements.txt` is not yet present, it will be added in future commits.)

---
## Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/yuyalush/Copilot-demo2.git
cd Copilot-demo2
```

### Step 2: Set Up Virtual Environment
**Recommended: Using venv (built-in)**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# On Windows:
# .venv\Scripts\activate
```

**Alternative: Using Poetry**
```bash
poetry shell
```

### Step 3: Install Dependencies
**Using pip (Recommended):**
```bash
pip install -r requirements.txt
```

**Using Poetry:**
```bash
poetry install
```

> **Note:** If `requirements.txt` is not yet present, it will be added in future commits.

---
## Environment Variables
The tool requires an API key for the weather provider. Set it before running the CLI.

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | API key for OpenWeatherMap (or chosen provider) | `export OPENWEATHER_API_KEY=your_key_here` |

### Setting Up Environment Variables

**Method 1: Export directly (temporary)**
```bash
export OPENWEATHER_API_KEY=your_actual_api_key_here
```

**Method 2: Using .env file (recommended for development)**

1. Copy the example file to create your `.env` file:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your actual API key:
```bash
# Open .env in your editor and replace 'your_api_key_here' with your actual key
# Or use this command:
echo "OPENWEATHER_API_KEY=your_actual_api_key_here" > .env
```

3. The CLI will automatically load the `.env` file via `python-dotenv` if present.

**Important Notes:**
- Never commit `.env` files to version control (already in `.gitignore`)
- Get your API key from [OpenWeatherMap](https://openweathermap.org/api)
- If the key is missing, the CLI prints a clear error message and exits with a non-zero status

---
## Usage
After installation and environment variable setup:
```bash
python -m tokyoweather
```
Or if an entry point script `tokyoweather` is provided (planned):
```bash
tokyoweather
```
### Example Output
```
Tokyo Time: 2025-11-19 15:42:07 JST
Weather: Clear sky
Temperature: 18.2 °C
Humidity: 55 %
Wind: 3.4 m/s
```

### (Planned) Options
| Flag | Description |
|------|-------------|
| `--json` | Output raw JSON from the API plus derived time info |
| `--units metric|imperial` | Override units (default: metric) |
| `--raw` | Show unformatted API payload |

(These flags will be added incrementally; initial MVP may start without them.)

### Error Handling Examples
- Missing API key → prints: `ERROR: OPENWEATHER_API_KEY not set.`
- Network issue → prints: `ERROR: Failed to reach weather service (details...)`
- Invalid response → prints: `ERROR: Unexpected API response format.`

Exit codes:
- `0` success
- `1` configuration error (e.g. missing API key)
- `2` network/API failure

---
## Project Structure (Planned)
```
Copilot-demo2/
├── tokyoweather/
│   ├── __init__.py
│   ├── cli.py              # Argument parsing / main entry
│   ├── weather.py          # Weather API client logic
│   ├── time_utils.py       # JST time helpers
│   └── models.py           # (Optional) Data classes for responses
├── tests/
│   ├── test_weather.py
│   ├── test_time_utils.py
│   └── test_cli.py
├── README.md
├── requirements.txt (or pyproject.toml)
└── .env (excluded from version control / sample via .env.example)
```

---
## Testing
### Running Tests
Run all tests with `pytest`:
```bash
pytest -v
```

Run tests with coverage report:
```bash
pytest --cov=tokyoweather --cov-report=term-missing
```

Run specific test file:
```bash
pytest tests/test_weather.py -v
```

Run tests matching a pattern:
```bash
pytest -k "test_fetch_weather" -v
```

### Test Structure
Tests use `pytest` with mocking for external API calls to ensure reliability without actual network requests.

### Mocking External Calls
Use `pytest` + `unittest.mock` or `responses` library to mock HTTP calls:
```python
# Example snippet for test_weather.py
from unittest.mock import patch
from tokyoweather.weather import fetch_weather

@patch("tokyoweather.weather.requests.get")
def test_fetch_weather_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 18.2, "humidity": 55},
        "wind": {"speed": 3.4}
    }
    data = fetch_weather(api_key="dummy", city="Tokyo")
    assert data.temperature == 18.2
```

---
## Development Workflow
1. Create feature branch: `git checkout -b feature/cli-basic`
2. Implement / update code
3. Add or update tests
4. Run `pytest`
5. Commit & push
6. Open Pull Request referencing relevant Issues (see epic & child issues already drafted)

---
## Contribution Guidelines
We welcome contributions!
- Open an Issue before large changes
- Keep PRs focused & small
- Follow existing code style (PEP 8)
- Add tests for new logic
- Ensure CI (if added later) passes
- Do not commit secrets—use environment variables

### Reporting Bugs
Please include:
- CLI command used
- Full error output
- Environment (OS, Python version)

### Suggesting Features
Open an Issue with the label `enhancement` describing:
- Use case
- Proposed interface / flags
- Example output

---
## Security
- Never commit `.env` or actual API keys.
- Consider adding rate limiting / retries for production-grade usage.

---
## Roadmap (High-Level)
- [x] Draft Issues (epic + tasks)
- [ ] Implement base weather/time modules
- [ ] Implement CLI bootstrap
- [ ] Add argparse and basic flags
- [ ] JSON output mode
- [ ] Test coverage >80%
- [ ] Publish package to PyPI (optional)

---
## License
MIT License (unless the repository chooses a different one). If a `LICENSE` file is not yet present, one will be added in a future commit.

---
## Acknowledgements
- OpenWeatherMap (or selected weather API provider)
- Python community & open source libraries

---
## Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError` when running the CLI**
- **Solution:** Ensure you've activated your virtual environment and installed dependencies:
  ```bash
  source .venv/bin/activate  # or .venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```

**Issue: API key error despite setting environment variable**
- **Solution:** 
  1. Check if the variable is set: `echo $OPENWEATHER_API_KEY` (Linux/Mac) or `echo %OPENWEATHER_API_KEY%` (Windows)
  2. If using `.env`, ensure the file is in the project root directory
  3. Restart your terminal or re-activate the virtual environment

**Issue: Network/connection errors**
- **Solution:**
  1. Check your internet connection
  2. Verify the API key is valid by testing it at OpenWeatherMap
  3. Check if your firewall is blocking requests to `api.openweathermap.org`

**Issue: Tests fail to run**
- **Solution:**
  1. Ensure `pytest` is installed: `pip install pytest`
  2. Run from the project root directory
  3. Check that test files are in the `tests/` directory

**Issue: Permission denied when creating virtual environment**
- **Solution:** 
  - On Linux/Mac: You may need to use `python3` instead of `python`
  - On Windows: Run your terminal as administrator if needed

---
## FAQ
**Q: Why only Tokyo?**  
A: MVP scope. Later we can generalize to arbitrary city input.

**Q: Can I use another weather provider?**  
A: Yes. Abstract the fetch logic in `weather.py` and add adapters.

**Q: How do I change units?**  
A: Planned `--units` flag; currently defaults to metric.

**Q: What Python version is required?**  
A: Python 3.10 or higher is recommended. Check your version with `python --version`.

**Q: The CLI shows "API key not set" - what should I do?**  
A: Ensure you've set the `OPENWEATHER_API_KEY` environment variable or created a `.env` file with your API key. See the [Environment Variables](#environment-variables) section.

**Q: How do I get an OpenWeatherMap API key?**  
A: Sign up at [OpenWeatherMap](https://openweathermap.org/api) and create a free API key. The free tier is sufficient for this tool.

**Q: Tests are failing with network errors - is this normal?**  
A: Tests should use mocked API calls and not require network access. If you see network errors, ensure tests are properly mocking external calls.

**Q: Can I run this tool without installing it?**  
A: Yes, after activating your virtual environment and installing dependencies, run: `python -m tokyoweather`

**Q: Where can I report bugs or suggest features?**  
A: Open an issue on the GitHub repository with detailed information about the problem or enhancement.

---
## Maintainers
Initial setup by project contributors. Feel free to open Issues to join.

---
## Disclaimer
This project is an MVP and may evolve rapidly. Use responsibly.
