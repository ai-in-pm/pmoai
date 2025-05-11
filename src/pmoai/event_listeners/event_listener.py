from datetime import datetime
from typing import Any, Dict, Optional

from crewai.utilities.events.crewai_event_bus import crewai_event_bus
from pydantic import Field, PrivateAttr

from pmoai.event_listeners.base_event_listener import BaseEventListener
from pmoai.event_listeners.pm_events import (
    DeliverableCompletedEvent,
    MilestoneCompletedEvent,
    ProjectClosingEvent,
    ProjectExecutionEvent,
    ProjectInitiationEvent,
    ProjectMonitoringEvent,
    ProjectPlanningEvent,
    ResourceAllocationEvent,
    RiskIdentifiedEvent,
    StakeholderCommunicationEvent,
)


class EventListener(BaseEventListener):
    """Event listener for PMOAI events.
    
    This class extends the BaseEventListener to handle PM-specific events.
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the event listener."""
        if getattr(self, "_initialized", False):
            return
        
        super().__init__()
        self._initialized = True
        self.setup_listeners(crewai_event_bus)
    
    def setup_listeners(self, event_bus: Any) -> None:
        """Set up event listeners for PM-specific events.
        
        Args:
            event_bus: The event bus to register listeners with.
        """
        # Project lifecycle events
        @event_bus.on(ProjectInitiationEvent)
        def on_project_initiation(source: Any, event: ProjectInitiationEvent) -> None:
            """Handle project initiation events."""
            print(f"Project '{event.project_name}' initiated by {event.sponsor} on {event.start_date}")
        
        @event_bus.on(ProjectPlanningEvent)
        def on_project_planning(source: Any, event: ProjectPlanningEvent) -> None:
            """Handle project planning events."""
            print(f"Project '{event.project_name}' planning: {event.plan_type} plan {event.plan_status}")
        
        @event_bus.on(ProjectExecutionEvent)
        def on_project_execution(source: Any, event: ProjectExecutionEvent) -> None:
            """Handle project execution events."""
            print(f"Project '{event.project_name}' execution: {event.activity} is {event.status} ({event.progress}% complete)")
        
        @event_bus.on(ProjectMonitoringEvent)
        def on_project_monitoring(source: Any, event: ProjectMonitoringEvent) -> None:
            """Handle project monitoring events."""
            print(f"Project '{event.project_name}' monitoring: {event.metric} - Actual: {event.actual_value}, Planned: {event.planned_value}, Variance: {event.variance}")
        
        @event_bus.on(ProjectClosingEvent)
        def on_project_closing(source: Any, event: ProjectClosingEvent) -> None:
            """Handle project closing events."""
            print(f"Project '{event.project_name}' closed on {event.end_date} with status: {event.status}")
        
        # Risk management events
        @event_bus.on(RiskIdentifiedEvent)
        def on_risk_identified(source: Any, event: RiskIdentifiedEvent) -> None:
            """Handle risk identified events."""
            print(f"Project '{event.project_name}' risk identified: {event.risk_id} - {event.risk_description} (Probability: {event.probability}, Impact: {event.impact})")
        
        # Stakeholder management events
        @event_bus.on(StakeholderCommunicationEvent)
        def on_stakeholder_communication(source: Any, event: StakeholderCommunicationEvent) -> None:
            """Handle stakeholder communication events."""
            print(f"Project '{event.project_name}' stakeholder communication: {event.communication_type} with {event.stakeholder}")
        
        # Resource management events
        @event_bus.on(ResourceAllocationEvent)
        def on_resource_allocation(source: Any, event: ResourceAllocationEvent) -> None:
            """Handle resource allocation events."""
            print(f"Project '{event.project_name}' resource allocation: {event.resource_name} ({event.resource_type}) allocated at {event.allocation_percentage}% from {event.start_date} to {event.end_date}")
        
        # Milestone and deliverable events
        @event_bus.on(MilestoneCompletedEvent)
        def on_milestone_completed(source: Any, event: MilestoneCompletedEvent) -> None:
            """Handle milestone completed events."""
            print(f"Project '{event.project_name}' milestone completed: {event.milestone_name} on {event.completion_date} with status: {event.status}")
        
        @event_bus.on(DeliverableCompletedEvent)
        def on_deliverable_completed(source: Any, event: DeliverableCompletedEvent) -> None:
            """Handle deliverable completed events."""
            print(f"Project '{event.project_name}' deliverable completed: {event.deliverable_name} on {event.completion_date} with quality status: {event.quality_status}")


# Create a singleton instance
event_listener = EventListener()
