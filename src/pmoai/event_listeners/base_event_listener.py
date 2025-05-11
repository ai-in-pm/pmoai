from abc import ABC, abstractmethod
from typing import Any

from crewai.utilities.events.base_event_listener import BaseEventListener as CrewAIBaseEventListener


class BaseEventListener(CrewAIBaseEventListener, ABC):
    """Base class for event listeners in PMOAI.
    
    This class extends CrewAI's BaseEventListener to provide PM-specific event handling.
    """

    def __init__(self):
        """Initialize the event listener."""
        super().__init__()
    
    @abstractmethod
    def setup_listeners(self, event_bus: Any) -> None:
        """Set up event listeners.
        
        Args:
            event_bus: The event bus to register listeners with.
        """
        pass
