# {{crew_name}}

This is a PMOAI crew for project management tasks.

## Project Management Methodology

This crew uses the following project management methodology:
- Methodology: Agile (default, can be configured)
- Phase: Planning (default, can be configured)

## Installation

```bash
pip install -e .
```

## Usage

```python
from {{folder_name}}.crew import {{crew_name}}

# Create the crew
crew = {{crew_name}}()

# Configure project properties
crew.project_name = "My Project"
crew.project_code = "PRJ-001"
crew.project_methodology = "Agile"
crew.project_phase = "Planning"
crew.organization = "My Organization"
crew.portfolio = "My Portfolio"

# Run the crew
result = crew.kickoff()

# Print the result
print(result.raw)
```

## CLI Usage

```bash
# Run the crew
pmoai run --project-name "My Project" --project-code "PRJ-001" --methodology "Agile" --phase "Planning"

# Reset memories
pmoai reset-memories --all
```

## Configuration

The crew is configured using YAML files in the `config` directory:

- `agents.yaml`: Defines the agents in the crew
- `tasks.yaml`: Defines the tasks for the crew

## Tools

Custom tools are defined in the `tools` directory.

## Knowledge

Project-specific knowledge is stored in the `knowledge` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
