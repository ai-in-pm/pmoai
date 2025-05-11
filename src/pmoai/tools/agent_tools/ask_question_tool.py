from typing import Optional

from pydantic import Field

from pmoai.tools.agent_tools.base_agent_tools import BaseAgentTool


class AskQuestionTool(BaseAgentTool):
    """
    Tool for asking questions to other agents.
    """

    name: str = Field(default="ask_question", description="Name of the tool")
    description: str = Field(
        default="Ask a question to a coworker. Use this when you need information from a specific coworker.",
        description="Description of the tool",
    )

    def _run(
        self,
        coworker: Optional[str] = None,
        question: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Ask a question to another agent.

        Args:
            coworker: The name of the agent to ask
            question: The question to ask
            **kwargs: Additional arguments

        Returns:
            The response from the agent
        """
        coworker = self._get_coworker(coworker, **kwargs)
        question = question or kwargs.get("question")

        if not question:
            return self.i18n.errors("agent_tool_missing_question")

        return self._execute(
            agent_name=coworker,
            task=question,
        )
