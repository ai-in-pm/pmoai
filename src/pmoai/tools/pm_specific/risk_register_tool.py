from typing import List, Type

from pydantic import BaseModel, Field

from pmoai.tools.base_tool import BaseTool


class Risk(BaseModel):
    """Model for a project risk."""
    
    id: str = Field(description="A unique identifier for the risk (e.g., R-001).")
    description: str = Field(description="A description of the risk.")
    category: str = Field(description="The category of the risk (e.g., Technical, Schedule, Resource).")
    probability: str = Field(description="The probability of the risk occurring (High, Medium, Low).")
    impact: str = Field(description="The impact if the risk occurs (High, Medium, Low).")
    severity: str = Field(description="The overall severity of the risk (High, Medium, Low).")
    mitigation_strategy: str = Field(description="The strategy to mitigate the risk.")
    contingency_plan: str = Field(description="The plan if the risk occurs.")
    owner: str = Field(description="The person responsible for managing the risk.")
    status: str = Field(description="The current status of the risk (Open, Closed, Mitigated).")


class RiskRegisterInput(BaseModel):
    """Input schema for RiskRegisterTool."""
    
    project_name: str = Field(description="The name of the project.")
    risks: List[Risk] = Field(description="The list of risks for the project.")


class RiskRegisterTool(BaseTool):
    """Tool for creating a risk register document."""
    
    name: str = "Risk Register Generator"
    description: str = "Creates a comprehensive risk register document based on provided information."
    args_schema: Type[BaseModel] = RiskRegisterInput
    
    def _run(
        self,
        project_name: str,
        risks: List[Risk],
    ) -> str:
        """Create a risk register document.
        
        Args:
            project_name: The name of the project.
            risks: The list of risks for the project.
            
        Returns:
            A formatted risk register document.
        """
        # Create the header of the risk register
        risk_register = f"""
# RISK REGISTER

## Project Name
{project_name}

## Date
{self._get_current_date()}

## Risks

| ID | Description | Category | Probability | Impact | Severity | Mitigation Strategy | Contingency Plan | Owner | Status |
|----|-------------|----------|------------|--------|----------|---------------------|------------------|-------|--------|
"""
        
        # Add each risk to the register
        for risk in risks:
            risk_register += f"| {risk.id} | {risk.description} | {risk.category} | {risk.probability} | {risk.impact} | {risk.severity} | {risk.mitigation_strategy} | {risk.contingency_plan} | {risk.owner} | {risk.status} |\n"
        
        return risk_register
    
    def _get_current_date(self) -> str:
        """Get the current date in YYYY-MM-DD format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
