"""
Flow trackable module for tracking flow execution.
"""

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union, cast

from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T")
FlowMethod = Callable[..., Any]


class FlowTrackable:
    """Base class for trackable flow objects.

    This class provides functionality for tracking flow execution, including
    method calls, state changes, and other events.
    """

    def __init__(self):
        """Initialize the flow trackable."""
        self._tracked_methods: Dict[str, FlowMethod] = {}
        self._start_methods: Set[str] = set()
        self._trigger_methods: Dict[str, List[str]] = {}
        self._router_methods: Set[str] = set()
        self._condition_types: Dict[str, str] = {}
        
        # Collect all flow methods
        self._collect_flow_methods()
    
    def _collect_flow_methods(self) -> None:
        """Collect all flow methods from the class."""
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if hasattr(method, "__is_flow_method__"):
                self._tracked_methods[name] = method
                
                if hasattr(method, "__is_start_method__"):
                    self._start_methods.add(name)
                
                if hasattr(method, "__trigger_methods__"):
                    self._trigger_methods[name] = getattr(method, "__trigger_methods__")
                
                if hasattr(method, "__is_router__"):
                    self._router_methods.add(name)
                
                if hasattr(method, "__condition_type__"):
                    self._condition_types[name] = getattr(method, "__condition_type__")
    
    def get_tracked_methods(self) -> Dict[str, FlowMethod]:
        """Get all tracked methods.
        
        Returns:
            A dictionary of tracked methods.
        """
        return self._tracked_methods
    
    def get_start_methods(self) -> Set[str]:
        """Get all start methods.
        
        Returns:
            A set of start method names.
        """
        return self._start_methods
    
    def get_trigger_methods(self) -> Dict[str, List[str]]:
        """Get all trigger methods.
        
        Returns:
            A dictionary of trigger method names.
        """
        return self._trigger_methods
    
    def get_router_methods(self) -> Set[str]:
        """Get all router methods.
        
        Returns:
            A set of router method names.
        """
        return self._router_methods
    
    def get_condition_types(self) -> Dict[str, str]:
        """Get all condition types.
        
        Returns:
            A dictionary of condition types.
        """
        return self._condition_types
