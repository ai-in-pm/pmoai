from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pmoai.agent import Agent
from pmoai.task import Task


class Risk(BaseModel):
    """Represents a project risk."""
    
    id: str = Field(description="The risk identifier.")
    description: str = Field(description="A description of the risk.")
    category: str = Field(description="The category of the risk (e.g., 'technical', 'schedule', 'resource').")
    probability: str = Field(description="The probability of the risk occurring (High, Medium, Low).")
    impact: str = Field(description="The impact if the risk occurs (High, Medium, Low).")
    severity: str = Field(description="The overall severity of the risk (High, Medium, Low).")
    mitigation_strategy: str = Field(description="The strategy to mitigate the risk.")
    contingency_plan: str = Field(description="The plan if the risk occurs.")
    owner: str = Field(description="The person responsible for managing the risk.")
    status: str = Field(description="The current status of the risk (Open, Closed, Mitigated).")


class RiskPlan(BaseModel):
    """Represents a risk management plan."""
    
    project_name: str = Field(description="The name of the project.")
    project_code: Optional[str] = Field(None, description="The project code.")
    risks: List[Risk] = Field(description="The risks identified for the project.")
    risk_management_approach: str = Field(description="The approach to risk management for the project.")
    risk_categories: List[str] = Field(description="The categories of risks for the project.")
    risk_probability_definitions: Dict[str, str] = Field(description="The definitions of risk probability levels.")
    risk_impact_definitions: Dict[str, str] = Field(description="The definitions of risk impact levels.")
    risk_severity_matrix: Dict[str, Dict[str, str]] = Field(description="The risk severity matrix.")
    risk_thresholds: Dict[str, Any] = Field(description="The risk thresholds for the project.")


class RiskPlanner(BaseModel):
    """Plans and manages project risks."""
    
    risk_analyst_agent: Agent = Field(description="The risk analyst agent.")
    
    def create_risk_plan(
        self,
        project_name: str,
        project_description: str,
        project_code: Optional[str] = None,
    ) -> RiskPlan:
        """Create a risk management plan.
        
        Args:
            project_name: The name of the project.
            project_description: A description of the project.
            project_code: The project code.
            
        Returns:
            A risk management plan.
        """
        # Create a task for the risk analyst to create a risk management plan
        planning_task = Task(
            description=f"""
            Create a comprehensive risk management plan for the project '{project_name}'.
            
            Project Description:
            {project_description}
            
            Project Code: {project_code or 'N/A'}
            
            Include the following in your risk management plan:
            - Risk management approach
            - Risk categories
            - Risk probability definitions
            - Risk impact definitions
            - Risk severity matrix
            - Risk thresholds
            - Initial risk register with at least 10 potential risks
            
            Provide your risk management plan in JSON format.
            """,
            expected_output="A comprehensive risk management plan in JSON format.",
            agent=self.risk_analyst_agent,
        )
        
        # Execute the task
        result = planning_task.execute()
        
        # Parse the result into a RiskPlan
        plan_data = result.raw
        
        # Create a RiskPlan object
        plan = RiskPlan(
            project_name=project_name,
            project_code=project_code,
            **plan_data,
        )
        
        return plan
    
    def identify_risks(
        self,
        project_name: str,
        project_description: str,
        project_code: Optional[str] = None,
        existing_risks: Optional[List[Risk]] = None,
    ) -> List[Risk]:
        """Identify risks for a project.
        
        Args:
            project_name: The name of the project.
            project_description: A description of the project.
            project_code: The project code.
            existing_risks: Existing risks for the project.
            
        Returns:
            A list of identified risks.
        """
        # Create a task for the risk analyst to identify risks
        identification_task = Task(
            description=f"""
            Identify risks for the project '{project_name}'.
            
            Project Description:
            {project_description}
            
            Project Code: {project_code or 'N/A'}
            
            Existing Risks:
            {existing_risks or 'No existing risks.'}
            
            Identify at least 5 new potential risks for the project, including:
            - Risk description
            - Risk category
            - Risk probability
            - Risk impact
            - Risk severity
            - Mitigation strategy
            - Contingency plan
            - Risk owner
            - Risk status
            
            Provide your identified risks in JSON format.
            """,
            expected_output="A list of identified risks in JSON format.",
            agent=self.risk_analyst_agent,
        )
        
        # Execute the task
        result = identification_task.execute()
        
        # Parse the result into a list of Risk objects
        risks_data = result.raw
        
        # Create Risk objects
        risks = [Risk(**risk_data) for risk_data in risks_data]
        
        return risks
    
    def analyze_risks(self, risks: List[Risk]) -> Dict[str, Any]:
        """Analyze risks for a project.
        
        Args:
            risks: The risks to analyze.
            
        Returns:
            An analysis of the risks.
        """
        # Create a task for the risk analyst to analyze risks
        analysis_task = Task(
            description=f"""
            Analyze the following risks:
            
            {[risk.json(indent=2) for risk in risks]}
            
            Provide an analysis of the risks, including:
            - Overall risk profile
            - Top risks by severity
            - Risk distribution by category
            - Risk distribution by probability
            - Risk distribution by impact
            - Risk distribution by status
            - Recommendations for risk management
            
            Provide your analysis in JSON format.
            """,
            expected_output="An analysis of risks in JSON format.",
            agent=self.risk_analyst_agent,
        )
        
        # Execute the task
        result = analysis_task.execute()
        
        # Parse the result into a dictionary
        analysis = result.raw
        
        return analysis
