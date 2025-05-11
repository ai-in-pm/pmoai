from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LIMSData(BaseModel):
    """Base class for LIMS data."""
    
    id: str = Field(description="The unique identifier for the data.")
    name: str = Field(description="The name of the data.")
    description: Optional[str] = Field(None, description="A description of the data.")
    created_at: datetime = Field(description="The creation timestamp.")
    updated_at: datetime = Field(description="The last update timestamp.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata.")


class LIMSProject(LIMSData):
    """Represents a project in a LIMS system."""
    
    code: str = Field(description="The project code.")
    status: str = Field(description="The status of the project.")
    start_date: datetime = Field(description="The start date of the project.")
    end_date: Optional[datetime] = Field(None, description="The end date of the project.")
    client: Optional[str] = Field(None, description="The client for the project.")
    budget: Optional[float] = Field(None, description="The budget for the project.")
    priority: str = Field(description="The priority of the project.")
    tasks: List[str] = Field(default_factory=list, description="The IDs of tasks in the project.")
    resources: List[str] = Field(default_factory=list, description="The IDs of resources assigned to the project.")


class LIMSTask(LIMSData):
    """Represents a task in a LIMS system."""
    
    project_id: str = Field(description="The ID of the project the task belongs to.")
    status: str = Field(description="The status of the task.")
    start_date: datetime = Field(description="The start date of the task.")
    end_date: Optional[datetime] = Field(None, description="The end date of the task.")
    assignee: Optional[str] = Field(None, description="The ID of the resource assigned to the task.")
    priority: str = Field(description="The priority of the task.")
    dependencies: List[str] = Field(default_factory=list, description="The IDs of tasks this task depends on.")
    progress: float = Field(default=0.0, description="The progress of the task (0-100).")


class LIMSResource(LIMSData):
    """Represents a resource in a LIMS system."""
    
    type: str = Field(description="The type of resource (e.g., 'human', 'equipment', 'material').")
    status: str = Field(description="The status of the resource.")
    availability: float = Field(description="The availability percentage (0-100).")
    skills: List[str] = Field(default_factory=list, description="The skills of the resource (for human resources).")
    cost_rate: Optional[float] = Field(None, description="The cost rate of the resource.")
    assigned_projects: List[str] = Field(default_factory=list, description="The IDs of projects the resource is assigned to.")
    assigned_tasks: List[str] = Field(default_factory=list, description="The IDs of tasks the resource is assigned to.")
