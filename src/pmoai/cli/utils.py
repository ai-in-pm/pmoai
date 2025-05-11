"""Utilities for the PMOAI CLI."""

import os
import re
from pathlib import Path
from typing import Dict, Optional


def load_env_vars(folder_path: Path) -> Dict[str, str]:
    """Load environment variables from a .env file.
    
    Args:
        folder_path: The path to the folder containing the .env file.
        
    Returns:
        A dictionary of environment variables.
    """
    env_vars = {}
    env_file = folder_path / ".env"
    
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars


def write_env_file(folder_path: Path, env_vars: Dict[str, str]) -> None:
    """Write environment variables to a .env file.
    
    Args:
        folder_path: The path to the folder to write the .env file to.
        env_vars: A dictionary of environment variables.
    """
    env_file = folder_path / ".env"
    
    with open(env_file, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")


def copy_template(src_file: Path, dst_file: Path, name: str, class_name: str, folder_name: str) -> None:
    """Copy a template file, replacing placeholders.
    
    Args:
        src_file: The source template file.
        dst_file: The destination file.
        name: The name of the crew.
        class_name: The class name of the crew.
        folder_name: The folder name of the crew.
    """
    if not src_file.exists():
        return
    
    # Create parent directories if they don't exist
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(src_file, "r") as f:
        content = f.read()
    
    # Replace placeholders
    content = content.replace("{{name}}", name)
    content = content.replace("{{class_name}}", class_name)
    content = content.replace("{{folder_name}}", folder_name)
    content = content.replace("{{crew_name}}", class_name)
    
    with open(dst_file, "w") as f:
        f.write(content)


def get_project_root() -> Optional[Path]:
    """Get the root directory of the project.
    
    Returns:
        The root directory of the project, or None if not found.
    """
    current_dir = Path.cwd()
    
    # Look for common project files
    project_files = ["pyproject.toml", "setup.py", ".git"]
    
    while current_dir != current_dir.parent:
        for file in project_files:
            if (current_dir / file).exists():
                return current_dir
        
        current_dir = current_dir.parent
    
    return None


def find_config_dir() -> Optional[Path]:
    """Find the configuration directory.
    
    Returns:
        The configuration directory, or None if not found.
    """
    # First, check if there's a config directory in the current directory
    current_dir = Path.cwd()
    config_dir = current_dir / "config"
    
    if config_dir.exists() and config_dir.is_dir():
        return config_dir
    
    # Then, check if there's a config directory in the project root
    project_root = get_project_root()
    if project_root:
        config_dir = project_root / "config"
        if config_dir.exists() and config_dir.is_dir():
            return config_dir
    
    # Finally, check if there's a config directory in the src directory
    if project_root:
        src_dir = project_root / "src"
        if src_dir.exists() and src_dir.is_dir():
            for path in src_dir.glob("**/config"):
                if path.is_dir():
                    return path
    
    return None


def camel_to_snake(name: str) -> str:
    """Convert a camel case string to snake case.
    
    Args:
        name: The camel case string.
        
    Returns:
        The snake case string.
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def snake_to_camel(name: str) -> str:
    """Convert a snake case string to camel case.
    
    Args:
        name: The snake case string.
        
    Returns:
        The camel case string.
    """
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])
