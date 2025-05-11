"""Create a flow."""

import shutil
import sys
from pathlib import Path

import click

from pmoai.cli.utils import copy_template


def create_folder_structure(name, parent_folder=None):
    """Create the folder structure for a flow.
    
    Args:
        name: The name of the flow.
        parent_folder: The parent folder to create the flow in.
        
    Returns:
        A tuple of (folder_path, folder_name, class_name).
    """
    folder_name = name.replace(" ", "_").replace("-", "_").lower()
    class_name = name.replace("_", " ").replace("-", " ").title().replace(" ", "")

    if parent_folder:
        folder_path = Path(parent_folder) / folder_name
    else:
        folder_path = Path(folder_name)

    if folder_path.exists():
        if not click.confirm(
            f"Folder {folder_name} already exists. Do you want to override it?"
        ):
            click.secho("Operation cancelled.", fg="yellow")
            sys.exit(0)
        click.secho(f"Overriding folder {folder_name}...", fg="green", bold=True)
        shutil.rmtree(folder_path)  # Delete the existing folder and its contents

    click.secho(
        f"Creating {'flow' if parent_folder else 'folder'} {folder_name}...",
        fg="green",
        bold=True,
    )

    folder_path.mkdir(parents=True)
    (folder_path / "tests").mkdir(exist_ok=True)
    if not parent_folder:
        (folder_path / "src" / folder_name).mkdir(parents=True)
        (folder_path / "src" / folder_name / "crews").mkdir(parents=True)

    return folder_path, folder_name, class_name


def create_flow(name, parent_folder=None):
    """Create a flow.
    
    Args:
        name: The name of the flow.
        parent_folder: The parent folder to create the flow in.
    """
    folder_path, folder_name, class_name = create_folder_structure(name, parent_folder)

    package_dir = Path(__file__).parent
    templates_dir = package_dir / "templates" / "flow"

    root_template_files = (
        [".gitignore", "pyproject.toml", "README.md"] if not parent_folder else []
    )
    src_template_files = (
        ["__init__.py", "main.py", "flow.py"] if not parent_folder else ["flow.py"]
    )

    for file_name in root_template_files:
        src_file = templates_dir / file_name
        dst_file = folder_path / file_name
        copy_template(src_file, dst_file, name, class_name, folder_name)

    src_folder = folder_path / "src" / folder_name if not parent_folder else folder_path

    for file_name in src_template_files:
        src_file = templates_dir / file_name
        dst_file = src_folder / file_name
        copy_template(src_file, dst_file, name, class_name, folder_name)

    click.secho(f"Flow {name} created successfully!", fg="green", bold=True)
