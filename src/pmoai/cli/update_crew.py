import os
import re
import subprocess
from pathlib import Path

import click


def update_crew() -> None:
    """
    Update the pyproject.toml of the Crew project to use uv.
    """
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        click.echo("Error: pyproject.toml not found in the current directory.")
        return

    with open(pyproject_path, "r") as f:
        content = f.read()

    # Check if the pyproject.toml already has uv configuration
    if "[tool.uv]" in content:
        click.echo("The pyproject.toml already has uv configuration.")
        return

    # Add uv configuration
    uv_config = """
[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "isort>=5.0.0",
    "mypy>=1.0.0",
]

[tool.uv.scripts]
kickoff = "python -c \\"from flow import Flow; Flow().kickoff()\\"" 
plot = "python -c \\"from flow import Flow; Flow().plot()\\"" 
train = "python -c \\"import sys; from crew import Crew; Crew().train(int(sys.argv[1]), sys.argv[2])\\"" 
test = "python -c \\"import sys; from crew import Crew; Crew().test(int(sys.argv[1]), sys.argv[2])\\"" 
replay = "python -c \\"import sys; from crew import Crew; Crew().replay(sys.argv[1])\\"" 
"""

    # Add the uv configuration to the pyproject.toml
    with open(pyproject_path, "a") as f:
        f.write(uv_config)

    click.echo("Updated pyproject.toml with uv configuration.")

    # Create a .gitignore file if it doesn't exist
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write("""# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# Virtual environments
venv/
env/
.env/
.venv/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# Logs
*.log

# Local configuration
.env
.env.local

# Output files
output/
""")
        click.echo("Created .gitignore file.")

    # Initialize a git repository if it doesn't exist
    if not os.path.exists(".git"):
        try:
            subprocess.run(["git", "init"], check=True)
            click.echo("Initialized git repository.")
        except subprocess.CalledProcessError:
            click.echo("Failed to initialize git repository.")
        except FileNotFoundError:
            click.echo("Git not found. Please install git to initialize a repository.")

    click.echo("Crew project updated successfully!")
