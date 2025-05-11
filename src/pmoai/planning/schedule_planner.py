from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pmoai.agent import Agent
from pmoai.task import Task


class ScheduleTask(BaseModel):
    """Represents a task in a project schedule."""
    
    id: str = Field(description="The task identifier.")
    name: str = Field(description="The name of the task.")
    description: str = Field(description="A description of the task.")
    start_date: str = Field(description="The start date of the task.")
    end_date: str = Field(description="The end date of the task.")
    duration: int = Field(description="The duration of the task in days.")
    dependencies: List[str] = Field(default_factory=list, description="The dependencies of the task.")
    resources: List[str] = Field(default_factory=list, description="The resources assigned to the task.")
    progress: float = Field(default=0.0, description="The progress of the task (0-100).")
    status: str = Field(default="Not Started", description="The status of the task.")


class Milestone(BaseModel):
    """Represents a milestone in a project schedule."""
    
    id: str = Field(description="The milestone identifier.")
    name: str = Field(description="The name of the milestone.")
    description: str = Field(description="A description of the milestone.")
    date: str = Field(description="The date of the milestone.")
    dependencies: List[str] = Field(default_factory=list, description="The dependencies of the milestone.")
    status: str = Field(default="Not Started", description="The status of the milestone.")


class Schedule(BaseModel):
    """Represents a project schedule."""
    
    project_name: str = Field(description="The name of the project.")
    project_code: Optional[str] = Field(None, description="The project code.")
    start_date: str = Field(description="The start date of the project.")
    end_date: str = Field(description="The end date of the project.")
    tasks: List[ScheduleTask] = Field(description="The tasks in the project schedule.")
    milestones: List[Milestone] = Field(description="The milestones in the project schedule.")
    critical_path: List[str] = Field(description="The critical path of the project schedule.")


class SchedulePlanner(BaseModel):
    """Plans and manages project schedules."""
    
    project_manager_agent: Agent = Field(description="The project manager agent.")
    
    def create_schedule(
        self,
        project_name: str,
        project_description: str,
        start_date: str,
        project_code: Optional[str] = None,
    ) -> Schedule:
        """Create a project schedule.
        
        Args:
            project_name: The name of the project.
            project_description: A description of the project.
            start_date: The start date of the project.
            project_code: The project code.
            
        Returns:
            A project schedule.
        """
        # Create a task for the project manager to create a schedule
        planning_task = Task(
            description=f"""
            Create a comprehensive project schedule for the project '{project_name}'.
            
            Project Description:
            {project_description}
            
            Project Code: {project_code or 'N/A'}
            
            Project Start Date: {start_date}
            
            Include the following in your project schedule:
            - Project end date
            - Tasks with start dates, end dates, and durations
            - Task dependencies
            - Milestones
            - Critical path
            
            Provide your project schedule in JSON format.
            """,
            expected_output="A comprehensive project schedule in JSON format.",
            agent=self.project_manager_agent,
        )
        
        # Execute the task
        result = planning_task.execute()
        
        # Parse the result into a Schedule
        schedule_data = result.raw
        
        # Create a Schedule object
        schedule = Schedule(
            project_name=project_name,
            project_code=project_code,
            start_date=start_date,
            **schedule_data,
        )
        
        return schedule
    
    def update_schedule(
        self, schedule: Schedule, updates: Dict[str, Any]
    ) -> Schedule:
        """Update a project schedule.
        
        Args:
            schedule: The project schedule to update.
            updates: The updates to apply to the schedule.
            
        Returns:
            The updated project schedule.
        """
        # Create a task for the project manager to update the schedule
        update_task = Task(
            description=f"""
            Update the project schedule for the project '{schedule.project_name}'.
            
            Current Schedule:
            {schedule.json(indent=2)}
            
            Updates to Apply:
            {updates}
            
            Provide the updated project schedule in JSON format.
            """,
            expected_output="An updated project schedule in JSON format.",
            agent=self.project_manager_agent,
        )
        
        # Execute the task
        result = update_task.execute()
        
        # Parse the result into a Schedule
        updated_schedule_data = result.raw
        
        # Create a new Schedule object with the updates
        updated_schedule = Schedule(**updated_schedule_data)
        
        return updated_schedule
    
    def analyze_schedule(self, schedule: Schedule) -> Dict[str, Any]:
        """Analyze a project schedule.
        
        Args:
            schedule: The project schedule to analyze.
            
        Returns:
            An analysis of the project schedule.
        """
        # Create a task for the project manager to analyze the schedule
        analysis_task = Task(
            description=f"""
            Analyze the project schedule for the project '{schedule.project_name}'.
            
            Schedule:
            {schedule.json(indent=2)}
            
            Provide an analysis of the project schedule, including:
            - Project duration
            - Critical path analysis
            - Schedule risks
            - Resource utilization
            - Schedule compression opportunities
            - Schedule quality assessment
            - Recommendations for improvement
            
            Provide your analysis in JSON format.
            """,
            expected_output="An analysis of the project schedule in JSON format.",
            agent=self.project_manager_agent,
        )
        
        # Execute the task
        result = analysis_task.execute()
        
        # Parse the result into a dictionary
        analysis = result.raw
        
        return analysis
    
    def generate_gantt_chart(self, schedule: Schedule) -> str:
        """Generate a Gantt chart for a project schedule.
        
        Args:
            schedule: The project schedule to generate a Gantt chart for.
            
        Returns:
            A text-based Gantt chart.
        """
        # Create a task for the project manager to generate a Gantt chart
        gantt_task = Task(
            description=f"""
            Generate a text-based Gantt chart for the project '{schedule.project_name}'.
            
            Schedule:
            {schedule.json(indent=2)}
            
            Create a text-based Gantt chart showing:
            - Tasks and their durations
            - Task dependencies
            - Milestones
            - Critical path
            - Current date indicator
            
            Use ASCII characters to create the Gantt chart.
            """,
            expected_output="A text-based Gantt chart.",
            agent=self.project_manager_agent,
        )
        
        # Execute the task
        result = gantt_task.execute()
        
        # Return the Gantt chart
        return result.raw
