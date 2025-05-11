from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, Field

from pmoai.agent import Agent
from pmoai.collaboration.collaboration_strategy import (
    AgileCollaborationStrategy,
    BaseCollaborationStrategy,
    HybridCollaborationStrategy,
    KanbanCollaborationStrategy,
    SequentialCollaborationStrategy,
    WaterfallCollaborationStrategy,
)


class TeamMember(BaseModel):
    """Represents a team member in a project."""
    
    id: str = Field(description="The team member identifier.")
    name: str = Field(description="The name of the team member.")
    role: str = Field(description="The role of the team member.")
    skills: List[str] = Field(default_factory=list, description="The skills of the team member.")
    availability: float = Field(description="The availability percentage (0-100).")
    agent: Optional[Agent] = Field(None, description="The agent representing this team member.")


class TeamCollaboration(BaseModel):
    """Facilitates collaboration within a project team."""
    
    project_name: str = Field(description="The name of the project.")
    project_code: Optional[str] = Field(None, description="The project code.")
    team_members: List[TeamMember] = Field(default_factory=list, description="The list of team members.")
    collaboration_strategy: BaseCollaborationStrategy = Field(
        default_factory=SequentialCollaborationStrategy,
        description="The collaboration strategy to use."
    )
    
    def add_team_member(self, team_member: TeamMember) -> None:
        """Add a team member to the collaboration.
        
        Args:
            team_member: The team member to add.
        """
        self.team_members.append(team_member)
    
    def remove_team_member(self, team_member_id: str) -> None:
        """Remove a team member from the collaboration.
        
        Args:
            team_member_id: The ID of the team member to remove.
        """
        self.team_members = [tm for tm in self.team_members if tm.id != team_member_id]
    
    def get_team_member(self, team_member_id: str) -> Optional[TeamMember]:
        """Get a team member by ID.
        
        Args:
            team_member_id: The ID of the team member to get.
            
        Returns:
            The team member, or None if not found.
        """
        for team_member in self.team_members:
            if team_member.id == team_member_id:
                return team_member
        return None
    
    def set_collaboration_strategy(
        self, strategy_type: Type[BaseCollaborationStrategy], **kwargs: Any
    ) -> None:
        """Set the collaboration strategy.
        
        Args:
            strategy_type: The type of collaboration strategy to use.
            **kwargs: Additional arguments to pass to the strategy constructor.
        """
        self.collaboration_strategy = strategy_type(**kwargs)
    
    def collaborate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Facilitate collaboration between team members.
        
        Args:
            context: The context for the collaboration.
            
        Returns:
            The result of the collaboration.
        """
        # Extract agents from team members
        agents = [tm.agent for tm in self.team_members if tm.agent is not None]
        
        # Use the collaboration strategy to facilitate collaboration
        return self.collaboration_strategy.facilitate_collaboration(agents, context)
    
    def create_team_roster(self) -> Dict[str, Any]:
        """Create a team roster.
        
        Returns:
            A team roster.
        """
        roster = {
            "project_name": self.project_name,
            "project_code": self.project_code,
            "team_members": [],
        }
        
        for team_member in self.team_members:
            member_info = {
                "id": team_member.id,
                "name": team_member.name,
                "role": team_member.role,
                "skills": team_member.skills,
                "availability": team_member.availability,
            }
            roster["team_members"].append(member_info)
        
        return roster
    
    def find_team_members_by_skill(self, skill: str) -> List[TeamMember]:
        """Find team members with a specific skill.
        
        Args:
            skill: The skill to search for.
            
        Returns:
            A list of team members with the specified skill.
        """
        return [tm for tm in self.team_members if skill in tm.skills]
    
    def get_available_collaboration_strategies(self) -> Dict[str, Type[BaseCollaborationStrategy]]:
        """Get the available collaboration strategies.
        
        Returns:
            A dictionary mapping strategy names to strategy types.
        """
        return {
            "sequential": SequentialCollaborationStrategy,
            "agile": AgileCollaborationStrategy,
            "waterfall": WaterfallCollaborationStrategy,
            "kanban": KanbanCollaborationStrategy,
            "hybrid": HybridCollaborationStrategy,
        }
