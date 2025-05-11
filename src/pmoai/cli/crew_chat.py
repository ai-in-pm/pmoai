"""Crew chat module."""

import os
import sys
from pathlib import Path
from typing import Optional

import click

from pmoai.config import ConfigLoader
from pmoai.cli.utils import find_config_dir


def run_chat() -> None:
    """Run a chat with the crew."""
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
        click.secho("Select a crew to chat with:", fg="green")
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
    
    # Start the chat
    click.secho(f"=== Starting Chat with Crew: {crew_name} ===", fg="green", bold=True)
    click.echo(f"Project: {crew.project_name}")
    click.echo(f"Methodology: {crew.project_methodology}")
    click.echo(f"Phase: {crew.project_phase}")
    click.echo()
    
    # Initialize chat history
    chat_history = []
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = click.prompt("You", prompt_suffix="> ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "q"]:
                click.secho("Exiting chat...", fg="yellow")
                break
            
            # Add user message to chat history
            chat_history.append({"role": "user", "content": user_input})
            
            # Get crew response
            with click.progressbar(
                length=100,
                label="Crew is thinking...",
                show_eta=False,
                show_percent=True,
                fill_char="=",
                empty_char=" ",
            ) as bar:
                # Simulate progress
                for i in range(100):
                    bar.update(1)
                    import time
                    time.sleep(0.01)
                
                # Get response from crew
                response = "This is a placeholder response. In a real implementation, this would be a response from the crew."
            
            # Add crew response to chat history
            chat_history.append({"role": "assistant", "content": response})
            
            # Display crew response
            click.secho("Crew", fg="green", bold=True, nl=False)
            click.echo("> " + response)
            
        except KeyboardInterrupt:
            click.secho("\nExiting chat...", fg="yellow")
            break
        except Exception as e:
            click.secho(f"Error: {e}", fg="red")
    
    return None
