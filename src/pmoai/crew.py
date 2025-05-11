from typing import Any, Dict, List, Optional, Union

from crewai import Crew as CrewAICrew
from pydantic import Field

from pmoai.agent import Agent
from pmoai.knowledge.source.base_knowledge_source import BaseKnowledgeSource
from pmoai.llm import BaseLLM
from pmoai.process import Process
from pmoai.task import Task


class Crew(CrewAICrew):
    """A Project Management focused crew in PMOAI.

    Attributes:
        agents: List of agents part of this crew.
        tasks: List of tasks assigned to the crew.
        process: The process flow that the crew will follow.
        verbose: Indicates the verbosity level for logging during execution.
        project_name: The name of the project the crew is working on.
        project_code: A unique code identifier for the project.
        project_methodology: The project management methodology being used.
        project_phase: The current phase of the project.
        organization: The organization the project belongs to.
        portfolio: The portfolio the project belongs to.
    """

    project_name: Optional[str] = Field(
        default=None,
        description="The name of the project the crew is working on.",
    )
    
    project_code: Optional[str] = Field(
        default=None,
        description="A unique code identifier for the project.",
    )
    
    project_methodology: Optional[str] = Field(
        default=None,
        description="The project management methodology being used (e.g., Agile, Waterfall, PRINCE2).",
    )
    
    project_phase: Optional[str] = Field(
        default=None,
        description="The current phase of the project (e.g., Initiation, Planning, Execution, Monitoring, Closing).",
    )
    
    organization: Optional[str] = Field(
        default=None,
        description="The organization the project belongs to.",
    )
    
    portfolio: Optional[str] = Field(
        default=None,
        description="The portfolio the project belongs to.",
    )

    def __init__(
        self,
        agents: List[Agent],
        tasks: List[Task],
        process: Union[Process, str] = Process.sequential,
        verbose: bool = False,
        project_name: Optional[str] = None,
        project_code: Optional[str] = None,
        project_methodology: Optional[str] = None,
        project_phase: Optional[str] = None,
        organization: Optional[str] = None,
        portfolio: Optional[str] = None,
        manager_llm: Optional[Union[BaseLLM, str]] = None,
        manager_agent: Optional[Agent] = None,
        memory: bool = False,
        memory_config: Optional[Dict[str, Any]] = None,
        cache: bool = False,
        function_calling_llm: Optional[Union[BaseLLM, str]] = None,
        config: Optional[Dict[str, Any]] = None,
        max_rpm: Optional[int] = None,
        prompt_file: Optional[str] = None,
        task_callback: Optional[Any] = None,
        step_callback: Optional[Any] = None,
        share_crew: bool = False,
        planning: bool = False,
        chat_llm: Optional[Union[BaseLLM, str]] = None,
        knowledge_sources: Optional[List[BaseKnowledgeSource]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a new Crew instance.

        Args:
            agents: List of agents part of this crew.
            tasks: List of tasks assigned to the crew.
            process: The process flow that the crew will follow.
            verbose: Indicates the verbosity level for logging during execution.
            project_name: The name of the project the crew is working on.
            project_code: A unique code identifier for the project.
            project_methodology: The project management methodology being used.
            project_phase: The current phase of the project.
            organization: The organization the project belongs to.
            portfolio: The portfolio the project belongs to.
            manager_llm: The language model that will run manager agent.
            manager_agent: Custom agent that will be used as manager.
            memory: Whether the crew should use memory to store memories of it's execution.
            memory_config: Configuration for the memory to be used for the crew.
            cache: Whether the crew should use a cache to store the results of the tools execution.
            function_calling_llm: The language model that will run the tool calling for all the agents.
            config: Configuration settings for the crew.
            max_rpm: Maximum number of requests per minute for the crew execution to be respected.
            prompt_file: Path to the prompt json file to be used for the crew.
            task_callback: Callback to be executed after each task for every agents execution.
            step_callback: Callback to be executed after each step for every agents execution.
            share_crew: Whether you want to share the complete crew information and execution with crewAI.
            planning: Plan the crew execution and add the plan to the crew.
            chat_llm: The language model used for orchestrating chat interactions with the crew.
            knowledge_sources: Knowledge sources to be used by the crew.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            agents=agents,
            tasks=tasks,
            process=process,
            verbose=verbose,
            manager_llm=manager_llm,
            manager_agent=manager_agent,
            memory=memory,
            memory_config=memory_config,
            cache=cache,
            function_calling_llm=function_calling_llm,
            config=config,
            max_rpm=max_rpm,
            prompt_file=prompt_file,
            task_callback=task_callback,
            step_callback=step_callback,
            share_crew=share_crew,
            planning=planning,
            chat_llm=chat_llm,
            knowledge_sources=knowledge_sources,
            **kwargs,
        )
        
        self.project_name = project_name
        self.project_code = project_code
        self.project_methodology = project_methodology
        self.project_phase = project_phase
        self.organization = organization
        self.portfolio = portfolio
