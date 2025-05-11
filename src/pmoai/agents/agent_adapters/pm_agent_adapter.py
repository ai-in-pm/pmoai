from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from pmoai.agents.agent_adapters.base_agent_adapter import BaseAgentAdapter
from pmoai.tools.base_tool import BaseTool


class PMAgentAdapter(BaseAgentAdapter):
    """Project Management specific agent adapter for PMOAI.
    
    This adapter extends the base agent adapter with PM-specific functionality.
    """
    
    pm_methodology: str = Field(
        default="Agile",
        description="The project management methodology used by the agent.",
    )
    certifications: List[str] = Field(
        default_factory=list,
        description="The project management certifications held by the agent.",
    )
    industry_expertise: List[str] = Field(
        default_factory=list,
        description="The industries the agent has expertise in.",
    )
    
    def __init__(
        self,
        pm_methodology: str = "Agile",
        certifications: Optional[List[str]] = None,
        industry_expertise: Optional[List[str]] = None,
        agent_config: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        """Initialize the PM agent adapter.
        
        Args:
            pm_methodology: The project management methodology used by the agent.
            certifications: The project management certifications held by the agent.
            industry_expertise: The industries the agent has expertise in.
            agent_config: Additional configuration for the agent.
            **kwargs: Additional arguments to pass to the parent constructor.
        """
        super().__init__(agent_config=agent_config, **kwargs)
        self.pm_methodology = pm_methodology
        self.certifications = certifications or []
        self.industry_expertise = industry_expertise or []
    
    def configure_tools(self, tools: Optional[List[BaseTool]] = None) -> None:
        """Configure and adapt tools for the PM agent.
        
        Args:
            tools: Optional list of BaseTool instances to be configured.
        """
        # This is a placeholder implementation
        # In a real implementation, this would configure tools specifically for PM agents
        self.tools = tools or []
    
    def enhance_system_prompt(self, base_prompt: str) -> str:
        """Enhance the system prompt with PM-specific instructions.
        
        Args:
            base_prompt: The base system prompt.
            
        Returns:
            The enhanced system prompt.
        """
        # Add PM-specific instructions to the system prompt
        pm_instructions = f"""
You are a project management expert with the following characteristics:
- Methodology: {self.pm_methodology}
- Certifications: {', '.join(self.certifications)}
- Industry Expertise: {', '.join(self.industry_expertise)}

As a project management professional, you should:
1. Follow best practices for {self.pm_methodology} methodology
2. Use appropriate project management terminology
3. Consider project constraints (scope, time, cost, quality)
4. Identify and manage risks proactively
5. Communicate clearly with stakeholders
6. Document decisions and actions
7. Ensure alignment with project objectives
"""
        
        # Combine the base prompt with the PM-specific instructions
        enhanced_prompt = f"{base_prompt}\n\n{pm_instructions}"
        
        return enhanced_prompt
