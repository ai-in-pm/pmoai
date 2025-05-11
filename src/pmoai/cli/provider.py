"""Provider utilities for the PMOAI CLI."""

import click

from pmoai.cli.constants import MODELS


def get_provider_data():
    """Get provider data.
    
    Returns:
        A dictionary of provider data.
    """
    provider_models = {
        "openai": MODELS["openai"],
        "anthropic": MODELS["anthropic"],
        "google": MODELS["google"],
        "azure_openai": MODELS["azure_openai"],
        "ollama": MODELS["ollama"],
        "together": MODELS["together"],
        "groq": MODELS["groq"],
        "mistral": MODELS["mistral"],
        "anyscale": MODELS["anyscale"],
        "cohere": MODELS["cohere"],
        "huggingface": MODELS["huggingface"],
        "replicate": MODELS["replicate"],
        "perplexity": MODELS["perplexity"],
        "fireworks": MODELS["fireworks"],
        "deepinfra": MODELS["deepinfra"],
        "voyage": MODELS["voyage"],
        "databricks": MODELS["databricks"],
    }
    
    return provider_models


def select_provider(provider_models):
    """Select a provider.
    
    Args:
        provider_models: A dictionary of provider data.
        
    Returns:
        The selected provider.
    """
    click.secho("Select a provider:", fg="green")
    providers = list(provider_models.keys())
    
    for i, provider in enumerate(providers, 1):
        click.echo(f"{i}. {provider.capitalize()}")
    
    while True:
        choice = click.prompt("Enter your choice (number or 'q' to quit)", default="1")
        if choice.lower() == "q":
            return None
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(providers):
                return providers[choice_idx]
            else:
                click.secho("Invalid choice. Please try again.", fg="red")
        except ValueError:
            click.secho("Invalid input. Please enter a number or 'q'.", fg="red")


def select_model(provider, provider_models):
    """Select a model.
    
    Args:
        provider: The provider to select a model for.
        provider_models: A dictionary of provider data.
        
    Returns:
        The selected model.
    """
    models = provider_models[provider]
    
    if not models:
        click.secho(
            f"No predefined models for {provider}. You'll need to specify the model in your code.",
            fg="yellow",
        )
        return ""
    
    click.secho(f"Select a model for {provider.capitalize()}:", fg="green")
    
    for i, model in enumerate(models, 1):
        click.echo(f"{i}. {model}")
    
    while True:
        choice = click.prompt("Enter your choice (number or 'q' to quit)", default="1")
        if choice.lower() == "q":
            return None
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(models):
                return models[choice_idx]
            else:
                click.secho("Invalid choice. Please try again.", fg="red")
        except ValueError:
            click.secho("Invalid input. Please enter a number or 'q'.", fg="red")
