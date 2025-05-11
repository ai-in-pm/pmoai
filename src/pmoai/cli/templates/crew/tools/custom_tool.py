"""Custom tool for the {{crew_name}} crew."""

from typing import Optional

from pmoai.tools.base_tool import BaseTool, tool


class CustomTool(BaseTool):
    """A custom tool for the {{crew_name}} crew."""
    
    name: str = "custom_tool"
    description: str = "A custom tool for the {{crew_name}} crew."
    
    @tool
    def run(self, query: str) -> str:
        """Run the custom tool.
        
        Args:
            query: The query to process.
            
        Returns:
            The result of the tool.
        """
        # Implement your custom tool logic here
        return f"Custom tool processed query: {query}"
