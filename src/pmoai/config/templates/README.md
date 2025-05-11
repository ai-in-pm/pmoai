# PMOAI Configuration Templates

This directory contains YAML configuration templates for PMOAI.

## Files

- `agents.yaml`: Defines the agents that will be used in the project.
- `tasks.yaml`: Defines the tasks that will be executed in the project.
- `crews.yaml`: Defines the crews that will be used in the project.

## Usage

You can use these templates as a starting point for your own configuration files. To create your own configuration files, run:

```bash
pmoai init --output-dir your_config_dir
```

This will copy these templates to your specified directory, where you can customize them for your project.

## Format

### agents.yaml

```yaml
agent_name:
  role: "Agent Role"
  goal: "Agent Goal"
  backstory: "Agent Backstory"
  pm_methodology: "Agile"
  certifications: ["Cert1", "Cert2"]
  industry_expertise: ["Industry1", "Industry2"]
  verbose: true
  allow_delegation: true
```

### tasks.yaml

```yaml
task_name:
  description: "Task Description"
  expected_output: "Expected Output"
  agent: "agent_name"
  pm_phase: "Phase"
  priority: "High"
  dependencies: ["other_task_name"]
  estimated_duration: 4.0
  deliverables: ["Deliverable1", "Deliverable2"]
  stakeholders: ["Stakeholder1", "Stakeholder2"]
  tools: ["ToolName1", "ToolName2"]
```

### crews.yaml

```yaml
crew_name:
  agents: ["agent_name1", "agent_name2"]
  tasks: ["task_name1", "task_name2"]
  process: "sequential"
  verbose: true
  project_name: "Project Name"
  project_code: "PRJ-2023"
  project_methodology: "Agile"
  project_phase: "Phase"
  organization: "Organization Name"
  portfolio: "Portfolio Name"
```
