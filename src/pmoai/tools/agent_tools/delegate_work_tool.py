from typing import Optional

from pydantic import Field

from pmoai.tools.agent_tools.base_agent_tools import BaseAgentTool


class DelegateWorkTool(BaseAgentTool):
    """
    Tool for delegating work to other agents.
    """

    name: str = Field(default="delegate_work", description="Name of the tool")
    description: str = Field(
        default="Delegate a task to a coworker. Use this when you need help from a specific coworker.",
        description="Description of the tool",
    )

    def _run(
        self,
        coworker: Optional[str] = None,
        task: Optional[str] = None,
        context: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Delegate a task to another agent.

        Args:
            coworker: The name of the agent to delegate to
            task: The task to delegate
            context: Optional context for the task
            **kwargs: Additional arguments

        Returns:
            The result of the delegated task
        """
        coworker = self._get_coworker(coworker, **kwargs)
        task = task or kwargs.get("task")
        context = context or kwargs.get("context")

        if not task:
            return self.i18n.errors("agent_tool_missing_task")

        return self._execute(
            agent_name=coworker,
            task=task,
            context=context,
        )
