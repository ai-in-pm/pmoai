"""
Base class for flow state persistence.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel


class FlowPersistence(ABC):
    """Abstract base class for flow state persistence.

    This class defines the interface for flow state persistence implementations.
    Concrete implementations should inherit from this class and implement the
    save_state and load_state methods.
    """

    @abstractmethod
    def save_state(
        self,
        flow_uuid: str,
        method_name: str,
        state_data: Union[Dict[str, Any], BaseModel],
    ) -> None:
        """Save the current flow state.

        Args:
            flow_uuid: Unique identifier for the flow instance
            method_name: Name of the method that just completed
            state_data: Current state data (either dict or Pydantic model)
        """
        pass

    @abstractmethod
    def load_state(self, flow_uuid: str) -> Optional[Dict[str, Any]]:
        """Load the most recent state for a given flow UUID.

        Args:
            flow_uuid: Unique identifier for the flow instance

        Returns:
            The most recent state as a dictionary, or None if no state exists
        """
        pass
