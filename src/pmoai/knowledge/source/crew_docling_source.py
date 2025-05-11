from typing import Any, Dict, List, Optional

from pydantic import Field

from pmoai.knowledge.source.base_knowledge_source import BaseKnowledgeSource


class CrewDoclingSource(BaseKnowledgeSource):
    """
    A knowledge source that reads from a crew docling.
    
    A crew docling is a document that contains information about a crew,
    including its purpose, agents, tasks, and other relevant information.
    """

    crew_name: str = Field(..., description="The name of the crew")
    crew_description: str = Field(..., description="The description of the crew")
    agents: List[Dict[str, Any]] = Field(
        default_factory=list, description="The agents in the crew"
    )
    tasks: List[Dict[str, Any]] = Field(
        default_factory=list, description="The tasks in the crew"
    )
    project_info: Dict[str, Any] = Field(
        default_factory=dict, description="Information about the project"
    )

    def __init__(
        self,
        crew_name: str,
        crew_description: str,
        agents: Optional[List[Dict[str, Any]]] = None,
        tasks: Optional[List[Dict[str, Any]]] = None,
        project_info: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize a crew docling knowledge source.

        Args:
            crew_name: The name of the crew.
            crew_description: The description of the crew.
            agents: Optional list of agents in the crew.
            tasks: Optional list of tasks in the crew.
            project_info: Optional information about the project.
            metadata: Optional metadata for this knowledge source.
            **kwargs: Additional keyword arguments.
        """
        if metadata is None:
            metadata = {}

        # Add crew metadata
        metadata.update(
            {
                "source": "crew_docling",
                "crew_name": crew_name,
            }
        )

        super().__init__(
            crew_name=crew_name,
            crew_description=crew_description,
            agents=agents or [],
            tasks=tasks or [],
            project_info=project_info or {},
            metadata=metadata,
            **kwargs,
        )

    def add(self) -> None:
        """
        Add this knowledge source to the knowledge base.
        """
        if self.storage is None:
            raise ValueError("Storage is not initialized.")

        chunks = self.get_chunks()
        self.storage.add_texts(chunks, self.metadata)

    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        content = f"# Crew: {self.crew_name}\n\n"
        content += f"## Description\n{self.crew_description}\n\n"

        # Add project information
        if self.project_info:
            content += "## Project Information\n"
            for key, value in self.project_info.items():
                content += f"- {key}: {value}\n"
            content += "\n"

        # Add agents
        if self.agents:
            content += "## Agents\n"
            for i, agent in enumerate(self.agents, 1):
                content += f"### Agent {i}: {agent.get('name', 'Unnamed Agent')}\n"
                content += f"- Role: {agent.get('role', 'N/A')}\n"
                content += f"- Goal: {agent.get('goal', 'N/A')}\n"
                if "backstory" in agent:
                    content += f"- Backstory: {agent['backstory']}\n"
                content += "\n"

        # Add tasks
        if self.tasks:
            content += "## Tasks\n"
            for i, task in enumerate(self.tasks, 1):
                content += f"### Task {i}: {task.get('name', 'Unnamed Task')}\n"
                content += f"- Description: {task.get('description', 'N/A')}\n"
                content += f"- Expected Output: {task.get('expected_output', 'N/A')}\n"
                if "agent" in task:
                    content += f"- Assigned to: {task['agent']}\n"
                if "dependencies" in task:
                    content += f"- Dependencies: {', '.join(task['dependencies'])}\n"
                content += "\n"

        return content
