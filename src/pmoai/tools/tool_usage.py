import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple, Union

from pmoai.tools.base_tool import BaseTool
from pmoai.tools.tool_calling import ToolCalling
from pmoai.tools.tool_types import ToolResult

logger = logging.getLogger(__name__)


class ToolUsage:
    """
    A class for handling tool usage and parsing tool calls from LLM responses.
    """

    @staticmethod
    def parse_tool_calls(
        response: str,
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Parse tool calls from an LLM response.

        Args:
            response: The LLM response text

        Returns:
            Tuple containing:
                - The response with tool calls removed
                - List of parsed tool calls
        """
        # Extract tool calls using regex
        tool_pattern = r"```json\s*(\{.*?\})\s*```"
        matches = re.finditer(tool_pattern, response, re.DOTALL)
        
        tool_calls = []
        clean_response = response
        
        for match in matches:
            try:
                json_str = match.group(1)
                tool_data = json.loads(json_str)
                
                # Check if this is a valid tool call
                if "tool_name" in tool_data and "arguments" in tool_data:
                    tool_calls.append(tool_data)
                    # Remove the tool call from the response
                    clean_response = clean_response.replace(match.group(0), "")
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse tool call: {match.group(1)}")
        
        # Clean up any remaining artifacts
        clean_response = re.sub(r"\n{3,}", "\n\n", clean_response)
        clean_response = clean_response.strip()
        
        return clean_response, tool_calls

    @staticmethod
    def execute_tool_calls(
        tool_calls: List[Dict[str, Any]],
        tools: List[BaseTool],
    ) -> List[ToolResult]:
        """
        Execute a list of tool calls.

        Args:
            tool_calls: List of tool call dictionaries
            tools: List of available tools

        Returns:
            List of tool results
        """
        results = []
        
        for call in tool_calls:
            tool_name = call.get("tool_name")
            arguments = call.get("arguments", {})
            
            # Find the matching tool
            matching_tools = [t for t in tools if t.name == tool_name]
            
            if not matching_tools:
                logger.warning(f"Tool not found: {tool_name}")
                results.append(
                    ToolResult(
                        result=f"Error: Tool '{tool_name}' not found. Available tools: {', '.join(t.name for t in tools)}",
                        result_as_answer=False,
                    )
                )
                continue
            
            tool = matching_tools[0]
            
            try:
                # Execute the tool
                result = tool.run(**arguments)
                results.append(
                    ToolResult(
                        result=str(result),
                        result_as_answer=tool.result_as_answer,
                    )
                )
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {e}")
                results.append(
                    ToolResult(
                        result=f"Error executing tool '{tool_name}': {str(e)}",
                        result_as_answer=False,
                    )
                )
        
        return results

    @staticmethod
    def format_tool_results(
        results: List[ToolResult],
        include_tool_names: bool = True,
    ) -> str:
        """
        Format tool results into a string.

        Args:
            results: List of tool results
            include_tool_names: Whether to include tool names in the output

        Returns:
            Formatted string of tool results
        """
        if not results:
            return ""
            
        formatted_results = []
        
        for i, result in enumerate(results):
            if include_tool_names:
                formatted_results.append(f"Tool Result {i+1}:\n{result.result}")
            else:
                formatted_results.append(result.result)
        
        return "\n\n".join(formatted_results)
