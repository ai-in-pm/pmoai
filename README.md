# PMOAI: Project Management Office AI Agents

![pmoai_icon](https://github.com/user-attachments/assets/0cea089e-0f9b-43f5-b83e-b75e12a674d4)


PMOAI is a specialized framework for orchestrating AI agents focused on project management tasks. Built on top of CrewAI, PMOAI extends its capabilities with PM-specific agents, tasks, and tools to help automate and enhance project management workflows.

## Overview

Project Management Office (PMO) AI Agents are designed to assist project managers, stakeholders, and team members throughout the project lifecycle. By leveraging large language models (LLMs) and agent-based architectures, PMOAI can help with various project management activities such as planning, risk assessment, resource allocation, and status reporting.

## Features

- **PM-Specific Agents**: Pre-configured agents for common project management roles:
  - Project Manager
  - Business Analyst
  - Risk Manager
  - Resource Manager
  - Quality Assurance
  - Stakeholder Manager

- **PM Workflows**: Specialized workflows for:
  - Project initiation
  - Planning and scheduling
  - Execution and monitoring
  - Risk management
  - Resource allocation
  - Project closing

- **PM Tools**: Tools for creating project documentation, analyzing risks, managing resources, and more

- **Knowledge Integration**: Incorporate PM methodologies, best practices, and organizational knowledge

- **Flexible Architecture**: Support for different PM methodologies (Agile, Waterfall, Hybrid, etc.)

## Installation

### Prerequisites

- Python 3.9+
- An OpenAI API key (for LLM functionality)
- Git (for cloning the repository)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pmoai.git
cd pmoai
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -e .
pip install tensorflow tensorflow-probability tf-keras
```

5. Set up your OpenAI API key:
```bash
# On Windows
set OPENAI_API_KEY=your-api-key-here

# On macOS/Linux
export OPENAI_API_KEY=your-api-key-here
```

## Usage

Due to some dependency issues in the current version, it's recommended to use CrewAI directly for project management tasks. Here's an example:

```python
from crewai import Agent, Task, Crew
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Create PM-specific agents
project_manager = Agent(
    role="Project Manager",
    goal="Successfully plan and execute the project",
    backstory="You are an experienced project manager with PMP certification and 10+ years of experience in software development projects."
)

risk_analyst = Agent(
    role="Risk Analyst",
    goal="Identify and analyze project risks",
    backstory="You specialize in risk management for complex projects with a focus on technical and organizational risks."
)

# Create PM tasks
planning_task = Task(
    description="Create a project charter for a new software development project. Include project objectives, scope, stakeholders, and high-level timeline.",
    expected_output="A comprehensive project charter document",
    agent=project_manager
)

risk_task = Task(
    description="Identify potential risks for the software development project and develop mitigation strategies.",
    expected_output="A risk register with at least 5 key risks and mitigation strategies",
    agent=risk_analyst
)

# Create a PM crew
project_crew = Crew(
    agents=[project_manager, risk_analyst],
    tasks=[planning_task, risk_task],
    verbose=True
)

# Execute the crew
result = project_crew.kickoff()
print(result)
```

## Running PMOAI

### Setting Up Your OpenAI API Key

Before running any examples, you need to set up your OpenAI API key. You have several options:

1. **Using the new utility script (recommended):**
   ```bash
   # Activate your virtual environment first
   python utilities/set_openai_key.py
   ```
   This script will:
   - Prompt you for your OpenAI API key
   - Clean and validate the key format
   - Set it in the current environment
   - Update the .env file
   - Create a batch file for future use

2. **Setting the environment variable manually:**
   ```bash
   # On Windows Command Prompt (do NOT include 'set' in the actual key)
   set OPENAI_API_KEY=sk-your-actual-api-key-here

   # On Windows PowerShell
   $env:OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```

3. **Editing the .env file directly:**
   Open the `.env` file in the root directory and add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. **Editing the example scripts directly:**
   Open the example scripts and uncomment the line:
   ```python
   # os.environ["OPENAI_API_KEY"] = "sk-your-actual-api-key-here"
   ```
   Replace `sk-your-actual-api-key-here` with your actual API key.

> **Important Note**: When entering your API key, make sure to:
> - Include ONLY the key itself (it typically starts with "sk-")
> - Do NOT include "set" or "OPENAI_API_KEY=" as part of the key
> - Do NOT include quotes around the key unless specifically instructed

### Running the Example Scripts

The repository includes several example scripts to help you get started:

- `use_crewai_simple.py`: A minimal example of using CrewAI
- `pmo_example.py`: A more comprehensive example of using CrewAI for project management tasks

To run these examples:

```bash
# Activate your virtual environment first
python use_crewai_simple.py
# or
python pmo_example.py
```

The scripts have been updated to:
- Check if your API key is set
- Prompt you to enter it if it's missing
- Run the crew if the API key is available
- Display the results

## Project Structure

```
pmoai/
├── src/                  # Source code
│   └── pmoai/
│       ├── agents/       # Agent definitions and adapters
│       ├── flow/         # Workflow definitions
│       ├── knowledge/    # Knowledge base components
│       ├── memory/       # Memory components
│       ├── tasks/        # Task definitions
│       ├── tools/        # PM-specific tools
│       └── utilities/    # Utility functions
├── tests/                # Test suite
├── examples/             # Example scripts
├── venv/                 # Virtual environment (created during setup)
├── setup.py              # Package setup file
└── README.md             # This file
```

## Known Issues

- There are circular import issues in the current codebase that need to be resolved
- The package has dependencies on older versions of TensorFlow that use the deprecated `tf.contrib` module
- Some agent adapters have compatibility issues with the latest versions of their dependencies
- The OpenAI API key is required for LLM functionality

## Troubleshooting

If you encounter issues with TensorFlow dependencies, try the following:

```bash
# Install the patch scripts
python patch_tensorflow.py
python patch_agents.py
```

These scripts create mock modules for the missing TensorFlow components and agent tools.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here are some areas where help is needed:

- Fixing circular import issues
- Updating dependencies to work with modern versions of TensorFlow
- Adding more PM-specific tools and agents
- Improving documentation and examples

## License

MIT
