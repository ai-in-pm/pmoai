from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ProjectEvent(BaseModel):
    """Base class for project-related events."""
    
    project_name: str = Field(description="The name of the project.")
    project_code: Optional[str] = Field(None, description="The project code.")
    timestamp: str = Field(description="The timestamp of the event.")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional event details.")


class ProjectInitiationEvent(ProjectEvent):
    """Event emitted when a project is initiated."""
    
    sponsor: str = Field(description="The project sponsor.")
    start_date: str = Field(description="The project start date.")
    estimated_end_date: str = Field(description="The estimated project end date.")


class ProjectPlanningEvent(ProjectEvent):
    """Event emitted during project planning."""
    
    plan_type: str = Field(description="The type of plan (e.g., 'schedule', 'resource', 'risk').")
    plan_status: str = Field(description="The status of the plan.")


class ProjectExecutionEvent(ProjectEvent):
    """Event emitted during project execution."""
    
    activity: str = Field(description="The activity being executed.")
    status: str = Field(description="The status of the activity.")
    progress: float = Field(description="The progress percentage (0-100).")


class ProjectMonitoringEvent(ProjectEvent):
    """Event emitted during project monitoring."""
    
    metric: str = Field(description="The metric being monitored.")
    actual_value: Any = Field(description="The actual value of the metric.")
    planned_value: Any = Field(description="The planned value of the metric.")
    variance: Any = Field(description="The variance between actual and planned values.")


class ProjectClosingEvent(ProjectEvent):
    """Event emitted when a project is closed."""
    
    end_date: str = Field(description="The actual project end date.")
    status: str = Field(description="The final status of the project.")
    lessons_learned: Optional[str] = Field(None, description="Lessons learned from the project.")


class RiskIdentifiedEvent(ProjectEvent):
    """Event emitted when a risk is identified."""
    
    risk_id: str = Field(description="The risk identifier.")
    risk_description: str = Field(description="The description of the risk.")
    probability: str = Field(description="The probability of the risk occurring (High, Medium, Low).")
    impact: str = Field(description="The impact if the risk occurs (High, Medium, Low).")
    mitigation_strategy: Optional[str] = Field(None, description="The strategy to mitigate the risk.")


class StakeholderCommunicationEvent(ProjectEvent):
    """Event emitted during stakeholder communication."""
    
    stakeholder: str = Field(description="The stakeholder being communicated with.")
    communication_type: str = Field(description="The type of communication.")
    message: str = Field(description="The communication message.")
    response: Optional[str] = Field(None, description="The stakeholder's response.")


class ResourceAllocationEvent(ProjectEvent):
    """Event emitted during resource allocation."""
    
    resource_type: str = Field(description="The type of resource being allocated.")
    resource_name: str = Field(description="The name of the resource.")
    allocation_percentage: float = Field(description="The allocation percentage (0-100).")
    start_date: str = Field(description="The start date of the allocation.")
    end_date: str = Field(description="The end date of the allocation.")


class MilestoneCompletedEvent(ProjectEvent):
    """Event emitted when a milestone is completed."""
    
    milestone_id: str = Field(description="The milestone identifier.")
    milestone_name: str = Field(description="The name of the milestone.")
    completion_date: str = Field(description="The date the milestone was completed.")
    status: str = Field(description="The status of the milestone.")


class DeliverableCompletedEvent(ProjectEvent):
    """Event emitted when a deliverable is completed."""
    
    deliverable_id: str = Field(description="The deliverable identifier.")
    deliverable_name: str = Field(description="The name of the deliverable.")
    completion_date: str = Field(description="The date the deliverable was completed.")
    quality_status: str = Field(description="The quality status of the deliverable.")
