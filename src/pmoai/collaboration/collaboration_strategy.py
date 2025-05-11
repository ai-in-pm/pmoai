from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BaseCollaborationStrategy(BaseModel, ABC):
    """Base class for collaboration strategies in PMOAI.
    
    This class defines the interface for collaboration strategies between agents.
    """
    
    name: str = Field(description="The name of the collaboration strategy.")
    description: str = Field(description="A description of the collaboration strategy.")
    
    @abstractmethod
    def facilitate_collaboration(
        self, agents: List[Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Facilitate collaboration between agents.
        
        Args:
            agents: The list of agents to facilitate collaboration between.
            context: The context for the collaboration.
            
        Returns:
            The result of the collaboration.
        """
        pass


class SequentialCollaborationStrategy(BaseCollaborationStrategy):
    """Sequential collaboration strategy.
    
    In this strategy, agents collaborate in a sequential manner, with each agent
    building on the work of the previous agent.
    """
    
    name: str = Field(default="Sequential Collaboration")
    description: str = Field(
        default="Agents collaborate in a sequential manner, with each agent building on the work of the previous agent."
    )
    
    def facilitate_collaboration(
        self, agents: List[Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Facilitate sequential collaboration between agents.
        
        Args:
            agents: The list of agents to facilitate collaboration between.
            context: The context for the collaboration.
            
        Returns:
            The result of the collaboration.
        """
        result = context.copy()
        
        for agent in agents:
            # Each agent processes the result of the previous agent
            agent_result = agent.process(result)
            result.update(agent_result)
        
        return result


class AgileCollaborationStrategy(BaseCollaborationStrategy):
    """Agile collaboration strategy.
    
    In this strategy, agents collaborate in an agile manner, with frequent
    interactions and adaptations.
    """
    
    name: str = Field(default="Agile Collaboration")
    description: str = Field(
        default="Agents collaborate in an agile manner, with frequent interactions and adaptations."
    )
    sprint_length: int = Field(default=2, description="The length of each sprint in weeks.")
    
    def facilitate_collaboration(
        self, agents: List[Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Facilitate agile collaboration between agents.
        
        Args:
            agents: The list of agents to facilitate collaboration between.
            context: The context for the collaboration.
            
        Returns:
            The result of the collaboration.
        """
        result = context.copy()
        
        # Simulate sprints
        num_sprints = context.get("num_sprints", 3)
        
        for sprint in range(1, num_sprints + 1):
            sprint_result = {"sprint": sprint}
            
            # Each agent contributes to the sprint
            for agent in agents:
                agent_result = agent.process(result)
                sprint_result.update(agent_result)
            
            # Sprint retrospective
            retrospective = self._conduct_retrospective(agents, sprint_result)
            sprint_result["retrospective"] = retrospective
            
            # Update the overall result
            result[f"sprint_{sprint}"] = sprint_result
        
        return result
    
    def _conduct_retrospective(self, agents: List[Any], sprint_result: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct a sprint retrospective.
        
        Args:
            agents: The list of agents involved in the sprint.
            sprint_result: The result of the sprint.
            
        Returns:
            The retrospective findings.
        """
        # Simulate a retrospective
        return {
            "what_went_well": "Team collaboration was effective",
            "what_could_be_improved": "Communication could be more frequent",
            "action_items": ["Increase daily check-ins", "Improve documentation"]
        }


class WaterfallCollaborationStrategy(BaseCollaborationStrategy):
    """Waterfall collaboration strategy.
    
    In this strategy, agents collaborate in a waterfall manner, with distinct
    phases and formal handoffs.
    """
    
    name: str = Field(default="Waterfall Collaboration")
    description: str = Field(
        default="Agents collaborate in a waterfall manner, with distinct phases and formal handoffs."
    )
    phases: List[str] = Field(
        default=["requirements", "design", "implementation", "verification", "maintenance"],
        description="The phases of the waterfall process."
    )
    
    def facilitate_collaboration(
        self, agents: List[Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Facilitate waterfall collaboration between agents.
        
        Args:
            agents: The list of agents to facilitate collaboration between.
            context: The context for the collaboration.
            
        Returns:
            The result of the collaboration.
        """
        result = context.copy()
        
        # Assign agents to phases (assuming equal distribution)
        agents_per_phase = max(1, len(agents) // len(self.phases))
        
        for i, phase in enumerate(self.phases):
            phase_result = {"phase": phase}
            
            # Determine which agents work on this phase
            start_idx = i * agents_per_phase
            end_idx = min(start_idx + agents_per_phase, len(agents))
            phase_agents = agents[start_idx:end_idx]
            
            # Each agent in this phase contributes
            for agent in phase_agents:
                agent_result = agent.process(result)
                phase_result.update(agent_result)
            
            # Formal phase approval
            phase_result["approved"] = True
            phase_result["approval_date"] = "2023-01-01"  # Placeholder
            
            # Update the overall result
            result[f"phase_{phase}"] = phase_result
        
        return result


class KanbanCollaborationStrategy(BaseCollaborationStrategy):
    """Kanban collaboration strategy.
    
    In this strategy, agents collaborate using a Kanban approach, with work
    items flowing through stages based on capacity.
    """
    
    name: str = Field(default="Kanban Collaboration")
    description: str = Field(
        default="Agents collaborate using a Kanban approach, with work items flowing through stages based on capacity."
    )
    stages: List[str] = Field(
        default=["backlog", "in_progress", "review", "done"],
        description="The stages of the Kanban board."
    )
    
    def facilitate_collaboration(
        self, agents: List[Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Facilitate Kanban collaboration between agents.
        
        Args:
            agents: The list of agents to facilitate collaboration between.
            context: The context for the collaboration.
            
        Returns:
            The result of the collaboration.
        """
        result = context.copy()
        
        # Initialize Kanban board
        board = {stage: [] for stage in self.stages}
        
        # Create work items (assuming they come from context)
        work_items = context.get("work_items", [{"id": 1, "description": "Sample work item"}])
        
        # Initially, all work items are in the backlog
        board["backlog"] = work_items.copy()
        
        # Simulate work flowing through the Kanban board
        for agent in agents:
            # Agent pulls work from the previous stage to their assigned stage
            agent_stage = agent.get_assigned_stage()
            previous_stage = self._get_previous_stage(agent_stage)
            
            if previous_stage and board[previous_stage]:
                # Pull work from previous stage
                work_item = board[previous_stage].pop(0)
                
                # Process the work item
                processed_item = agent.process(work_item)
                
                # Move to the next stage
                board[agent_stage].append(processed_item)
        
        # Update the result with the final board state
        result["kanban_board"] = board
        
        return result
    
    def _get_previous_stage(self, stage: str) -> Optional[str]:
        """Get the previous stage in the Kanban flow.
        
        Args:
            stage: The current stage.
            
        Returns:
            The previous stage, or None if there is no previous stage.
        """
        try:
            idx = self.stages.index(stage)
            return self.stages[idx - 1] if idx > 0 else None
        except ValueError:
            return None


class HybridCollaborationStrategy(BaseCollaborationStrategy):
    """Hybrid collaboration strategy.
    
    In this strategy, agents collaborate using a hybrid approach that combines
    elements of both Agile and Waterfall methodologies.
    """
    
    name: str = Field(default="Hybrid Collaboration")
    description: str = Field(
        default="Agents collaborate using a hybrid approach that combines elements of both Agile and Waterfall methodologies."
    )
    
    def facilitate_collaboration(
        self, agents: List[Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Facilitate hybrid collaboration between agents.
        
        Args:
            agents: The list of agents to facilitate collaboration between.
            context: The context for the collaboration.
            
        Returns:
            The result of the collaboration.
        """
        result = context.copy()
        
        # Use Waterfall for planning and requirements
        waterfall_strategy = WaterfallCollaborationStrategy()
        waterfall_phases = ["requirements", "high_level_design"]
        waterfall_context = context.copy()
        waterfall_context["phases"] = waterfall_phases
        
        waterfall_result = waterfall_strategy.facilitate_collaboration(
            agents[:len(agents)//2], waterfall_context
        )
        
        # Use Agile for implementation and testing
        agile_strategy = AgileCollaborationStrategy()
        agile_context = context.copy()
        agile_context.update(waterfall_result)
        
        agile_result = agile_strategy.facilitate_collaboration(
            agents[len(agents)//2:], agile_context
        )
        
        # Combine results
        result.update(waterfall_result)
        result.update(agile_result)
        
        return result
