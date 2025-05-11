from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pmoai.agent import Agent
from pmoai.task import Task


class Resource(BaseModel):
    """Represents a project resource."""
    
    id: str = Field(description="The resource identifier.")
    name: str = Field(description="The name of the resource.")
    type: str = Field(description="The type of resource (e.g., 'human', 'equipment', 'material').")
    skills: Optional[List[str]] = Field(None, description="The skills of the resource (for human resources).")
    cost_rate: Optional[float] = Field(None, description="The cost rate of the resource.")
    availability: float = Field(description="The availability percentage (0-100).")
    start_date: Optional[str] = Field(None, description="The start date of the resource availability.")
    end_date: Optional[str] = Field(None, description="The end date of the resource availability.")


class ResourceAllocation(BaseModel):
    """Represents a resource allocation."""
    
    resource_id: str = Field(description="The resource identifier.")
    task_id: str = Field(description="The task identifier.")
    allocation_percentage: float = Field(description="The allocation percentage (0-100).")
    start_date: str = Field(description="The start date of the allocation.")
    end_date: str = Field(description="The end date of the allocation.")


class ResourcePlan(BaseModel):
    """Represents a resource plan."""
    
    project_name: str = Field(description="The name of the project.")
    project_code: Optional[str] = Field(None, description="The project code.")
    resources: List[Resource] = Field(description="The resources available for the project.")
    allocations: List[ResourceAllocation] = Field(description="The resource allocations for the project.")


class ResourcePlanner(BaseModel):
    """Plans and manages project resources."""
    
    resource_manager_agent: Agent = Field(description="The resource manager agent.")
    
    def create_resource_plan(
        self,
        project_name: str,
        project_code: Optional[str] = None,
        resources: Optional[List[Resource]] = None,
        tasks: Optional[List[Dict[str, Any]]] = None,
    ) -> ResourcePlan:
        """Create a resource plan.
        
        Args:
            project_name: The name of the project.
            project_code: The project code.
            resources: The resources available for the project.
            tasks: The tasks for the project.
            
        Returns:
            A resource plan.
        """
        # Create a task for the resource manager to create a resource plan
        planning_task = Task(
            description=f"""
            Create a comprehensive resource plan for the project '{project_name}'.
            
            Project Code: {project_code or 'N/A'}
            
            Available Resources:
            {resources or 'No resources provided.'}
            
            Project Tasks:
            {tasks or 'No tasks provided.'}
            
            Include the following in your resource plan:
            - Resource allocations for each task
            - Resource utilization over time
            - Resource conflicts and resolutions
            - Resource costs
            
            Provide your resource plan in JSON format.
            """,
            expected_output="A comprehensive resource plan in JSON format.",
            agent=self.resource_manager_agent,
        )
        
        # Execute the task
        result = planning_task.execute()
        
        # Parse the result into a ResourcePlan
        plan_data = result.raw
        
        # Create a ResourcePlan object
        plan = ResourcePlan(
            project_name=project_name,
            project_code=project_code,
            resources=resources or [],
            allocations=[],
            **plan_data,
        )
        
        return plan
    
    def optimize_resource_allocations(
        self, resource_plan: ResourcePlan
    ) -> ResourcePlan:
        """Optimize resource allocations in a resource plan.
        
        Args:
            resource_plan: The resource plan to optimize.
            
        Returns:
            The optimized resource plan.
        """
        # Create a task for the resource manager to optimize resource allocations
        optimization_task = Task(
            description=f"""
            Optimize the resource allocations in the resource plan for the project '{resource_plan.project_name}'.
            
            Current Resource Plan:
            {resource_plan.json(indent=2)}
            
            Optimize the resource allocations to:
            - Minimize resource conflicts
            - Maximize resource utilization
            - Balance workload across resources
            - Minimize project duration
            - Minimize project cost
            
            Provide the optimized resource plan in JSON format.
            """,
            expected_output="An optimized resource plan in JSON format.",
            agent=self.resource_manager_agent,
        )
        
        # Execute the task
        result = optimization_task.execute()
        
        # Parse the result into a ResourcePlan
        optimized_plan_data = result.raw
        
        # Create a new ResourcePlan object with the optimized allocations
        optimized_plan = ResourcePlan(**optimized_plan_data)
        
        return optimized_plan
    
    def analyze_resource_utilization(
        self, resource_plan: ResourcePlan
    ) -> Dict[str, Any]:
        """Analyze resource utilization in a resource plan.
        
        Args:
            resource_plan: The resource plan to analyze.
            
        Returns:
            An analysis of resource utilization.
        """
        # Create a task for the resource manager to analyze resource utilization
        analysis_task = Task(
            description=f"""
            Analyze the resource utilization in the resource plan for the project '{resource_plan.project_name}'.
            
            Resource Plan:
            {resource_plan.json(indent=2)}
            
            Provide an analysis of resource utilization, including:
            - Overall resource utilization percentage
            - Resource utilization over time
            - Overallocated resources
            - Underallocated resources
            - Resource utilization by type
            - Recommendations for improvement
            
            Provide your analysis in JSON format.
            """,
            expected_output="An analysis of resource utilization in JSON format.",
            agent=self.resource_manager_agent,
        )
        
        # Execute the task
        result = analysis_task.execute()
        
        # Parse the result into a dictionary
        analysis = result.raw
        
        return analysis
