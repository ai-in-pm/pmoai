from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pmoai.agent import Agent
from pmoai.task import Task


class ProjectPlan(BaseModel):
    """Represents a project plan."""
    
    project_name: str = Field(description="The name of the project.")
    project_code: Optional[str] = Field(None, description="The project code.")
    project_description: str = Field(description="A description of the project.")
    project_objectives: List[str] = Field(description="The objectives of the project.")
    project_scope: str = Field(description="The scope of the project.")
    project_timeline: str = Field(description="The timeline of the project.")
    project_budget: Optional[str] = Field(None, description="The budget of the project.")
    project_stakeholders: List[str] = Field(description="The stakeholders of the project.")
    project_risks: List[str] = Field(description="The risks of the project.")
    project_assumptions: List[str] = Field(description="The assumptions of the project.")
    project_constraints: List[str] = Field(description="The constraints of the project.")
    project_deliverables: List[str] = Field(description="The deliverables of the project.")
    project_milestones: List[Dict[str, Any]] = Field(description="The milestones of the project.")
    project_team: List[Dict[str, Any]] = Field(description="The team members of the project.")
    project_communication_plan: Dict[str, Any] = Field(description="The communication plan for the project.")
    project_quality_plan: Optional[Dict[str, Any]] = Field(None, description="The quality plan for the project.")
    project_procurement_plan: Optional[Dict[str, Any]] = Field(None, description="The procurement plan for the project.")


class ProjectPlanner(BaseModel):
    """Plans and manages project planning activities."""
    
    project_manager_agent: Agent = Field(description="The project manager agent.")
    
    def create_project_plan(
        self,
        project_name: str,
        project_description: str,
        project_objectives: List[str],
        **kwargs: Any,
    ) -> ProjectPlan:
        """Create a project plan.
        
        Args:
            project_name: The name of the project.
            project_description: A description of the project.
            project_objectives: The objectives of the project.
            **kwargs: Additional arguments for the project plan.
            
        Returns:
            A project plan.
        """
        # Create a task for the project manager to create a project plan
        planning_task = Task(
            description=f"""
            Create a comprehensive project plan for the project '{project_name}'.
            
            Project Description:
            {project_description}
            
            Project Objectives:
            {"".join([f"- {objective}\\n" for objective in project_objectives])}
            
            Include the following in your project plan:
            - Project scope
            - Project timeline
            - Project budget
            - Project stakeholders
            - Project risks
            - Project assumptions
            - Project constraints
            - Project deliverables
            - Project milestones
            - Project team
            - Project communication plan
            - Project quality plan
            - Project procurement plan
            """,
            expected_output="A comprehensive project plan in JSON format.",
            agent=self.project_manager_agent,
        )
        
        # Execute the task
        result = planning_task.execute()
        
        # Parse the result into a ProjectPlan
        plan_data = result.raw
        
        # Create a ProjectPlan object
        plan = ProjectPlan(
            project_name=project_name,
            project_description=project_description,
            project_objectives=project_objectives,
            **kwargs,
            **plan_data,
        )
        
        return plan
    
    def update_project_plan(
        self, project_plan: ProjectPlan, updates: Dict[str, Any]
    ) -> ProjectPlan:
        """Update a project plan.
        
        Args:
            project_plan: The project plan to update.
            updates: The updates to apply to the project plan.
            
        Returns:
            The updated project plan.
        """
        # Create a task for the project manager to update the project plan
        update_task = Task(
            description=f"""
            Update the project plan for the project '{project_plan.project_name}'.
            
            Current Project Plan:
            {project_plan.json(indent=2)}
            
            Updates to Apply:
            {updates}
            
            Provide the updated project plan in JSON format.
            """,
            expected_output="An updated project plan in JSON format.",
            agent=self.project_manager_agent,
        )
        
        # Execute the task
        result = update_task.execute()
        
        # Parse the result into a ProjectPlan
        updated_plan_data = result.raw
        
        # Create a new ProjectPlan object with the updates
        updated_plan = ProjectPlan(**updated_plan_data)
        
        return updated_plan
    
    def evaluate_project_plan(self, project_plan: ProjectPlan) -> Dict[str, Any]:
        """Evaluate a project plan.
        
        Args:
            project_plan: The project plan to evaluate.
            
        Returns:
            An evaluation of the project plan.
        """
        # Create a task for the project manager to evaluate the project plan
        evaluation_task = Task(
            description=f"""
            Evaluate the project plan for the project '{project_plan.project_name}'.
            
            Project Plan:
            {project_plan.json(indent=2)}
            
            Provide an evaluation of the project plan, including:
            - Strengths
            - Weaknesses
            - Opportunities
            - Threats
            - Recommendations for improvement
            
            Provide your evaluation in JSON format.
            """,
            expected_output="An evaluation of the project plan in JSON format.",
            agent=self.project_manager_agent,
        )
        
        # Execute the task
        result = evaluation_task.execute()
        
        # Parse the result into a dictionary
        evaluation = result.raw
        
        return evaluation
