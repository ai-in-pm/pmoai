"""Path utilities for PMOAI."""

import os
from pathlib import Path


def get_pmoai_home() -> str:
    """
    Get the PMOAI home directory.

    Returns:
        Path to the PMOAI home directory
    """
    pmoai_home = os.environ.get("PMOAI_HOME")
    if pmoai_home:
        return pmoai_home

    return os.path.join(str(Path.home()), ".pmoai")


def db_storage_path() -> str:
    """Get the path to the database storage directory.

    Returns:
        The path to the database storage directory.
    """
    db_dir = os.path.join(get_pmoai_home(), "db")
    os.makedirs(db_dir, exist_ok=True)
    return db_dir


def cache_storage_path() -> str:
    """
    Get the path to the cache storage directory.

    Returns:
        Path to the cache storage directory
    """
    cache_path = os.path.join(get_pmoai_home(), "cache")
    os.makedirs(cache_path, exist_ok=True)
    return cache_path


def logs_path() -> str:
    """
    Get the path to the logs directory.

    Returns:
        Path to the logs directory
    """
    logs_path = os.path.join(get_pmoai_home(), "logs")
    os.makedirs(logs_path, exist_ok=True)
    return logs_path
