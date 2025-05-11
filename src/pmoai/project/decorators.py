"""Decorators for PMOAI projects."""

import functools
import inspect
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast

import yaml

from pmoai.agent import Agent
from pmoai.crew import Crew
from pmoai.flow.flow import Flow
from pmoai.task import Task

T = TypeVar("T")


def agent(func: Callable[..., Agent]) -> Callable[..., Agent]:
    """Decorator for agent methods.
    
    This decorator marks a method as an agent method, which will be collected
    by the CrewBase decorator.
    
    Args:
        func: The agent method to decorate.
        
    Returns:
        The decorated agent method.
    """
    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Agent:
        agent_instance = func(self, *args, **kwargs)
        if not hasattr(self, "_agents"):
            self._agents = []
        self._agents.append(agent_instance)
        return agent_instance
    
    wrapper._is_agent = True  # type: ignore
    return wrapper


def task(func: Callable[..., Task]) -> Callable[..., Task]:
    """Decorator for task methods.
    
    This decorator marks a method as a task method, which will be collected
    by the CrewBase decorator.
    
    Args:
        func: The task method to decorate.
        
    Returns:
        The decorated task method.
    """
    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Task:
        task_instance = func(self, *args, **kwargs)
        if not hasattr(self, "_tasks"):
            self._tasks = []
        self._tasks.append(task_instance)
        return task_instance
    
    wrapper._is_task = True  # type: ignore
    return wrapper


def crew(func: Callable[..., Crew]) -> Callable[..., Crew]:
    """Decorator for crew methods.
    
    This decorator marks a method as a crew method, which will be collected
    by the CrewBase decorator.
    
    Args:
        func: The crew method to decorate.
        
    Returns:
        The decorated crew method.
    """
    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Crew:
        crew_instance = func(self, *args, **kwargs)
        if not hasattr(self, "_crew"):
            self._crew = crew_instance
        return crew_instance
    
    wrapper._is_crew = True  # type: ignore
    return wrapper


def flow(func: Callable[..., Flow]) -> Callable[..., Flow]:
    """Decorator for flow methods.
    
    This decorator marks a method as a flow method, which will be collected
    by the FlowBase decorator.
    
    Args:
        func: The flow method to decorate.
        
    Returns:
        The decorated flow method.
    """
    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Flow:
        flow_instance = func(self, *args, **kwargs)
        if not hasattr(self, "_flow"):
            self._flow = flow_instance
        return flow_instance
    
    wrapper._is_flow = True  # type: ignore
    return wrapper


def CrewBase(cls: Type[T]) -> Type[T]:
    """Decorator for crew classes.
    
    This decorator collects all agent and task methods in the class and
    makes them available as properties.
    
    Args:
        cls: The crew class to decorate.
        
    Returns:
        The decorated crew class.
    """
    original_init = cls.__init__
    
    def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
        """Initialize the crew class."""
        self._agents = []
        self._tasks = []
        self._crew = None
        
        # Load configuration files
        self.agents_config = {}
        self.tasks_config = {}
        self.crews_config = {}
        
        config_dir = Path("config")
        if config_dir.exists():
            agents_yaml = config_dir / "agents.yaml"
            tasks_yaml = config_dir / "tasks.yaml"
            crews_yaml = config_dir / "crews.yaml"
            
            if agents_yaml.exists():
                with open(agents_yaml, "r") as f:
                    self.agents_config = yaml.safe_load(f)
            
            if tasks_yaml.exists():
                with open(tasks_yaml, "r") as f:
                    self.tasks_config = yaml.safe_load(f)
            
            if crews_yaml.exists():
                with open(crews_yaml, "r") as f:
                    self.crews_config = yaml.safe_load(f)
        
        # Call the original __init__
        original_init(self, *args, **kwargs)
        
        # Call all agent methods
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if hasattr(method, "_is_agent"):
                method()
        
        # Call all task methods
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if hasattr(method, "_is_task"):
                method()
        
        # Call the crew method
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if hasattr(method, "_is_crew"):
                method()
    
    def kickoff(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Kickoff the crew."""
        if self._crew is None:
            raise ValueError("No crew method found.")
        return self._crew.kickoff(*args, **kwargs)
    
    def train(self: Any, n_iterations: int, filename: str) -> None:
        """Train the crew."""
        if self._crew is None:
            raise ValueError("No crew method found.")
        # This is a placeholder implementation
        print(f"Training crew for {n_iterations} iterations, saving to {filename}")
    
    def test(self: Any, n_iterations: int, model: str) -> None:
        """Test the crew."""
        if self._crew is None:
            raise ValueError("No crew method found.")
        # This is a placeholder implementation
        print(f"Testing crew for {n_iterations} iterations with model {model}")
    
    def replay(self: Any, task_id: str) -> None:
        """Replay the crew from a specific task."""
        if self._crew is None:
            raise ValueError("No crew method found.")
        # This is a placeholder implementation
        print(f"Replaying crew from task {task_id}")
    
    # Add properties
    cls.__init__ = __init__
    cls.kickoff = kickoff
    cls.train = train
    cls.test = test
    cls.replay = replay
    cls.agents = property(lambda self: self._agents)
    cls.tasks = property(lambda self: self._tasks)
    
    return cls


def FlowBase(cls: Type[T]) -> Type[T]:
    """Decorator for flow classes.
    
    This decorator collects all flow methods in the class and
    makes them available as properties.
    
    Args:
        cls: The flow class to decorate.
        
    Returns:
        The decorated flow class.
    """
    original_init = cls.__init__
    
    def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
        """Initialize the flow class."""
        self._flow = None
        
        # Call the original __init__
        original_init(self, *args, **kwargs)
        
        # Call the flow method
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if hasattr(method, "_is_flow"):
                method()
    
    def kickoff(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Kickoff the flow."""
        if self._flow is None:
            raise ValueError("No flow method found.")
        return self._flow.kickoff(*args, **kwargs)
    
    def plot(self: Any) -> None:
        """Plot the flow."""
        if self._flow is None:
            raise ValueError("No flow method found.")
        # This is a placeholder implementation
        print("Plotting flow")
    
    # Add properties
    cls.__init__ = __init__
    cls.kickoff = kickoff
    cls.plot = plot
    
    return cls
