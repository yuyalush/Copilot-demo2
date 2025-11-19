"""
Unit tests for time_utils module.
"""

import pytest
from datetime import datetime, timezone, timedelta
from tokyoweather.time_utils import get_jst_time, format_jst_time


def test_get_jst_time():
    """Test that get_jst_time returns a datetime in JST timezone."""
    jst_time = get_jst_time()
    
    # Check that it returns a datetime object
    assert isinstance(jst_time, datetime)
    
    # Check that the timezone offset is +9 hours (JST)
    expected_offset = timedelta(hours=9)
    assert jst_time.utcoffset() == expected_offset


def test_get_jst_time_is_current():
    """Test that get_jst_time returns approximately current time."""
    before = datetime.now(timezone(timedelta(hours=9)))
    jst_time = get_jst_time()
    after = datetime.now(timezone(timedelta(hours=9)))
    
    # The returned time should be between before and after
    assert before <= jst_time <= after


def test_format_jst_time_with_no_argument():
    """Test format_jst_time with no argument uses current time."""
    formatted = format_jst_time()
    
    # Check format: "YYYY-MM-DD HH:MM:SS JST"
    assert " JST" in formatted
    assert len(formatted) == 23  # "2025-11-19 16:05:01 JST"
    
    # Verify it can be parsed back
    time_part = formatted.replace(" JST", "")
    datetime.strptime(time_part, "%Y-%m-%d %H:%M:%S")


def test_format_jst_time_with_datetime():
    """Test format_jst_time with a specific datetime."""
    jst = timezone(timedelta(hours=9))
    test_dt = datetime(2025, 11, 19, 15, 42, 7, tzinfo=jst)
    
    formatted = format_jst_time(test_dt)
    
    assert formatted == "2025-11-19 15:42:07 JST"


def test_format_jst_time_handles_different_times():
    """Test format_jst_time with various times."""
    jst = timezone(timedelta(hours=9))
    
    # Test midnight
    test_dt = datetime(2025, 1, 1, 0, 0, 0, tzinfo=jst)
    assert format_jst_time(test_dt) == "2025-01-01 00:00:00 JST"
    
    # Test noon
    test_dt = datetime(2025, 6, 15, 12, 30, 45, tzinfo=jst)
    assert format_jst_time(test_dt) == "2025-06-15 12:30:45 JST"
    
    # Test late evening
    test_dt = datetime(2025, 12, 31, 23, 59, 59, tzinfo=jst)
    assert format_jst_time(test_dt) == "2025-12-31 23:59:59 JST"
