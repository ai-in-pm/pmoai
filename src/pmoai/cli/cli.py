import os
from importlib.metadata import version as get_version
from typing import Optional, Tuple

import click

from pmoai.cli.add_crew_to_flow import add_crew_to_flow
from pmoai.cli.create_crew import create_crew
from pmoai.cli.create_flow import create_flow
from pmoai.cli.crew_chat import run_chat
from pmoai.memory.storage.kickoff_task_outputs_storage import (
    KickoffTaskOutputsSQLiteStorage,
)

from .reset_memories_command import reset_memories_command
from .run_crew import run_crew


@click.group()
@click.version_option(get_version("pmoai"))
def pmoai():
    """Top-level command group for PMOAI."""


@pmoai.command()
@click.argument("type", type=click.Choice(["crew", "flow"]))
@click.argument("name")
@click.option("--provider", type=str, help="The provider to use for the crew")
@click.option("--skip_provider", is_flag=True, help="Skip provider validation")
@click.option("--pm-methodology", type=str, help="The project management methodology to use")
def create(type, name, provider, skip_provider=False, pm_methodology=None):
    """Create a new crew, or flow."""
    if type == "crew":
        create_crew(name, provider, skip_provider, pm_methodology=pm_methodology)
    elif type == "flow":
        create_flow(name)
    else:
        click.secho("Error: Invalid type. Must be 'crew' or 'flow'.", fg="red")


@pmoai.command()
@click.option(
    "--tools", is_flag=True, help="Show the installed version of pmoai tools"
)
def version(tools):
    """Show the installed version of PMOAI."""
    try:
        pmoai_version = get_version("pmoai")
    except Exception:
        pmoai_version = "unknown version"
    click.echo(f"pmoai version: {pmoai_version}")

    if tools:
        try:
            tools_version = get_version("pmoai")
            click.echo(f"pmoai tools version: {tools_version}")
        except Exception:
            click.echo("pmoai tools not installed")


@pmoai.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=5,
    help="Number of iterations to train the crew",
)
@click.option(
    "-f",
    "--filename",
    type=str,
    default="trained_agents_data.pkl",
    help="Path to a custom file for training",
)
def train(n_iterations: int, filename: str):
    """Train the crew."""
    click.echo(f"Training the Crew for {n_iterations} iterations")
    from pmoai.cli.train_crew import train_crew
    train_crew(n_iterations, filename)


@pmoai.command()
@click.option(
    "-t",
    "--task_id",
    type=str,
    help="Replay the crew from this task ID, including all subsequent tasks.",
)
def replay(task_id: str) -> None:
    """
    Replay the crew execution from a specific task.

    Args:
        task_id (str): The ID of the task to replay from.
    """
    try:
        click.echo(f"Replaying the crew from task {task_id}")
        from pmoai.cli.replay_from_task import replay_task_command
        replay_task_command(task_id)
    except Exception as e:
        click.echo(f"An error occurred while replaying: {e}", err=True)


@pmoai.command()
def log_tasks_outputs() -> None:
    """
    Retrieve your latest crew.kickoff() task outputs.
    """
    try:
        storage = KickoffTaskOutputsSQLiteStorage()
        tasks = storage.load()

        if not tasks:
            click.echo(
                "No task outputs found. Only crew kickoff task outputs are logged."
            )
            return

        for index, task in enumerate(tasks, 1):
            click.echo(f"Task {index}: {task['task_id']}")
            click.echo(f"Description: {task['expected_output']}")
            click.echo("------")

    except Exception as e:
        click.echo(f"An error occurred while logging task outputs: {e}", err=True)


@pmoai.command()
@click.option("-l", "--long", is_flag=True, help="Reset LONG TERM memory")
@click.option("-s", "--short", is_flag=True, help="Reset SHORT TERM memory")
@click.option("-e", "--entities", is_flag=True, help="Reset ENTITIES memory")
@click.option("-kn", "--knowledge", is_flag=True, help="Reset KNOWLEDGE storage")
@click.option(
    "-k",
    "--kickoff-outputs",
    is_flag=True,
    help="Reset LATEST KICKOFF TASK OUTPUTS",
)
@click.option("-a", "--all", is_flag=True, help="Reset ALL memories")
def reset_memories(
    long: bool,
    short: bool,
    entities: bool,
    knowledge: bool,
    kickoff_outputs: bool,
    all: bool,
) -> None:
    """
    Reset the crew memories (long, short, entity, latest_crew_kickoff_ouputs). This will delete all the data saved.
    """
    try:
        if not all and not (long or short or entities or knowledge or kickoff_outputs):
            click.echo(
                "Please specify at least one memory type to reset using the appropriate flags."
            )
            return
        reset_memories_command(long, short, entities, knowledge, kickoff_outputs, all)
    except Exception as e:
        click.echo(f"An error occurred while resetting memories: {e}", err=True)


@pmoai.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=3,
    help="Number of iterations to Test the crew",
)
@click.option(
    "-m",
    "--model",
    type=str,
    default="gpt-4o-mini",
    help="LLM Model to run the tests on the Crew. For now only accepting only OpenAI models.",
)
def test(n_iterations: int, model: str):
    """Test the crew and evaluate the results."""
    click.echo(f"Testing the crew for {n_iterations} iterations with model {model}")
    from pmoai.cli.evaluate_crew import evaluate_crew
    evaluate_crew(n_iterations, model)


@pmoai.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.pass_context
def install(context):
    """Install the Crew."""
    from pmoai.cli.install_crew import install_crew
    install_crew(context.args)


@pmoai.command()
@click.option("--project-name", type=str, help="Project name")
@click.option("--project-code", type=str, help="Project code")
@click.option("--organization", type=str, help="Organization name")
@click.option("--portfolio", type=str, help="Portfolio name")
@click.option("--methodology", type=str, help="Project management methodology")
@click.option("--phase", type=str, help="Project phase")
def run(project_name, project_code, organization, portfolio, methodology, phase):
    """Run the Crew."""
    run_crew(
        project_name=project_name,
        project_code=project_code,
        organization=organization,
        portfolio=portfolio,
        methodology=methodology,
        phase=phase,
    )


@pmoai.command()
def update():
    """Update the pyproject.toml of the Crew project to use uv."""
    from pmoai.cli.update_crew import update_crew
    update_crew()


@pmoai.group()
def flow():
    """Flow related commands."""
    pass


@flow.command(name="kickoff")
def flow_run():
    """Kickoff the Flow."""
    click.echo("Running the Flow")
    from pmoai.cli.kickoff_flow import kickoff_flow
    kickoff_flow()


@flow.command(name="plot")
def flow_plot():
    """Plot the Flow."""
    click.echo("Plotting the Flow")
    from pmoai.cli.plot_flow import plot_flow
    plot_flow()


@flow.command(name="add-crew")
@click.argument("crew_name")
def flow_add_crew(crew_name):
    """Add a crew to an existing flow."""
    click.echo(f"Adding crew {crew_name} to the flow")
    add_crew_to_flow(crew_name)


@pmoai.command()
def chat():
    """
    Start a conversation with the Crew, collecting user-supplied inputs,
    and using the Chat LLM to generate responses.
    """
    click.secho(
        "\nStarting a conversation with the Crew\n" "Type 'exit' or Ctrl+C to quit.\n",
    )

    run_chat()


if __name__ == "__main__":
    pmoai()
