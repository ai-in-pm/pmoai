from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from pmoai.lims.lims_connector import LIMSConnector
from pmoai.lims.lims_data import LIMSData, LIMSProject, LIMSResource, LIMSTask


class LIMSClient(BaseModel):
    """Client for interacting with a LIMS system.
    
    This class provides a high-level interface for interacting with a LIMS system
    through a connector.
    """
    
    connector: LIMSConnector = Field(description="The connector to use for LIMS interactions.")
    
    def __init__(self, connector: LIMSConnector, **data: Any):
        """Initialize the LIMS client.
        
        Args:
            connector: The connector to use for LIMS interactions.
            **data: Additional data for the model.
        """
        super().__init__(connector=connector, **data)
        self.connector.connect()
    
    def get_projects(self) -> List[LIMSProject]:
        """Get all projects from the LIMS system.
        
        Returns:
            A list of projects.
        """
        return self.connector.get_projects()
    
    def get_project(self, project_id: str) -> Optional[LIMSProject]:
        """Get a project from the LIMS system.
        
        Args:
            project_id: The ID of the project to get.
            
        Returns:
            The project, or None if not found.
        """
        return self.connector.get_project(project_id)
    
    def create_project(self, project: LIMSProject) -> LIMSProject:
        """Create a project in the LIMS system.
        
        Args:
            project: The project to create.
            
        Returns:
            The created project.
        """
        return self.connector.create_project(project)
    
    def update_project(self, project: LIMSProject) -> LIMSProject:
        """Update a project in the LIMS system.
        
        Args:
            project: The project to update.
            
        Returns:
            The updated project.
        """
        return self.connector.update_project(project)
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project from the LIMS system.
        
        Args:
            project_id: The ID of the project to delete.
            
        Returns:
            Whether the deletion was successful.
        """
        return self.connector.delete_project(project_id)
    
    def get_tasks(self, project_id: Optional[str] = None) -> List[LIMSTask]:
        """Get tasks from the LIMS system.
        
        Args:
            project_id: The ID of the project to get tasks for, or None to get all tasks.
            
        Returns:
            A list of tasks.
        """
        return self.connector.get_tasks(project_id)
    
    def get_task(self, task_id: str) -> Optional[LIMSTask]:
        """Get a task from the LIMS system.
        
        Args:
            task_id: The ID of the task to get.
            
        Returns:
            The task, or None if not found.
        """
        return self.connector.get_task(task_id)
    
    def create_task(self, task: LIMSTask) -> LIMSTask:
        """Create a task in the LIMS system.
        
        Args:
            task: The task to create.
            
        Returns:
            The created task.
        """
        return self.connector.create_task(task)
    
    def update_task(self, task: LIMSTask) -> LIMSTask:
        """Update a task in the LIMS system.
        
        Args:
            task: The task to update.
            
        Returns:
            The updated task.
        """
        return self.connector.update_task(task)
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task from the LIMS system.
        
        Args:
            task_id: The ID of the task to delete.
            
        Returns:
            Whether the deletion was successful.
        """
        return self.connector.delete_task(task_id)
    
    def get_resources(self) -> List[LIMSResource]:
        """Get all resources from the LIMS system.
        
        Returns:
            A list of resources.
        """
        return self.connector.get_resources()
    
    def get_resource(self, resource_id: str) -> Optional[LIMSResource]:
        """Get a resource from the LIMS system.
        
        Args:
            resource_id: The ID of the resource to get.
            
        Returns:
            The resource, or None if not found.
        """
        return self.connector.get_resource(resource_id)
    
    def create_resource(self, resource: LIMSResource) -> LIMSResource:
        """Create a resource in the LIMS system.
        
        Args:
            resource: The resource to create.
            
        Returns:
            The created resource.
        """
        return self.connector.create_resource(resource)
    
    def update_resource(self, resource: LIMSResource) -> LIMSResource:
        """Update a resource in the LIMS system.
        
        Args:
            resource: The resource to update.
            
        Returns:
            The updated resource.
        """
        return self.connector.update_resource(resource)
    
    def delete_resource(self, resource_id: str) -> bool:
        """Delete a resource from the LIMS system.
        
        Args:
            resource_id: The ID of the resource to delete.
            
        Returns:
            Whether the deletion was successful.
        """
        return self.connector.delete_resource(resource_id)
    
    def close(self) -> None:
        """Close the connection to the LIMS system."""
        self.connector.disconnect()
