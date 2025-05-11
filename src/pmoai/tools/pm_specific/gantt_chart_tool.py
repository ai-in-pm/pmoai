from typing import Dict, List, Optional, Type

from pydantic import BaseModel, Field

from pmoai.tools.base_tool import BaseTool


class GanttTask(BaseModel):
    """Model for a task in a Gantt chart."""
    
    id: str = Field(description="A unique identifier for the task (e.g., T-001).")
    name: str = Field(description="The name of the task.")
    start_date: str = Field(description="The start date of the task (YYYY-MM-DD).")
    end_date: str = Field(description="The end date of the task (YYYY-MM-DD).")
    progress: float = Field(description="The progress of the task in percentage (0-100).")
    dependencies: Optional[List[str]] = Field(default=None, description="The IDs of tasks that this task depends on.")
    assignee: Optional[str] = Field(default=None, description="The person assigned to the task.")


class GanttMilestone(BaseModel):
    """Model for a milestone in a Gantt chart."""
    
    id: str = Field(description="A unique identifier for the milestone (e.g., M-001).")
    name: str = Field(description="The name of the milestone.")
    date: str = Field(description="The date of the milestone (YYYY-MM-DD).")
    description: Optional[str] = Field(default=None, description="A description of the milestone.")


class GanttChartInput(BaseModel):
    """Input schema for GanttChartTool."""
    
    project_name: str = Field(description="The name of the project.")
    tasks: List[GanttTask] = Field(description="The list of tasks for the Gantt chart.")
    milestones: Optional[List[GanttMilestone]] = Field(default=None, description="The list of milestones for the Gantt chart.")
    start_date: str = Field(description="The start date of the project (YYYY-MM-DD).")
    end_date: str = Field(description="The end date of the project (YYYY-MM-DD).")


class GanttChartTool(BaseTool):
    """Tool for creating a Gantt chart document."""
    
    name: str = "Gantt Chart Generator"
    description: str = "Creates a text-based Gantt chart document based on provided information."
    args_schema: Type[BaseModel] = GanttChartInput
    
    def _run(
        self,
        project_name: str,
        tasks: List[GanttTask],
        milestones: Optional[List[GanttMilestone]] = None,
        start_date: str = "",
        end_date: str = "",
    ) -> str:
        """Create a text-based Gantt chart document.
        
        Args:
            project_name: The name of the project.
            tasks: The list of tasks for the Gantt chart.
            milestones: The list of milestones for the Gantt chart.
            start_date: The start date of the project.
            end_date: The end date of the project.
            
        Returns:
            A formatted Gantt chart document.
        """
        from datetime import datetime, timedelta
        
        # Parse dates
        project_start = datetime.strptime(start_date, "%Y-%m-%d")
        project_end = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Calculate project duration in days
        project_duration = (project_end - project_start).days + 1
        
        # Create the header of the Gantt chart
        gantt_chart = f"""
# GANTT CHART

## Project Name
{project_name}

## Project Duration
{start_date} to {end_date} ({project_duration} days)

## Tasks and Timeline

"""
        
        # Create a dictionary to store task information
        task_dict: Dict[str, GanttTask] = {task.id: task for task in tasks}
        
        # Sort tasks by start date
        sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x.start_date, "%Y-%m-%d"))
        
        # Add each task to the Gantt chart
        for task in sorted_tasks:
            task_start = datetime.strptime(task.start_date, "%Y-%m-%d")
            task_end = datetime.strptime(task.end_date, "%Y-%m-%d")
            task_duration = (task_end - task_start).days + 1
            
            # Calculate the position of the task in the timeline
            start_offset = (task_start - project_start).days
            
            # Create the task line
            task_line = f"{task.id}: {task.name} "
            if task.assignee:
                task_line += f"[{task.assignee}] "
            task_line += f"({task.start_date} to {task.end_date}, {task_duration} days, {task.progress}% complete)"
            
            # Add dependencies if any
            if task.dependencies:
                dependency_names = []
                for dep_id in task.dependencies:
                    if dep_id in task_dict:
                        dependency_names.append(f"{dep_id}: {task_dict[dep_id].name}")
                if dependency_names:
                    task_line += f"\n   Dependencies: {', '.join(dependency_names)}"
            
            gantt_chart += f"{task_line}\n"
            
            # Create the Gantt bar
            gantt_bar = " " * start_offset
            gantt_bar += "[" + "=" * (task_duration - 2) + "]"
            
            gantt_chart += f"   {gantt_bar}\n\n"
        
        # Add milestones if any
        if milestones:
            gantt_chart += "## Milestones\n\n"
            
            # Sort milestones by date
            sorted_milestones = sorted(milestones, key=lambda x: datetime.strptime(x.date, "%Y-%m-%d"))
            
            for milestone in sorted_milestones:
                milestone_date = datetime.strptime(milestone.date, "%Y-%m-%d")
                
                # Calculate the position of the milestone in the timeline
                milestone_offset = (milestone_date - project_start).days
                
                # Create the milestone line
                milestone_line = f"{milestone.id}: {milestone.name} ({milestone.date})"
                if milestone.description:
                    milestone_line += f" - {milestone.description}"
                
                gantt_chart += f"{milestone_line}\n"
                
                # Create the milestone marker
                milestone_marker = " " * milestone_offset + "◆"
                
                gantt_chart += f"   {milestone_marker}\n\n"
        
        # Add a legend
        gantt_chart += """
## Legend
- [====] : Task duration
- ◆ : Milestone
"""
        
        return gantt_chart
