"""
Datetime utilities for timezone conversion and formatting.
"""

from datetime import datetime, timezone

def utc_to_local_string(utc_datetime_str, format_str="%Y-%m-%d %H:%M"):
    """
    Convert UTC datetime string to local timezone string.
    
    Args:
        utc_datetime_str: UTC datetime string (ISO format)
        format_str: Output format string
        
    Returns:
        Formatted local datetime string
    """
    if not utc_datetime_str:
        return 'N/A'
    
    try:
        # Parse the UTC datetime string
        if 'T' in utc_datetime_str:
            # Full ISO format with T separator
            utc_dt = datetime.fromisoformat(utc_datetime_str.replace('Z', '+00:00'))
        else:
            # Space-separated format from database
            utc_dt = datetime.fromisoformat(utc_datetime_str + '+00:00')
        
        # Ensure it's UTC
        if utc_dt.tzinfo is None:
            utc_dt = utc_dt.replace(tzinfo=timezone.utc)
        elif utc_dt.tzinfo != timezone.utc:
            utc_dt = utc_dt.astimezone(timezone.utc)
        
        # Convert to local timezone (system timezone)
        local_dt = utc_dt.astimezone()
        
        return local_dt.strftime(format_str)
        
    except (ValueError, TypeError) as e:
        print(f"Error converting datetime {utc_datetime_str}: {e}")
        return utc_datetime_str[:16] if len(utc_datetime_str) >= 16 else utc_datetime_str


def utc_to_local_date_string(utc_datetime_str):
    """
    Convert UTC datetime string to local date string (YYYY-MM-DD).
    
    Args:
        utc_datetime_str: UTC datetime string
        
    Returns:
        Local date string in YYYY-MM-DD format
    """
    return utc_to_local_string(utc_datetime_str, "%Y-%m-%d")


def get_local_today():
    """
    Get today's date in local timezone.
    
    Returns:
        Today's date string in YYYY-MM-DD format (local timezone)
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_utc_today():
    """
    Get today's date in UTC timezone.
    
    Returns:
        Today's date string in YYYY-MM-DD format (UTC timezone)
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def is_same_local_date(utc_datetime_str, local_date_str):
    """
    Check if a UTC datetime falls on the same local date.
    
    Args:
        utc_datetime_str: UTC datetime string
        local_date_str: Local date string (YYYY-MM-DD)
        
    Returns:
        Boolean indicating if they're the same local date
    """
    try:
        local_date_from_utc = utc_to_local_date_string(utc_datetime_str)
        return local_date_from_utc == local_date_str
    except:
        return False
