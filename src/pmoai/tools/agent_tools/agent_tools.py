from typing import List, Optional

from pydantic import Field

from pmoai.agent import Agent
from pmoai.tools.agent_tools.add_image_tool import AddImageTool
from pmoai.tools.agent_tools.ask_question_tool import AskQuestionTool
from pmoai.tools.agent_tools.delegate_work_tool import DelegateWorkTool
from pmoai.tools.base_tool import BaseTool
from pmoai.utilities import I18N


class AgentTools:
    """
    A collection of tools for agent-to-agent interactions.
    """

    def __init__(
        self,
        agents: List[Agent],
        i18n: Optional[I18N] = None,
    ):
        """
        Initialize the agent tools.

        Args:
            agents: List of agents that can be delegated to
            i18n: Optional internationalization settings
        """
        self.agents = agents
        self.i18n = i18n or I18N()

    def get_tools(self) -> List[BaseTool]:
        """
        Get all available agent tools.

        Returns:
            List of agent tools
        """
        return [
            DelegateWorkTool(
                agents=self.agents,
                i18n=self.i18n,
            ),
            AskQuestionTool(
                agents=self.agents,
                i18n=self.i18n,
            ),
            AddImageTool(
                agents=self.agents,
                i18n=self.i18n,
            ),
        ]
