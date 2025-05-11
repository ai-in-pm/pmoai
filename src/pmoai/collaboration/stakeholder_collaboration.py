from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pmoai.event_listeners.pm_events import StakeholderCommunicationEvent


class Stakeholder(BaseModel):
    """Represents a project stakeholder."""
    
    id: str = Field(description="The stakeholder identifier.")
    name: str = Field(description="The name of the stakeholder.")
    role: str = Field(description="The role of the stakeholder.")
    influence: str = Field(description="The level of influence (High, Medium, Low).")
    interest: str = Field(description="The level of interest (High, Medium, Low).")
    communication_preference: str = Field(description="The preferred communication method.")
    communication_frequency: str = Field(description="The preferred communication frequency.")


class StakeholderCollaboration(BaseModel):
    """Facilitates collaboration with project stakeholders."""
    
    project_name: str = Field(description="The name of the project.")
    project_code: Optional[str] = Field(None, description="The project code.")
    stakeholders: List[Stakeholder] = Field(default_factory=list, description="The list of stakeholders.")
    
    def add_stakeholder(self, stakeholder: Stakeholder) -> None:
        """Add a stakeholder to the collaboration.
        
        Args:
            stakeholder: The stakeholder to add.
        """
        self.stakeholders.append(stakeholder)
    
    def remove_stakeholder(self, stakeholder_id: str) -> None:
        """Remove a stakeholder from the collaboration.
        
        Args:
            stakeholder_id: The ID of the stakeholder to remove.
        """
        self.stakeholders = [s for s in self.stakeholders if s.id != stakeholder_id]
    
    def get_stakeholder(self, stakeholder_id: str) -> Optional[Stakeholder]:
        """Get a stakeholder by ID.
        
        Args:
            stakeholder_id: The ID of the stakeholder to get.
            
        Returns:
            The stakeholder, or None if not found.
        """
        for stakeholder in self.stakeholders:
            if stakeholder.id == stakeholder_id:
                return stakeholder
        return None
    
    def communicate(
        self, stakeholder_id: str, communication_type: str, message: str
    ) -> StakeholderCommunicationEvent:
        """Communicate with a stakeholder.
        
        Args:
            stakeholder_id: The ID of the stakeholder to communicate with.
            communication_type: The type of communication.
            message: The communication message.
            
        Returns:
            A StakeholderCommunicationEvent.
            
        Raises:
            ValueError: If the stakeholder is not found.
        """
        stakeholder = self.get_stakeholder(stakeholder_id)
        if not stakeholder:
            raise ValueError(f"Stakeholder with ID {stakeholder_id} not found")
        
        # Create and return a communication event
        event = StakeholderCommunicationEvent(
            project_name=self.project_name,
            project_code=self.project_code,
            timestamp=self._get_current_timestamp(),
            stakeholder=stakeholder.name,
            communication_type=communication_type,
            message=message,
        )
        
        return event
    
    def create_stakeholder_matrix(self) -> Dict[str, List[Stakeholder]]:
        """Create a stakeholder matrix based on influence and interest.
        
        Returns:
            A dictionary mapping quadrants to stakeholders.
        """
        matrix = {
            "high_influence_high_interest": [],
            "high_influence_low_interest": [],
            "low_influence_high_interest": [],
            "low_influence_low_interest": [],
        }
        
        for stakeholder in self.stakeholders:
            if stakeholder.influence.lower() == "high" and stakeholder.interest.lower() == "high":
                matrix["high_influence_high_interest"].append(stakeholder)
            elif stakeholder.influence.lower() == "high" and stakeholder.interest.lower() == "low":
                matrix["high_influence_low_interest"].append(stakeholder)
            elif stakeholder.influence.lower() == "low" and stakeholder.interest.lower() == "high":
                matrix["low_influence_high_interest"].append(stakeholder)
            else:
                matrix["low_influence_low_interest"].append(stakeholder)
        
        return matrix
    
    def create_communication_plan(self) -> Dict[str, Any]:
        """Create a communication plan for all stakeholders.
        
        Returns:
            A communication plan.
        """
        plan = {
            "project_name": self.project_name,
            "project_code": self.project_code,
            "stakeholders": [],
        }
        
        for stakeholder in self.stakeholders:
            stakeholder_plan = {
                "id": stakeholder.id,
                "name": stakeholder.name,
                "role": stakeholder.role,
                "communication_preference": stakeholder.communication_preference,
                "communication_frequency": stakeholder.communication_frequency,
                "engagement_strategy": self._determine_engagement_strategy(stakeholder),
            }
            plan["stakeholders"].append(stakeholder_plan)
        
        return plan
    
    def _determine_engagement_strategy(self, stakeholder: Stakeholder) -> str:
        """Determine the engagement strategy for a stakeholder.
        
        Args:
            stakeholder: The stakeholder to determine the strategy for.
            
        Returns:
            The engagement strategy.
        """
        if stakeholder.influence.lower() == "high" and stakeholder.interest.lower() == "high":
            return "Manage Closely"
        elif stakeholder.influence.lower() == "high" and stakeholder.interest.lower() == "low":
            return "Keep Satisfied"
        elif stakeholder.influence.lower() == "low" and stakeholder.interest.lower() == "high":
            return "Keep Informed"
        else:
            return "Monitor"
    
    def _get_current_timestamp(self) -> str:
        """Get the current timestamp in ISO format.
        
        Returns:
            The current timestamp.
        """
        from datetime import datetime
        return datetime.now().isoformat()
