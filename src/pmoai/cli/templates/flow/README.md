# {{class_name}}

This is a PMOAI flow for project management tasks.

## Project Management Methodology

This flow uses the following project management methodology:
- Methodology: Agile (default, can be configured)
- Phase: Planning (default, can be configured)

## Installation

```bash
pip install -e .
```

## Usage

```python
from {{folder_name}}.flow import {{class_name}}

# Create the flow
flow = {{class_name}}()

# Configure project properties
flow.project_name = "My Project"
flow.project_code = "PRJ-001"
flow.project_methodology = "Agile"
flow.project_phase = "Planning"
flow.organization = "My Organization"
flow.portfolio = "My Portfolio"

# Run the flow
result = flow.kickoff()

# Print the result
print(result.raw)
```

## CLI Usage

```bash
# Run the flow
pmoai flow kickoff --project-name "My Project" --project-code "PRJ-001" --methodology "Agile" --phase "Planning"

# Add a crew to the flow
pmoai flow add-crew my_crew

# Plot the flow
pmoai flow plot
```

## Crews

Crews are defined in the `crews` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
