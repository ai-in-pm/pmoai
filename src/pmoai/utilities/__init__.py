"""Utilities module for PMOAI."""

from pmoai.utilities.embedding_configurator import EmbeddingConfigurator
from pmoai.utilities.logger import Logger
from pmoai.utilities.paths import (
    cache_storage_path,
    db_storage_path,
    get_pmoai_home,
    logs_path,
)
from pmoai.utilities.printer import Printer


class I18N:
    """
    Internationalization utilities for PMOAI.

    This is a placeholder implementation that will be expanded in the future.
    """

    def __init__(self, language: str = "en"):
        """
        Initialize the I18N utility.

        Args:
            language: Language code
        """
        self.language = language
        self._translations = {
            "en": {
                "errors": {
                    "agent_tool_unexisting_coworker": "Could not find coworker. Available coworkers: {coworkers}. Error: {error}",
                    "agent_tool_execution_error": "Error executing task with agent {agent_role}: {error}",
                    "agent_tool_missing_question": "Missing question for ask_question tool",
                    "agent_tool_missing_task": "Missing task for delegate_work tool",
                    "image_tool_file_not_found": "Image file not found: {path}",
                    "image_tool_read_error": "Error reading image file: {error}",
                    "image_tool_missing_image": "No image provided. Please provide an image path, URL, or base64 data.",
                    "tool_arguments_error": "Invalid tool arguments. Please provide valid arguments.",
                    "tool_usage_error": "Error using tool: {error}",
                    "tool_usage_exception": "Error using tool {tool}: {error}. Tool inputs: {tool_inputs}",
                },
                "tools": {
                    "delegate_work": "Delegate a task to a coworker. Available coworkers: {coworkers}",
                    "ask_question": "Ask a question to a coworker. Available coworkers: {coworkers}",
                    "add_image": {
                        "name": "Add Image",
                        "description": "Add an image to the conversation",
                        "default_action": "Here's an image:",
                    },
                },
                "slice": {
                    "format": "Remember to use the correct format for tools: {tool_names}",
                    "tools": "Available tools: {tools}\nTool names: {tool_names}",
                },
                "manager_request": "Response to a request from another agent",
            }
        }

    def errors(self, key: str) -> str:
        """Get an error message."""
        return self._translations.get(self.language, {}).get("errors", {}).get(key, key)

    def tools(self, key: str) -> str:
        """Get a tool message."""
        return self._translations.get(self.language, {}).get("tools", {}).get(key, key)

    def slice(self, key: str) -> str:
        """Get a slice message."""
        return self._translations.get(self.language, {}).get("slice", {}).get(key, key)


__all__ = [
    "EmbeddingConfigurator",
    "I18N",
    "Logger",
    "Printer",
    "cache_storage_path",
    "db_storage_path",
    "get_pmoai_home",
    "logs_path",
]
