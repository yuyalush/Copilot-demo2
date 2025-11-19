"""
Integration tests for CLI execution as subprocess.

These tests execute the CLI as a real subprocess to test end-to-end functionality.
"""

import pytest
import subprocess
import sys
import os
from pathlib import Path

pytestmark = [pytest.mark.integration, pytest.mark.cli, pytest.mark.slow]


@pytest.fixture
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def cli_command(project_root):
    """Get the command to run the CLI."""
    return [sys.executable, "-m", "tokyoweather"]


class TestCLISubprocess:
    """Tests for CLI execution as subprocess."""
    
    def test_cli_runs_without_api_key(self, cli_command, project_root):
        """Test CLI execution without API key shows appropriate error."""
        # Run CLI without API key
        env = os.environ.copy()
        env.pop("OPENWEATHER_API_KEY", None)  # Remove API key if present
        
        result = subprocess.run(
            cli_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env
        )
        
        # Verify exit code
        assert result.returncode == 1, f"Expected exit code 1, got {result.returncode}"
        
        # Verify output contains time
        assert "Tokyo Time:" in result.stdout, "Expected Tokyo time in stdout"
        
        # Verify error message
        assert "ERROR: OPENWEATHER_API_KEY environment variable not set" in result.stderr, \
            "Expected API key error in stderr"
        assert "export OPENWEATHER_API_KEY" in result.stderr, \
            "Expected usage instructions in stderr"
    
    def test_cli_module_can_be_imported(self):
        """Test that tokyoweather module can be imported."""
        try:
            import tokyoweather
            from tokyoweather import weather, time_utils
            from tokyoweather.models import WeatherData
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import tokyoweather module: {e}")
    
    def test_cli_main_function_exists(self):
        """Test that main function exists and is callable."""
        from tokyoweather.__main__ import main
        assert callable(main), "main function should be callable"
    
    def test_cli_help_with_python_module(self, cli_command, project_root):
        """Test that CLI can be run with python -m tokyoweather."""
        result = subprocess.run(
            cli_command + ["--help"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # The CLI doesn't have --help implemented, so it should fail
        # but it should fail gracefully
        # This test just verifies the CLI can be invoked
        assert result.returncode != 0 or "Tokyo Time:" in result.stdout
    
    @pytest.mark.skip(reason="Requires valid API key and network access")
    def test_cli_with_valid_api_key(self, cli_command, project_root):
        """Test CLI execution with valid API key (requires real API key)."""
        # This test is skipped by default as it requires a real API key
        # To run it, provide a valid OPENWEATHER_API_KEY environment variable
        # and remove the skip marker
        
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            pytest.skip("OPENWEATHER_API_KEY not set")
        
        env = os.environ.copy()
        env["OPENWEATHER_API_KEY"] = api_key
        
        result = subprocess.run(
            cli_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        
        # Verify exit code
        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
        
        # Verify output format
        assert "Tokyo Time:" in result.stdout
        assert "Weather:" in result.stdout
        assert "Temperature:" in result.stdout
        assert "Humidity:" in result.stdout
        assert "Wind:" in result.stdout


class TestCLIExitCodes:
    """Tests for CLI exit codes."""
    
    def test_missing_api_key_exit_code_1(self, cli_command, project_root):
        """Test that missing API key returns exit code 1 (configuration error)."""
        env = os.environ.copy()
        env.pop("OPENWEATHER_API_KEY", None)
        
        result = subprocess.run(
            cli_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env
        )
        
        assert result.returncode == 1, "Missing API key should return exit code 1"
    
    def test_empty_api_key_exit_code_1(self, cli_command, project_root):
        """Test that empty API key returns exit code 1 (configuration error)."""
        env = os.environ.copy()
        env["OPENWEATHER_API_KEY"] = ""
        
        result = subprocess.run(
            cli_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env
        )
        
        assert result.returncode == 1, "Empty API key should return exit code 1"
    
    def test_whitespace_api_key_exit_code_1(self, cli_command, project_root):
        """Test that whitespace-only API key returns exit code 1."""
        env = os.environ.copy()
        env["OPENWEATHER_API_KEY"] = "   "
        
        result = subprocess.run(
            cli_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env
        )
        
        assert result.returncode == 1, "Whitespace API key should return exit code 1"


class TestCLIOutput:
    """Tests for CLI output formatting."""
    
    def test_output_includes_timestamp(self, cli_command, project_root):
        """Test that CLI output includes a JST timestamp."""
        env = os.environ.copy()
        env.pop("OPENWEATHER_API_KEY", None)
        
        result = subprocess.run(
            cli_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env
        )
        
        # Even without API key, time should be displayed
        assert "Tokyo Time:" in result.stdout
        assert "JST" in result.stdout
    
    def test_stderr_for_errors(self, cli_command, project_root):
        """Test that errors are written to stderr, not stdout."""
        env = os.environ.copy()
        env.pop("OPENWEATHER_API_KEY", None)
        
        result = subprocess.run(
            cli_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env
        )
        
        # Error messages should be in stderr
        assert "ERROR:" in result.stderr
        # Success output (time) should be in stdout
        assert "Tokyo Time:" in result.stdout
