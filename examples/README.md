# PMOAI Examples

This directory contains example scripts demonstrating how to use PMOAI for various project management tasks.

## Prerequisites

Before running the examples, make sure you have:

1. Installed PMOAI (run `python install.py` from the root directory)
2. Set your OpenAI API key as an environment variable:
   ```
   # Linux/Mac
   export OPENAI_API_KEY=your-api-key
   
   # Windows
   set OPENAI_API_KEY=your-api-key
   ```
   
   Alternatively, create a `.env` file in the examples directory with your API key:
   ```
   OPENAI_API_KEY=your-api-key
   ```

## Available Examples

### Verify Installation

A simple script to verify that PMOAI is installed correctly:

```bash
python verify_installation.py
```

### Project Initiation Example

Demonstrates how to use PMOAI for project initiation tasks, including creating a project charter, risk register, and stakeholder communication plan:

```bash
python project_initiation_example.py
```

## Creating Your Own Examples

To create your own PMOAI examples:

1. Import the necessary components:
   ```python
   from pmoai import Agent, Task, Crew, Process
   from pmoai.tools.pm_specific import ProjectCharterTool, RiskRegisterTool
   ```

2. Create PM-specific agents with relevant expertise:
   ```python
   project_manager = Agent(
       role="Project Manager",
       goal="Successfully plan and execute the project",
       backstory="You are an experienced project manager with PMP certification.",
       pm_methodology="Agile",
       certifications=["PMP", "CSM"],
       industry_expertise=["Software Development"]
   )
   ```

3. Create PM tasks with appropriate tools:
   ```python
   charter_task = Task(
       description="Create a project charter for a new software development project",
       expected_output="A comprehensive project charter document",
       agent=project_manager,
       tools=[ProjectCharterTool()],
       pm_phase="Initiation",
       priority="High"
   )
   ```

4. Create a PM crew and execute it:
   ```python
   project_crew = Crew(
       agents=[project_manager],
       tasks=[charter_task],
       process=Process.sequential,
       project_name="My Project",
       project_methodology="Agile"
   )
   
   result = project_crew.kickoff()
   print(result.raw)
   ```
