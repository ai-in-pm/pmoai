from typing import Dict, List, Type

from pydantic import BaseModel, Field

from pmoai.tools.base_tool import BaseTool


class Resource(BaseModel):
    """Model for a project resource."""
    
    id: str = Field(description="A unique identifier for the resource (e.g., R-001).")
    name: str = Field(description="The name of the resource.")
    role: str = Field(description="The role of the resource.")
    skills: List[str] = Field(description="The skills of the resource.")
    availability: float = Field(description="The availability of the resource in percentage (0-100).")
    cost_rate: float = Field(description="The cost rate of the resource per hour.")
    location: str = Field(description="The location of the resource.")


class Task(BaseModel):
    """Model for a project task."""
    
    id: str = Field(description="A unique identifier for the task (e.g., T-001).")
    name: str = Field(description="The name of the task.")
    description: str = Field(description="A description of the task.")
    duration: float = Field(description="The duration of the task in hours.")
    required_skills: List[str] = Field(description="The skills required for the task.")
    dependencies: List[str] = Field(description="The dependencies of the task.")
    priority: str = Field(description="The priority of the task (High, Medium, Low).")


class ResourceAllocation(BaseModel):
    """Model for a resource allocation."""
    
    task_id: str = Field(description="The ID of the task.")
    resource_id: str = Field(description="The ID of the resource.")
    allocation_percentage: float = Field(description="The percentage of the resource allocated to the task (0-100).")
    start_date: str = Field(description="The start date of the allocation (YYYY-MM-DD).")
    end_date: str = Field(description="The end date of the allocation (YYYY-MM-DD).")


class ResourceAllocationInput(BaseModel):
    """Input schema for ResourceAllocationTool."""
    
    project_name: str = Field(description="The name of the project.")
    resources: List[Resource] = Field(description="The list of resources for the project.")
    tasks: List[Task] = Field(description="The list of tasks for the project.")
    allocations: List[ResourceAllocation] = Field(description="The list of resource allocations.")


class ResourceAllocationTool(BaseTool):
    """Tool for creating a resource allocation document."""
    
    name: str = "Resource Allocation Generator"
    description: str = "Creates a comprehensive resource allocation document based on provided information."
    args_schema: Type[BaseModel] = ResourceAllocationInput
    
    def _run(
        self,
        project_name: str,
        resources: List[Resource],
        tasks: List[Task],
        allocations: List[ResourceAllocation],
    ) -> str:
        """Create a resource allocation document.
        
        Args:
            project_name: The name of the project.
            resources: The list of resources for the project.
            tasks: The list of tasks for the project.
            allocations: The list of resource allocations.
            
        Returns:
            A formatted resource allocation document.
        """
        # Create resource lookup dictionary
        resource_lookup = {r.id: r for r in resources}
        task_lookup = {t.id: t for t in tasks}
        
        # Create the header of the resource allocation document
        allocation_doc = f"""
# RESOURCE ALLOCATION PLAN

## Project Name
{project_name}

## Date
{self._get_current_date()}

## Resources

| ID | Name | Role | Skills | Availability | Cost Rate | Location |
|----|------|------|--------|-------------|-----------|----------|
"""
        
        # Add each resource to the document
        for resource in resources:
            skills_str = ", ".join(resource.skills)
            allocation_doc += f"| {resource.id} | {resource.name} | {resource.role} | {skills_str} | {resource.availability}% | ${resource.cost_rate}/hr | {resource.location} |\n"
        
        # Add tasks section
        allocation_doc += """
## Tasks

| ID | Name | Description | Duration (hrs) | Required Skills | Dependencies | Priority |
|----|------|-------------|---------------|----------------|-------------|----------|
"""
        
        # Add each task to the document
        for task in tasks:
            skills_str = ", ".join(task.required_skills)
            dependencies_str = ", ".join(task.dependencies) if task.dependencies else "None"
            allocation_doc += f"| {task.id} | {task.name} | {task.description} | {task.duration} | {skills_str} | {dependencies_str} | {task.priority} |\n"
        
        # Add allocations section
        allocation_doc += """
## Allocations

| Task | Resource | Allocation % | Start Date | End Date | Resource Utilization |
|------|----------|-------------|------------|----------|---------------------|
"""
        
        # Add each allocation to the document
        for allocation in allocations:
            resource = resource_lookup.get(allocation.resource_id)
            task = task_lookup.get(allocation.task_id)
            
            if resource and task:
                resource_utilization = (allocation.allocation_percentage / 100) * task.duration
                allocation_doc += f"| {task.name} | {resource.name} | {allocation.allocation_percentage}% | {allocation.start_date} | {allocation.end_date} | {resource_utilization} hours |\n"
        
        # Add summary section
        allocation_doc += """
## Resource Utilization Summary

| Resource | Total Allocated Hours | Total Available Hours | Utilization % |
|----------|----------------------|----------------------|--------------|
"""
        
        # Calculate resource utilization
        resource_hours: Dict[str, float] = {r.id: 0 for r in resources}
        for allocation in allocations:
            if allocation.task_id in task_lookup and allocation.resource_id in resource_lookup:
                task = task_lookup[allocation.task_id]
                resource_hours[allocation.resource_id] += (allocation.allocation_percentage / 100) * task.duration
        
        # Add resource utilization summary
        for resource_id, hours in resource_hours.items():
            if resource_id in resource_lookup:
                resource = resource_lookup[resource_id]
                # Assuming 40-hour work week and 100% availability means 40 hours
                available_hours = (resource.availability / 100) * 40
                utilization_percentage = (hours / available_hours) * 100 if available_hours > 0 else 0
                allocation_doc += f"| {resource.name} | {hours:.2f} | {available_hours:.2f} | {utilization_percentage:.2f}% |\n"
        
        return allocation_doc
    
    def _get_current_date(self) -> str:
        """Get the current date in YYYY-MM-DD format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
