from typing import Type

from pydantic import BaseModel, Field

from pmoai.tools.base_tool import BaseTool


class ProjectCharterInput(BaseModel):
    """Input schema for ProjectCharterTool."""
    
    project_name: str = Field(
        description="The name of the project."
    )
    project_purpose: str = Field(
        description="The purpose and justification of the project."
    )
    project_objectives: str = Field(
        description="The measurable objectives of the project."
    )
    project_scope: str = Field(
        description="The scope of the project, including what is in and out of scope."
    )
    project_stakeholders: str = Field(
        description="The key stakeholders of the project."
    )
    project_timeline: str = Field(
        description="The high-level timeline of the project."
    )
    project_budget: str = Field(
        description="The estimated budget for the project."
    )
    project_risks: str = Field(
        description="The high-level risks of the project."
    )
    project_success_criteria: str = Field(
        description="The criteria for project success."
    )


class ProjectCharterTool(BaseTool):
    """Tool for creating a project charter document."""
    
    name: str = "Project Charter Generator"
    description: str = "Creates a comprehensive project charter document based on provided information."
    args_schema: Type[BaseModel] = ProjectCharterInput
    
    def _run(
        self,
        project_name: str,
        project_purpose: str,
        project_objectives: str,
        project_scope: str,
        project_stakeholders: str,
        project_timeline: str,
        project_budget: str,
        project_risks: str,
        project_success_criteria: str,
    ) -> str:
        """Create a project charter document.
        
        Args:
            project_name: The name of the project.
            project_purpose: The purpose and justification of the project.
            project_objectives: The measurable objectives of the project.
            project_scope: The scope of the project.
            project_stakeholders: The key stakeholders of the project.
            project_timeline: The high-level timeline of the project.
            project_budget: The estimated budget for the project.
            project_risks: The high-level risks of the project.
            project_success_criteria: The criteria for project success.
            
        Returns:
            A formatted project charter document.
        """
        charter = f"""
# PROJECT CHARTER

## Project Name
{project_name}

## Project Purpose
{project_purpose}

## Project Objectives
{project_objectives}

## Project Scope
### In Scope
{project_scope}

## Key Stakeholders
{project_stakeholders}

## Timeline
{project_timeline}

## Budget
{project_budget}

## High-Level Risks
{project_risks}

## Success Criteria
{project_success_criteria}

## Approvals
- Project Sponsor: ______________________ Date: __________
- Project Manager: ______________________ Date: __________
- Key Stakeholder: ______________________ Date: __________
"""
        return charter
