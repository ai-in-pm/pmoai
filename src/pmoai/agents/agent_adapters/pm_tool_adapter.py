from typing import Any, List, Optional

from pmoai.agents.agent_adapters.base_tool_adapter import BaseToolAdapter
from pmoai.tools.base_tool import BaseTool


class PMToolAdapter(BaseToolAdapter):
    """Project Management specific tool adapter for PMOAI.
    
    This adapter extends the base tool adapter with PM-specific functionality.
    """
    
    def __init__(self, tools: Optional[List[BaseTool]] = None):
        """Initialize the PM tool adapter.
        
        Args:
            tools: Optional list of BaseTool instances to be configured.
        """
        super().__init__(tools=tools)
    
    def configure_tools(self, tools: List[BaseTool]) -> None:
        """Configure and convert tools for PM-specific use.
        
        Args:
            tools: List of BaseTool instances to be configured and converted.
        """
        if self.original_tools:
            all_tools = tools + self.original_tools
        else:
            all_tools = tools
        
        if all_tools:
            self.converted_tools = self._enhance_tools_for_pm(all_tools)
    
    def _enhance_tools_for_pm(self, tools: List[BaseTool]) -> List[BaseTool]:
        """Enhance tools for PM-specific use.
        
        Args:
            tools: List of BaseTool instances to be enhanced.
            
        Returns:
            List of enhanced tools.
        """
        enhanced_tools = []
        
        for tool in tools:
            # Create a copy of the tool
            enhanced_tool = tool
            
            # Enhance the tool description with PM-specific context
            if hasattr(enhanced_tool, "description"):
                enhanced_tool.description = self._add_pm_context_to_description(
                    enhanced_tool.description
                )
            
            enhanced_tools.append(enhanced_tool)
        
        return enhanced_tools
    
    def _add_pm_context_to_description(self, description: str) -> str:
        """Add PM-specific context to a tool description.
        
        Args:
            description: The original tool description.
            
        Returns:
            The enhanced tool description.
        """
        # Add PM-specific context to the tool description
        pm_context = """
This tool should be used in accordance with project management best practices.
Consider the impact on project scope, schedule, cost, and quality when using this tool.
Document the use of this tool and its outcomes for project records.
"""
        
        # Combine the original description with the PM-specific context
        enhanced_description = f"{description}\n\n{pm_context}"
        
        return enhanced_description
