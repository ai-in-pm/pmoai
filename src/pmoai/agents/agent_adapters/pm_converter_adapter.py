import json
import re
from typing import Any, Dict, Optional

from pmoai.agents.agent_adapters.base_converter_adapter import BaseConverterAdapter


class PMConverterAdapter(BaseConverterAdapter):
    """Project Management specific converter adapter for PMOAI.
    
    This adapter extends the base converter adapter with PM-specific functionality.
    """
    
    def __init__(self, agent_adapter: Any):
        """Initialize the PM converter adapter.
        
        Args:
            agent_adapter: The agent adapter to use.
        """
        super().__init__(agent_adapter)
        self._output_format = None
        self._schema = None
        self._output_model = None
    
    def configure_structured_output(self, task: Any) -> None:
        """Configure the structured output for the task.
        
        Args:
            task: The task to configure structured output for.
        """
        if hasattr(task, "output_format") and task.output_format:
            self._output_format = task.output_format
            
            if self._output_format == "json":
                # Configure for JSON output
                self._schema = None
                self._output_model = None
            elif self._output_format == "pydantic":
                # Configure for Pydantic output
                if hasattr(task, "output_model") and task.output_model:
                    self._output_model = task.output_model
                    self._schema = self._generate_model_description(self._output_model)
                else:
                    self._output_model = None
                    self._schema = None
            else:
                # No structured output
                self._schema = None
                self._output_model = None
        else:
            # No structured output
            self._output_format = None
            self._schema = None
            self._output_model = None
    
    def enhance_system_prompt(self, base_prompt: str) -> str:
        """Enhance the system prompt with structured output instructions.
        
        Args:
            base_prompt: The base system prompt.
            
        Returns:
            The enhanced system prompt.
        """
        if not self._output_format:
            return base_prompt
        
        if self._output_format == "json":
            # Add JSON output instructions
            json_instructions = """
Your response should be formatted as a valid JSON object.
Make sure to escape any special characters and format the JSON properly.
"""
            return f"{base_prompt}\n\n{json_instructions}"
        elif self._output_format == "pydantic" and self._schema:
            # Add Pydantic output instructions
            pydantic_instructions = f"""
Your response should conform to the following schema:

{self._schema}

Make sure your response can be parsed as a valid JSON object that matches this schema.
"""
            return f"{base_prompt}\n\n{pydantic_instructions}"
        else:
            return base_prompt
    
    def post_process_result(self, result: str) -> str:
        """Post-process the result to ensure it matches the expected format.
        
        Args:
            result: The raw result from the agent.
            
        Returns:
            The processed result.
        """
        if not self._output_format:
            return result
        
        if self._output_format == "json":
            # Extract JSON from the result
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', result)
            if json_match:
                json_str = json_match.group(1)
                try:
                    # Validate JSON
                    json.loads(json_str)
                    return json_str
                except json.JSONDecodeError:
                    # If JSON is invalid, return the original result
                    return result
            
            # Try to find JSON without code blocks
            try:
                # Check if the entire result is valid JSON
                json.loads(result)
                return result
            except json.JSONDecodeError:
                # If not, return the original result
                return result
        elif self._output_format == "pydantic" and self._output_model:
            # Extract JSON from the result
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', result)
            if json_match:
                json_str = json_match.group(1)
                try:
                    # Validate JSON against the Pydantic model
                    data = json.loads(json_str)
                    # In a real implementation, we would validate against the Pydantic model here
                    return json_str
                except json.JSONDecodeError:
                    # If JSON is invalid, return the original result
                    return result
            
            # Try to find JSON without code blocks
            try:
                # Check if the entire result is valid JSON
                data = json.loads(result)
                # In a real implementation, we would validate against the Pydantic model here
                return result
            except json.JSONDecodeError:
                # If not, return the original result
                return result
        else:
            return result
    
    def _generate_model_description(self, model: Any) -> str:
        """Generate a description of a Pydantic model.
        
        Args:
            model: The Pydantic model to describe.
            
        Returns:
            A description of the model.
        """
        # In a real implementation, this would generate a description of the model
        # For now, we'll just return a placeholder
        return "Model description placeholder"
