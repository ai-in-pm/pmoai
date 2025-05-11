# PMOAI API Reference

This document provides a reference for the main classes and functions in PMOAI.

## Agent

The `Agent` class represents a project management focused agent in a PMOAI crew.

```python
from pmoai import Agent

agent = Agent(
    role="Project Manager",
    goal="Successfully plan and execute the project",
    backstory="You are an experienced project manager with PMP certification.",
    pm_methodology="Agile",
    certifications=["PMP", "CSM"],
    industry_expertise=["Software Development", "IT"],
    tools=[tool1, tool2],
    knowledge=knowledge_source,
    llm=llm,
    verbose=True,
    allow_delegation=True,
    max_rpm=10,
    max_iter=25,
    max_execution_time=300
)
```

### Parameters

- `role` (str): The role of the agent in the project (e.g., Project Manager, Risk Analyst).
- `goal` (str): The objective of the agent.
- `backstory` (str): The backstory of the agent, including experience and qualifications.
- `pm_methodology` (str, optional): The project management methodology the agent specializes in (e.g., Agile, Waterfall, PRINCE2).
- `certifications` (List[str], optional): List of professional certifications the agent possesses (e.g., PMP, PRINCE2, CSM).
- `industry_expertise` (List[str], optional): List of industries the agent has expertise in (e.g., IT, Construction, Healthcare).
- `tools` (List[BaseTool], optional): Tools at the agent's disposal.
- `knowledge` (Knowledge or List[Knowledge], optional): The knowledge base of the agent.
- `llm` (BaseLLM, optional): The language model that will run the agent.
- `verbose` (bool, optional): Whether the agent execution should be in verbose mode.
- `allow_delegation` (bool, optional): Whether the agent is allowed to delegate tasks to other agents.
- `max_rpm` (int, optional): Maximum number of requests per minute for the agent execution.
- `max_iter` (int, optional): Maximum number of iterations for an agent to execute a task.
- `max_execution_time` (int, optional): Maximum execution time for the agent in seconds.

## Task

The `Task` class represents a project management focused task in a PMOAI crew.

```python
from pmoai import Task

task = Task(
    description="Create a project charter for a new software development project",
    expected_output="A comprehensive project charter document",
    agent=project_manager,
    context=[previous_task],
    tools=[ProjectCharterTool()],
    pm_phase="Initiation",
    priority="High",
    dependencies=["Requirements Gathering"],
    estimated_duration=4.0,
    deliverables=["Project Charter Document"],
    stakeholders=["Executive Team", "Project Team"],
    async_execution=False,
    output_file="project_charter.md",
    human_input=False
)
```

### Parameters

- `description` (str): Description of the actual task.
- `expected_output` (str): Clear definition of expected output for the task.
- `agent` (BaseAgent, optional): Agent responsible for execution the task.
- `context` (List[Task], optional): Other tasks that will have their output used as context for this task.
- `tools` (List[BaseTool], optional): Tools the agent is limited to use for this task.
- `pm_phase` (str, optional): The project management phase this task belongs to (e.g., Initiation, Planning, Execution, Monitoring, Closing).
- `priority` (str, optional): The priority level of the task (e.g., High, Medium, Low).
- `dependencies` (List[str], optional): List of tasks that must be completed before this task.
- `estimated_duration` (float, optional): Estimated duration to complete the task in hours.
- `deliverables` (List[str], optional): List of deliverables expected from this task.
- `stakeholders` (List[str], optional): List of stakeholders involved in or affected by this task.
- `async_execution` (bool, optional): Whether the task should be executed asynchronously.
- `output_file` (str, optional): A file path to be used to create a file output.
- `human_input` (bool, optional): Whether the task should have a human review the final answer.

## Crew

The `Crew` class represents a project management focused crew in PMOAI.

```python
from pmoai import Crew, Process

crew = Crew(
    agents=[project_manager, risk_analyst],
    tasks=[charter_task, risk_task],
    process=Process.sequential,
    verbose=True,
    project_name="Mobile Banking App",
    project_code="MBA-2023",
    project_methodology="Agile",
    project_phase="Initiation",
    organization="ACME Bank",
    portfolio="Digital Transformation",
    manager_llm="gpt-4",
    memory=True,
    planning=True
)

result = crew.kickoff()
```

### Parameters

- `agents` (List[Agent]): List of agents part of this crew.
- `tasks` (List[Task]): List of tasks assigned to the crew.
- `process` (Process or str, optional): The process flow that the crew will follow.
- `verbose` (bool, optional): Indicates the verbosity level for logging during execution.
- `project_name` (str, optional): The name of the project the crew is working on.
- `project_code` (str, optional): A unique code identifier for the project.
- `project_methodology` (str, optional): The project management methodology being used.
- `project_phase` (str, optional): The current phase of the project.
- `organization` (str, optional): The organization the project belongs to.
- `portfolio` (str, optional): The portfolio the project belongs to.
- `manager_llm` (BaseLLM or str, optional): The language model that will run manager agent.
- `manager_agent` (Agent, optional): Custom agent that will be used as manager.
- `memory` (bool, optional): Whether the crew should use memory to store memories of it's execution.
- `planning` (bool, optional): Plan the crew execution and add the plan to the crew.

### Methods

- `kickoff(inputs=None)`: Executes the crew's workflow and returns the result.
- `kickoff_async(inputs=None)`: Asynchronously executes the crew's workflow.
- `kickoff_for_each(inputs_list)`: Executes the crew's workflow for each input in the list.

## Process

The `Process` enum represents different process flows in PMOAI.

```python
from pmoai import Process

# Available processes
process = Process.sequential   # Tasks are executed in sequence
process = Process.hierarchical # A manager agent delegates tasks
process = Process.agile        # Tasks are executed in sprints
process = Process.waterfall    # Tasks are executed in distinct phases
process = Process.kanban       # Tasks are pulled through workflow stages
process = Process.hybrid       # A combination of agile and waterfall
```

## PM-Specific Tools

PMOAI includes several PM-specific tools:

```python
from pmoai.tools.pm_specific import (
    ProjectCharterTool,
    RiskRegisterTool,
    ResourceAllocationTool,
    GanttChartTool,
    StakeholderCommunicationTool
)

# Create tools
charter_tool = ProjectCharterTool()
risk_tool = RiskRegisterTool()
resource_tool = ResourceAllocationTool()
gantt_tool = GanttChartTool()
stakeholder_tool = StakeholderCommunicationTool()
```
