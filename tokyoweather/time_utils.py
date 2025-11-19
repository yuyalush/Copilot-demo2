"""
Time utilities for handling JST (Japan Standard Time).
"""

from datetime import datetime, timezone, timedelta


def get_jst_time():
    """
    Get current time in JST (Japan Standard Time).
    
    Returns:
        datetime: Current datetime in JST timezone.
    """
    jst = timezone(timedelta(hours=9))
    return datetime.now(jst)


def format_jst_time(dt=None):
    """
    Format a datetime object as JST time string.
    
    Args:
        dt (datetime, optional): Datetime object to format. 
                                 If None, uses current JST time.
    
    Returns:
        str: Formatted time string in "YYYY-MM-DD HH:MM:SS JST" format.
    """
    if dt is None:
        dt = get_jst_time()
    return dt.strftime("%Y-%m-%d %H:%M:%S JST")
