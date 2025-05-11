"""Reset memories command."""

import os
import shutil
from pathlib import Path

import click


def reset_memories_command(
    long: bool,
    short: bool,
    entities: bool,
    knowledge: bool,
    kickoff_outputs: bool,
    all: bool,
) -> None:
    """Reset memories.
    
    Args:
        long: Whether to reset long-term memory.
        short: Whether to reset short-term memory.
        entities: Whether to reset entity memory.
        knowledge: Whether to reset knowledge storage.
        kickoff_outputs: Whether to reset kickoff outputs.
        all: Whether to reset all memories.
    """
    home_dir = os.path.expanduser("~")
    pmoai_dir = os.path.join(home_dir, ".pmoai")
    
    if all or long:
        long_term_dir = os.path.join(pmoai_dir, "memory", "long_term")
        if os.path.exists(long_term_dir):
            shutil.rmtree(long_term_dir)
            click.secho(f"Long-term memory reset: {long_term_dir}", fg="green")
        else:
            click.secho(f"Long-term memory directory not found: {long_term_dir}", fg="yellow")
    
    if all or short:
        short_term_dir = os.path.join(pmoai_dir, "memory", "short_term")
        if os.path.exists(short_term_dir):
            shutil.rmtree(short_term_dir)
            click.secho(f"Short-term memory reset: {short_term_dir}", fg="green")
        else:
            click.secho(f"Short-term memory directory not found: {short_term_dir}", fg="yellow")
    
    if all or entities:
        entities_dir = os.path.join(pmoai_dir, "memory", "entities")
        if os.path.exists(entities_dir):
            shutil.rmtree(entities_dir)
            click.secho(f"Entity memory reset: {entities_dir}", fg="green")
        else:
            click.secho(f"Entity memory directory not found: {entities_dir}", fg="yellow")
    
    if all or knowledge:
        knowledge_dir = os.path.join(pmoai_dir, "knowledge")
        if os.path.exists(knowledge_dir):
            shutil.rmtree(knowledge_dir)
            click.secho(f"Knowledge storage reset: {knowledge_dir}", fg="green")
        else:
            click.secho(f"Knowledge directory not found: {knowledge_dir}", fg="yellow")
    
    if all or kickoff_outputs:
        kickoff_outputs_file = os.path.join(pmoai_dir, "memory", "kickoff_task_outputs.db")
        if os.path.exists(kickoff_outputs_file):
            os.remove(kickoff_outputs_file)
            click.secho(f"Kickoff outputs reset: {kickoff_outputs_file}", fg="green")
        else:
            click.secho(f"Kickoff outputs file not found: {kickoff_outputs_file}", fg="yellow")
    
    click.secho("Memory reset complete.", fg="green", bold=True)
