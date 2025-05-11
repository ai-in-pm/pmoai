"""
Flow module for orchestrating crews.
"""

import asyncio
import functools
import inspect
import logging
import uuid
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

from pydantic import BaseModel, Field

from pmoai.crew import Crew
from pmoai.crews.crew_output import CrewOutput
from pmoai.flow.config import FlowConfig
from pmoai.flow.flow_trackable import FlowTrackable
from pmoai.flow.flow_visualizer import FlowVisualizer
from pmoai.utilities.printer import Printer

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Optional[BaseModel])
FlowMethod = Callable[..., Any]


class Flow(FlowTrackable, Generic[T]):
    """Flow for orchestrating crews.

    A Flow is a collection of crews that can be orchestrated to work together.
    Flows can be used to create complex workflows with multiple crews, where
    the output of one crew can be used as input for another.

    Example:
        ```python
        from pmoai import Flow, Crew, start, listen, or_, and_
        from pydantic import BaseModel, Field

        class MyState(BaseModel):
            id: str = Field(default_factory=lambda: str(uuid.uuid4()))
            step: int = 0
            data: Dict[str, Any] = Field(default_factory=dict)

        class MyFlow(Flow[MyState]):
            def __init__(self):
                super().__init__()
                self.state = MyState()
                self.crew1 = Crew(...)
                self.crew2 = Crew(...)

            @start()
            def begin(self):
                self.state.step = 1
                return self.crew1.kickoff()

            @listen(method="begin")
            def process(self, result: CrewOutput):
                self.state.step = 2
                self.state.data["crew1_result"] = result.raw
                return self.crew2.kickoff()

            @listen(method="process")
            def end(self, result: CrewOutput):
                self.state.step = 3
                self.state.data["crew2_result"] = result.raw
                return result
        ```
    """

    state: T
    crews: List[Crew]
    name: str
    description: str
    verbose: bool

    # Project Management specific properties
    project_name: str = "Project Name"
    project_code: str = "PRJ-001"
    project_methodology: str = "Agile"
    project_phase: str = "Planning"
    organization: str = "Organization Name"
    portfolio: str = "Portfolio Name"

    def __init__(
        self,
        crews: Optional[List[Crew]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        verbose: bool = False,
        state: Optional[T] = None,
    ):
        """Initialize the flow.

        Args:
            crews: Optional list of crews to include in the flow.
            name: Optional name for the flow.
            description: Optional description for the flow.
            verbose: Whether to print verbose output.
            state: Optional initial state for the flow.
        """
        super().__init__()

        self.crews = crews or []
        self.name = name or self.__class__.__name__
        self.description = description or f"{self.name} Flow"
        self.verbose = verbose

        # Initialize state if not provided
        if state is None:
            # Try to infer the state type from the generic parameter
            state_type = self._get_state_type()
            if state_type is not None:
                self.state = state_type()
            else:
                # Default to a basic state with an ID
                class DefaultState(BaseModel):
                    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

                self.state = cast(T, DefaultState())
        else:
            self.state = state

        self._printer = Printer()

    def _get_state_type(self) -> Optional[Type[BaseModel]]:
        """Get the state type from the generic parameter.

        Returns:
            The state type, or None if it couldn't be determined.
        """
        try:
            # Get the generic parameters of the class
            origin = get_origin(self.__class__)
            if origin is not None:
                args = get_args(self.__class__)
                if args and args[0] is not None:
                    return args[0]

            # If that didn't work, try to get it from the annotations
            annotations = getattr(self.__class__, "__annotations__", {})
            if "state" in annotations:
                return annotations["state"]
        except Exception as e:
            logger.warning(f"Failed to get state type: {e}")

        return None

    def kickoff(self) -> Any:
        """Kickoff the flow.

        This method starts the flow by calling the first start method.

        Returns:
            The result of the flow.
        """
        # Find the start methods
        start_methods = self.get_start_methods()
        if not start_methods:
            raise ValueError("No start methods found in the flow")

        # Call the first start method
        start_method_name = next(iter(start_methods))
        start_method = getattr(self, start_method_name)

        if self.verbose:
            self._printer.print(f"Starting flow with method: {start_method_name}", color="green")

        # Call the start method
        return start_method()

    def plot(self, output_path: Optional[str] = None, open_browser: bool = True) -> str:
        """Plot the flow.

        This method generates a visualization of the flow.

        Args:
            output_path: Optional path to save the visualization.
            open_browser: Whether to open the visualization in a browser.

        Returns:
            The path to the generated visualization.
        """
        visualizer = FlowVisualizer(self)
        return visualizer.visualize(output_path, open_browser)


def start():
    """Decorator for marking a method as a flow start point.

    This decorator marks a method as a starting point for the flow. A flow can
    have multiple start methods, but only one will be called when the flow is
    kicked off.

    Returns:
        A decorator function.
    """
    def decorator(method: FlowMethod) -> FlowMethod:
        setattr(method, "__is_flow_method__", True)
        setattr(method, "__is_start_method__", True)
        return method

    return decorator


def listen(method: str):
    """Decorator for marking a method as a listener.

    This decorator marks a method as a listener for another method. When the
    specified method completes, the listener method will be called with the
    result of the specified method.

    Args:
        method: The name of the method to listen to.

    Returns:
        A decorator function.
    """
    def decorator(listener_method: FlowMethod) -> FlowMethod:
        setattr(listener_method, "__is_flow_method__", True)

        # Get or create the trigger methods list
        if hasattr(listener_method, "__trigger_methods__"):
            trigger_methods = getattr(listener_method, "__trigger_methods__")
        else:
            trigger_methods = []

        # Add this listener to the trigger methods of the specified method
        trigger_methods.append(method)
        setattr(listener_method, "__trigger_methods__", trigger_methods)

        return listener_method

    return decorator


def router():
    """Decorator for marking a method as a router.

    This decorator marks a method as a router, which can dynamically determine
    which method to call next based on the input.

    Returns:
        A decorator function.
    """
    def decorator(method: FlowMethod) -> FlowMethod:
        setattr(method, "__is_flow_method__", True)
        setattr(method, "__is_router__", True)
        return method

    return decorator


def or_():
    """Decorator for marking a method as an OR condition.

    This decorator marks a method as an OR condition, which will be triggered
    if any of its trigger methods complete.

    Returns:
        A decorator function.
    """
    def decorator(method: FlowMethod) -> FlowMethod:
        setattr(method, "__is_flow_method__", True)
        setattr(method, "__condition_type__", "OR")
        return method

    return decorator


def and_():
    """Decorator for marking a method as an AND condition.

    This decorator marks a method as an AND condition, which will be triggered
    only if all of its trigger methods complete.

    Returns:
        A decorator function.
    """
    def decorator(method: FlowMethod) -> FlowMethod:
        setattr(method, "__is_flow_method__", True)
        setattr(method, "__condition_type__", "AND")
        return method

    return decorator
