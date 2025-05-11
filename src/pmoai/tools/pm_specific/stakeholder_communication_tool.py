from typing import List, Optional, Type

from pydantic import BaseModel, Field

from pmoai.tools.base_tool import BaseTool


class Stakeholder(BaseModel):
    """Model for a project stakeholder."""
    
    id: str = Field(description="A unique identifier for the stakeholder (e.g., S-001).")
    name: str = Field(description="The name of the stakeholder.")
    role: str = Field(description="The role of the stakeholder.")
    organization: str = Field(description="The organization of the stakeholder.")
    influence: str = Field(description="The level of influence of the stakeholder (High, Medium, Low).")
    interest: str = Field(description="The level of interest of the stakeholder (High, Medium, Low).")
    communication_preference: str = Field(description="The preferred communication method of the stakeholder.")
    communication_frequency: str = Field(description="The preferred communication frequency of the stakeholder.")
    key_concerns: Optional[List[str]] = Field(default=None, description="The key concerns of the stakeholder.")
    expectations: Optional[List[str]] = Field(default=None, description="The expectations of the stakeholder.")


class CommunicationPlan(BaseModel):
    """Model for a communication plan."""
    
    stakeholder_id: str = Field(description="The ID of the stakeholder.")
    communication_type: str = Field(description="The type of communication (e.g., Status Report, Meeting, Presentation).")
    frequency: str = Field(description="The frequency of the communication (e.g., Weekly, Monthly, Ad-hoc).")
    method: str = Field(description="The method of communication (e.g., Email, Meeting, Phone Call).")
    responsible: str = Field(description="The person responsible for the communication.")
    content: str = Field(description="The content of the communication.")
    purpose: str = Field(description="The purpose of the communication.")


class StakeholderCommunicationInput(BaseModel):
    """Input schema for StakeholderCommunicationTool."""
    
    project_name: str = Field(description="The name of the project.")
    stakeholders: List[Stakeholder] = Field(description="The list of stakeholders for the project.")
    communication_plans: List[CommunicationPlan] = Field(description="The list of communication plans for the project.")


class StakeholderCommunicationTool(BaseTool):
    """Tool for creating a stakeholder communication plan document."""
    
    name: str = "Stakeholder Communication Plan Generator"
    description: str = "Creates a comprehensive stakeholder communication plan document based on provided information."
    args_schema: Type[BaseModel] = StakeholderCommunicationInput
    
    def _run(
        self,
        project_name: str,
        stakeholders: List[Stakeholder],
        communication_plans: List[CommunicationPlan],
    ) -> str:
        """Create a stakeholder communication plan document.
        
        Args:
            project_name: The name of the project.
            stakeholders: The list of stakeholders for the project.
            communication_plans: The list of communication plans for the project.
            
        Returns:
            A formatted stakeholder communication plan document.
        """
        # Create stakeholder lookup dictionary
        stakeholder_lookup = {s.id: s for s in stakeholders}
        
        # Create the header of the stakeholder communication plan
        communication_plan = f"""
# STAKEHOLDER COMMUNICATION PLAN

## Project Name
{project_name}

## Date
{self._get_current_date()}

## Stakeholders

| ID | Name | Role | Organization | Influence | Interest | Communication Preference | Communication Frequency |
|----|------|------|-------------|-----------|---------|--------------------------|------------------------|
"""
        
        # Add each stakeholder to the document
        for stakeholder in stakeholders:
            communication_plan += f"| {stakeholder.id} | {stakeholder.name} | {stakeholder.role} | {stakeholder.organization} | {stakeholder.influence} | {stakeholder.interest} | {stakeholder.communication_preference} | {stakeholder.communication_frequency} |\n"
        
        # Add stakeholder analysis section
        communication_plan += """
## Stakeholder Analysis

### High Influence, High Interest (Manage Closely)
"""
        
        # Add stakeholders with high influence and high interest
        high_high = [s for s in stakeholders if s.influence.lower() == "high" and s.interest.lower() == "high"]
        if high_high:
            for stakeholder in high_high:
                communication_plan += f"- {stakeholder.name} ({stakeholder.role}, {stakeholder.organization})\n"
        else:
            communication_plan += "- None\n"
        
        communication_plan += """
### High Influence, Low Interest (Keep Satisfied)
"""
        
        # Add stakeholders with high influence and low interest
        high_low = [s for s in stakeholders if s.influence.lower() == "high" and s.interest.lower() == "low"]
        if high_low:
            for stakeholder in high_low:
                communication_plan += f"- {stakeholder.name} ({stakeholder.role}, {stakeholder.organization})\n"
        else:
            communication_plan += "- None\n"
        
        communication_plan += """
### Low Influence, High Interest (Keep Informed)
"""
        
        # Add stakeholders with low influence and high interest
        low_high = [s for s in stakeholders if s.influence.lower() == "low" and s.interest.lower() == "high"]
        if low_high:
            for stakeholder in low_high:
                communication_plan += f"- {stakeholder.name} ({stakeholder.role}, {stakeholder.organization})\n"
        else:
            communication_plan += "- None\n"
        
        communication_plan += """
### Low Influence, Low Interest (Monitor)
"""
        
        # Add stakeholders with low influence and low interest
        low_low = [s for s in stakeholders if s.influence.lower() == "low" and s.interest.lower() == "low"]
        if low_low:
            for stakeholder in low_low:
                communication_plan += f"- {stakeholder.name} ({stakeholder.role}, {stakeholder.organization})\n"
        else:
            communication_plan += "- None\n"
        
        # Add communication plan section
        communication_plan += """
## Communication Plan

| Stakeholder | Communication Type | Frequency | Method | Responsible | Content | Purpose |
|------------|-------------------|-----------|--------|------------|---------|---------|
"""
        
        # Add each communication plan to the document
        for plan in communication_plans:
            stakeholder_name = stakeholder_lookup[plan.stakeholder_id].name if plan.stakeholder_id in stakeholder_lookup else "Unknown"
            communication_plan += f"| {stakeholder_name} | {plan.communication_type} | {plan.frequency} | {plan.method} | {plan.responsible} | {plan.content} | {plan.purpose} |\n"
        
        return communication_plan
    
    def _get_current_date(self) -> str:
        """Get the current date in YYYY-MM-DD format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
