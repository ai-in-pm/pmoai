"""Run a crew."""

import os
import sys
from pathlib import Path
from typing import Optional

import click

from pmoai.config import ConfigLoader
from pmoai.cli.utils import find_config_dir


def run_crew(
    project_name: Optional[str] = None,
    project_code: Optional[str] = None,
    organization: Optional[str] = None,
    portfolio: Optional[str] = None,
    methodology: Optional[str] = None,
    phase: Optional[str] = None,
) -> None:
    """Run a crew.
    
    Args:
        project_name: The name of the project.
        project_code: The code of the project.
        organization: The organization name.
        portfolio: The portfolio name.
        methodology: The project management methodology.
        phase: The project phase.
    """
    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        click.secho("Error: OPENAI_API_KEY environment variable is not set.", fg="red")
        click.secho("Please set it before running PMOAI.", fg="red")
        sys.exit(1)
    
    # Find the config directory
    config_dir = find_config_dir()
    if not config_dir:
        click.secho("Error: Could not find config directory.", fg="red")
        click.secho("Please run this command from a PMOAI project directory.", fg="red")
        sys.exit(1)
    
    # Load the config
    config_loader = ConfigLoader(config_dir)
    
    # Get the crew name
    crew_names = list(config_loader.crews_config.keys())
    if not crew_names:
        click.secho("Error: No crews found in configuration.", fg="red")
        sys.exit(1)
    
    # If there's only one crew, use it
    if len(crew_names) == 1:
        crew_name = crew_names[0]
    else:
        # Otherwise, ask the user to select a crew
        click.secho("Select a crew to run:", fg="green")
        for i, name in enumerate(crew_names, 1):
            click.echo(f"{i}. {name}")
        
        while True:
            choice = click.prompt("Enter your choice (number)", default="1")
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(crew_names):
                    crew_name = crew_names[choice_idx]
                    break
                else:
                    click.secho("Invalid choice. Please try again.", fg="red")
            except ValueError:
                click.secho("Invalid input. Please enter a number.", fg="red")
    
    # Create the crew
    try:
        crew = config_loader.get_crew(crew_name)
    except Exception as e:
        click.secho(f"Error creating crew: {e}", fg="red")
        sys.exit(1)
    
    # Update crew properties
    if project_name:
        crew.project_name = project_name
    if project_code:
        crew.project_code = project_code
    if organization:
        crew.organization = organization
    if portfolio:
        crew.portfolio = portfolio
    if methodology:
        crew.project_methodology = methodology
    if phase:
        crew.project_phase = phase
    
    # Execute crew
    click.secho(f"=== Executing Crew: {crew_name} ===", fg="green", bold=True)
    click.echo(f"Project: {crew.project_name}")
    click.echo(f"Methodology: {crew.project_methodology}")
    click.echo(f"Phase: {crew.project_phase}")
    click.echo()
    
    try:
        result = crew.kickoff()
    except Exception as e:
        click.secho(f"Error executing crew: {e}", fg="red")
        sys.exit(1)
    
    # Print results
    click.secho("\n=== Execution Results ===\n", fg="green", bold=True)
    click.echo(result.raw)
    
    # Save results to files
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    for i, task_output in enumerate(result.tasks_output):
        task_name = task_output.task.description.split()[0].lower()
        filename = output_dir / f"output_{i+1}_{task_name}.md"
        
        with open(filename, "w") as f:
            f.write(task_output.raw)
        
        click.secho(f"Saved {filename}", fg="green")
    
    return None
