# Getting Started with PMOAI

PMOAI (Project Management Office AI Agents) is a framework for orchestrating AI agents focused on project management tasks. This guide will help you get started with PMOAI.

## Installation

You can install PMOAI using pip:

```bash
pip install pmoai
```

Alternatively, you can install from source:

```bash
git clone https://github.com/pmoai/pmoai.git
cd pmoai
python install.py
```

## Configuration

PMOAI requires an API key for the language model provider. You can set this as an environment variable:

```bash
# For OpenAI models (default)
export OPENAI_API_KEY=your-api-key  # Linux/Mac
set OPENAI_API_KEY=your-api-key     # Windows

# For Anthropic models (optional)
export ANTHROPIC_API_KEY=your-api-key  # Linux/Mac
set ANTHROPIC_API_KEY=your-api-key     # Windows
```

Alternatively, you can create a `.env` file in your project directory with these variables.

## Basic Usage

Here's a simple example of using PMOAI:

```python
from pmoai import Agent, Task, Crew
from pmoai.tools.pm_specific import ProjectCharterTool

# Create a project manager agent
project_manager = Agent(
    role="Project Manager",
    goal="Successfully plan and execute the project",
    backstory="You are an experienced project manager with PMP certification.",
    pm_methodology="Agile",
    certifications=["PMP", "CSM"],
    industry_expertise=["Software Development"]
)

# Create a project charter task
charter_task = Task(
    description="Create a project charter for a new software development project",
    expected_output="A comprehensive project charter document",
    agent=project_manager,
    tools=[ProjectCharterTool()],
    pm_phase="Initiation",
    priority="High"
)

# Create a project crew
project_crew = Crew(
    agents=[project_manager],
    tasks=[charter_task],
    project_name="My Software Project",
    project_methodology="Agile"
)

# Execute the crew
result = project_crew.kickoff()
print(result.raw)
```

## PM-Specific Tools

PMOAI includes several PM-specific tools:

- **ProjectCharterTool**: Creates project charter documents
- **RiskRegisterTool**: Creates risk register documents
- **ResourceAllocationTool**: Creates resource allocation plans
- **GanttChartTool**: Creates Gantt chart visualizations
- **StakeholderCommunicationTool**: Creates stakeholder communication plans

Example usage:

```python
from pmoai.tools.pm_specific import RiskRegisterTool

risk_analyst = Agent(
    role="Risk Analyst",
    goal="Identify and analyze project risks",
    backstory="You specialize in risk management for complex projects."
)

risk_task = Task(
    description="Identify potential risks for the software development project",
    expected_output="A risk register with at least 5 key risks and mitigation strategies",
    agent=risk_analyst,
    tools=[RiskRegisterTool()]
)
```

## PM-Specific Processes

PMOAI extends CrewAI's processes with PM-specific processes:

```python
from pmoai import Process

# Available processes
Process.sequential   # Tasks are executed in sequence
Process.hierarchical # A manager agent delegates tasks
Process.agile        # Tasks are executed in sprints
Process.waterfall    # Tasks are executed in distinct phases
Process.kanban       # Tasks are pulled through workflow stages
Process.hybrid       # A combination of agile and waterfall
```

## Next Steps

- Check out the [examples](../examples) directory for more usage examples
- Read the [API documentation](./api_reference.md) for detailed information
- Explore [advanced features](./advanced_features.md) for more capabilities
