from typing import Any, Dict, List, Optional, Union

from crewai import Agent as CrewAIAgent
from pydantic import Field

from pmoai.knowledge.knowledge import Knowledge
from pmoai.llm import BaseLLM
from pmoai.tools.base_tool import BaseTool


class Agent(CrewAIAgent):
    """A Project Management focused agent in a PMOAI crew.

    Attributes:
        role: The role of the agent in the project (e.g., Project Manager, Risk Analyst).
        goal: The objective of the agent.
        backstory: The backstory of the agent, including experience and qualifications.
        pm_methodology: The project management methodology the agent specializes in.
        certifications: List of professional certifications the agent possesses.
        industry_expertise: List of industries the agent has expertise in.
        tools: Tools at the agent's disposal.
        knowledge: The knowledge base of the agent.
        llm: The language model that will run the agent.
        verbose: Whether the agent execution should be in verbose mode.
        allow_delegation: Whether the agent is allowed to delegate tasks to other agents.
        max_rpm: Maximum number of requests per minute for the agent execution.
        max_iter: Maximum number of iterations for an agent to execute a task.
        max_execution_time: Maximum execution time for the agent in seconds.
    """

    pm_methodology: Optional[str] = Field(
        default=None,
        description="The project management methodology the agent specializes in (e.g., Agile, Waterfall, PRINCE2).",
    )
    
    certifications: Optional[List[str]] = Field(
        default=None,
        description="List of professional certifications the agent possesses (e.g., PMP, PRINCE2, CSM).",
    )
    
    industry_expertise: Optional[List[str]] = Field(
        default=None,
        description="List of industries the agent has expertise in (e.g., IT, Construction, Healthcare).",
    )

    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        pm_methodology: Optional[str] = None,
        certifications: Optional[List[str]] = None,
        industry_expertise: Optional[List[str]] = None,
        tools: Optional[List[Any]] = None,
        knowledge: Optional[Union[Knowledge, List[Knowledge]]] = None,
        llm: Optional[BaseLLM] = None,
        verbose: bool = False,
        allow_delegation: bool = True,
        max_rpm: Optional[int] = None,
        max_iter: int = 25,
        max_execution_time: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a new Agent instance.

        Args:
            role: The role of the agent in the project.
            goal: The objective of the agent.
            backstory: The backstory of the agent.
            pm_methodology: The project management methodology the agent specializes in.
            certifications: List of professional certifications the agent possesses.
            industry_expertise: List of industries the agent has expertise in.
            tools: Tools at the agent's disposal.
            knowledge: The knowledge base of the agent.
            llm: The language model that will run the agent.
            verbose: Whether the agent execution should be in verbose mode.
            allow_delegation: Whether the agent is allowed to delegate tasks to other agents.
            max_rpm: Maximum number of requests per minute for the agent execution.
            max_iter: Maximum number of iterations for an agent to execute a task.
            max_execution_time: Maximum execution time for the agent in seconds.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            knowledge=knowledge,
            llm=llm,
            verbose=verbose,
            allow_delegation=allow_delegation,
            max_rpm=max_rpm,
            max_iter=max_iter,
            max_execution_time=max_execution_time,
            **kwargs,
        )
        
        self.pm_methodology = pm_methodology
        self.certifications = certifications
        self.industry_expertise = industry_expertise
