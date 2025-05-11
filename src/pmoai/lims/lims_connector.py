from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from pmoai.lims.lims_data import LIMSData, LIMSProject, LIMSResource, LIMSTask


class LIMSConnector(BaseModel, ABC):
    """Base class for LIMS connectors.
    
    This class defines the interface for connecting to a LIMS system.
    """
    
    name: str = Field(description="The name of the LIMS connector.")
    description: str = Field(description="A description of the LIMS connector.")
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the LIMS system.
        
        Returns:
            Whether the connection was successful.
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the LIMS system.
        
        Returns:
            Whether the disconnection was successful.
        """
        pass
    
    @abstractmethod
    def get_projects(self) -> List[LIMSProject]:
        """Get all projects from the LIMS system.
        
        Returns:
            A list of projects.
        """
        pass
    
    @abstractmethod
    def get_project(self, project_id: str) -> Optional[LIMSProject]:
        """Get a project from the LIMS system.
        
        Args:
            project_id: The ID of the project to get.
            
        Returns:
            The project, or None if not found.
        """
        pass
    
    @abstractmethod
    def create_project(self, project: LIMSProject) -> LIMSProject:
        """Create a project in the LIMS system.
        
        Args:
            project: The project to create.
            
        Returns:
            The created project.
        """
        pass
    
    @abstractmethod
    def update_project(self, project: LIMSProject) -> LIMSProject:
        """Update a project in the LIMS system.
        
        Args:
            project: The project to update.
            
        Returns:
            The updated project.
        """
        pass
    
    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        """Delete a project from the LIMS system.
        
        Args:
            project_id: The ID of the project to delete.
            
        Returns:
            Whether the deletion was successful.
        """
        pass
    
    @abstractmethod
    def get_tasks(self, project_id: Optional[str] = None) -> List[LIMSTask]:
        """Get tasks from the LIMS system.
        
        Args:
            project_id: The ID of the project to get tasks for, or None to get all tasks.
            
        Returns:
            A list of tasks.
        """
        pass
    
    @abstractmethod
    def get_task(self, task_id: str) -> Optional[LIMSTask]:
        """Get a task from the LIMS system.
        
        Args:
            task_id: The ID of the task to get.
            
        Returns:
            The task, or None if not found.
        """
        pass
    
    @abstractmethod
    def create_task(self, task: LIMSTask) -> LIMSTask:
        """Create a task in the LIMS system.
        
        Args:
            task: The task to create.
            
        Returns:
            The created task.
        """
        pass
    
    @abstractmethod
    def update_task(self, task: LIMSTask) -> LIMSTask:
        """Update a task in the LIMS system.
        
        Args:
            task: The task to update.
            
        Returns:
            The updated task.
        """
        pass
    
    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        """Delete a task from the LIMS system.
        
        Args:
            task_id: The ID of the task to delete.
            
        Returns:
            Whether the deletion was successful.
        """
        pass
    
    @abstractmethod
    def get_resources(self) -> List[LIMSResource]:
        """Get all resources from the LIMS system.
        
        Returns:
            A list of resources.
        """
        pass
    
    @abstractmethod
    def get_resource(self, resource_id: str) -> Optional[LIMSResource]:
        """Get a resource from the LIMS system.
        
        Args:
            resource_id: The ID of the resource to get.
            
        Returns:
            The resource, or None if not found.
        """
        pass
    
    @abstractmethod
    def create_resource(self, resource: LIMSResource) -> LIMSResource:
        """Create a resource in the LIMS system.
        
        Args:
            resource: The resource to create.
            
        Returns:
            The created resource.
        """
        pass
    
    @abstractmethod
    def update_resource(self, resource: LIMSResource) -> LIMSResource:
        """Update a resource in the LIMS system.
        
        Args:
            resource: The resource to update.
            
        Returns:
            The updated resource.
        """
        pass
    
    @abstractmethod
    def delete_resource(self, resource_id: str) -> bool:
        """Delete a resource from the LIMS system.
        
        Args:
            resource_id: The ID of the resource to delete.
            
        Returns:
            Whether the deletion was successful.
        """
        pass
