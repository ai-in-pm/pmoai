from typing import Any, Dict, List, Optional, Type, Union

from crewai import Task as CrewAITask
from pydantic import BaseModel, Field

from pmoai.agents.agent_builder.base_agent import BaseAgent
from pmoai.tools.base_tool import BaseTool


class Task(CrewAITask):
    """A Project Management focused task in a PMOAI crew.

    Attributes:
        description: Description of the actual task.
        expected_output: Clear definition of expected output for the task.
        agent: Agent responsible for execution the task.
        context: Other tasks that will have their output used as context for this task.
        tools: Tools the agent is limited to use for this task.
        pm_phase: The project management phase this task belongs to.
        priority: The priority level of the task.
        dependencies: List of tasks that must be completed before this task.
        estimated_duration: Estimated duration to complete the task in hours.
        deliverables: List of deliverables expected from this task.
        stakeholders: List of stakeholders involved in or affected by this task.
    """

    pm_phase: Optional[str] = Field(
        default=None,
        description="The project management phase this task belongs to (e.g., Initiation, Planning, Execution, Monitoring, Closing).",
    )
    
    priority: Optional[str] = Field(
        default=None,
        description="The priority level of the task (e.g., High, Medium, Low).",
    )
    
    dependencies: Optional[List[str]] = Field(
        default=None,
        description="List of tasks that must be completed before this task.",
    )
    
    estimated_duration: Optional[float] = Field(
        default=None,
        description="Estimated duration to complete the task in hours.",
    )
    
    deliverables: Optional[List[str]] = Field(
        default=None,
        description="List of deliverables expected from this task.",
    )
    
    stakeholders: Optional[List[str]] = Field(
        default=None,
        description="List of stakeholders involved in or affected by this task.",
    )

    def __init__(
        self,
        description: str,
        expected_output: str,
        agent: Optional[BaseAgent] = None,
        context: Optional[List["Task"]] = None,
        tools: Optional[List[BaseTool]] = None,
        pm_phase: Optional[str] = None,
        priority: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        estimated_duration: Optional[float] = None,
        deliverables: Optional[List[str]] = None,
        stakeholders: Optional[List[str]] = None,
        async_execution: bool = False,
        output_json: Optional[Type[BaseModel]] = None,
        output_pydantic: Optional[Type[BaseModel]] = None,
        output_file: Optional[str] = None,
        callback: Optional[Any] = None,
        human_input: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize a new Task instance.

        Args:
            description: Description of the actual task.
            expected_output: Clear definition of expected output for the task.
            agent: Agent responsible for execution the task.
            context: Other tasks that will have their output used as context for this task.
            tools: Tools the agent is limited to use for this task.
            pm_phase: The project management phase this task belongs to.
            priority: The priority level of the task.
            dependencies: List of tasks that must be completed before this task.
            estimated_duration: Estimated duration to complete the task in hours.
            deliverables: List of deliverables expected from this task.
            stakeholders: List of stakeholders involved in or affected by this task.
            async_execution: Whether the task should be executed asynchronously.
            output_json: A Pydantic model to be used to create a JSON output.
            output_pydantic: A Pydantic model to be used to create a Pydantic output.
            output_file: A file path to be used to create a file output.
            callback: Callback to be executed after the task is completed.
            human_input: Whether the task should have a human review the final answer.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            description=description,
            expected_output=expected_output,
            agent=agent,
            context=context,
            tools=tools,
            async_execution=async_execution,
            output_json=output_json,
            output_pydantic=output_pydantic,
            output_file=output_file,
            callback=callback,
            human_input=human_input,
            **kwargs,
        )
        
        self.pm_phase = pm_phase
        self.priority = priority
        self.dependencies = dependencies
        self.estimated_duration = estimated_duration
        self.deliverables = deliverables
        self.stakeholders = stakeholders
