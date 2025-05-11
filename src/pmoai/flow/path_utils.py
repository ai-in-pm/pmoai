"""
Path utilities for flow visualization.
"""

import os
from pathlib import Path


def get_assets_path() -> str:
    """Get the path to the assets directory.

    Returns:
        The path to the assets directory.
    """
    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the assets directory
    assets_dir = os.path.join(current_dir, "assets")
    
    return assets_dir
