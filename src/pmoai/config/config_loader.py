import os
import yaml
from typing import Dict, Any, List, Optional, Union

import pkg_resources

from pmoai.agent import Agent
from pmoai.task import Task
from pmoai.crew import Crew
from pmoai.process import Process
from pmoai.tools.pm_specific import (
    GanttChartTool,
    ProjectCharterTool,
    ResourceAllocationTool,
    RiskRegisterTool,
    StakeholderCommunicationTool,
)


class ConfigLoader:
    """Loader for PMOAI configuration files."""

    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the ConfigLoader.
        
        Args:
            config_dir: Directory containing configuration files. If None, uses the default templates.
        """
        self.config_dir = config_dir
        self.agents_config = {}
        self.tasks_config = {}
        self.crews_config = {}
        self.tools_map = {
            "ProjectCharterTool": ProjectCharterTool(),
            "RiskRegisterTool": RiskRegisterTool(),
            "ResourceAllocationTool": ResourceAllocationTool(),
            "GanttChartTool": GanttChartTool(),
            "StakeholderCommunicationTool": StakeholderCommunicationTool(),
        }
        
        # Load configurations
        self._load_configs()
    
    def _load_configs(self) -> None:
        """Load all configuration files."""
        self.agents_config = self._load_config_file("agents.yaml")
        self.tasks_config = self._load_config_file("tasks.yaml")
        self.crews_config = self._load_config_file("crews.yaml")
    
    def _load_config_file(self, filename: str) -> Dict[str, Any]:
        """Load a configuration file.
        
        Args:
            filename: Name of the configuration file.
            
        Returns:
            Dictionary containing the configuration.
        """
        if self.config_dir and os.path.exists(os.path.join(self.config_dir, filename)):
            # Load from user-provided directory
            with open(os.path.join(self.config_dir, filename), "r") as f:
                return yaml.safe_load(f)
        else:
            # Load from package templates
            template_path = pkg_resources.resource_filename(
                "pmoai", f"config/templates/{filename}"
            )
            if os.path.exists(template_path):
                with open(template_path, "r") as f:
                    return yaml.safe_load(f)
            else:
                return {}
    
    def get_agent(self, agent_name: str) -> Agent:
        """Get an agent by name.
        
        Args:
            agent_name: Name of the agent in the configuration.
            
        Returns:
            Agent instance.
            
        Raises:
            ValueError: If the agent is not found in the configuration.
        """
        if agent_name not in self.agents_config:
            raise ValueError(f"Agent '{agent_name}' not found in configuration.")
        
        agent_config = self.agents_config[agent_name]
        
        return Agent(
            role=agent_config["role"],
            goal=agent_config["goal"],
            backstory=agent_config["backstory"],
            pm_methodology=agent_config.get("pm_methodology"),
            certifications=agent_config.get("certifications"),
            industry_expertise=agent_config.get("industry_expertise"),
            verbose=agent_config.get("verbose", False),
            allow_delegation=agent_config.get("allow_delegation", True),
        )
    
    def get_task(self, task_name: str, agents: Optional[Dict[str, Agent]] = None) -> Task:
        """Get a task by name.
        
        Args:
            task_name: Name of the task in the configuration.
            agents: Dictionary of agent instances by name.
            
        Returns:
            Task instance.
            
        Raises:
            ValueError: If the task is not found in the configuration.
        """
        if task_name not in self.tasks_config:
            raise ValueError(f"Task '{task_name}' not found in configuration.")
        
        task_config = self.tasks_config[task_name]
        
        # Get agent if specified
        agent = None
        if "agent" in task_config and agents and task_config["agent"] in agents:
            agent = agents[task_config["agent"]]
        
        # Get tools if specified
        tools = []
        if "tools" in task_config:
            for tool_name in task_config["tools"]:
                if tool_name in self.tools_map:
                    tools.append(self.tools_map[tool_name])
        
        return Task(
            description=task_config["description"],
            expected_output=task_config["expected_output"],
            agent=agent,
            tools=tools,
            pm_phase=task_config.get("pm_phase"),
            priority=task_config.get("priority"),
            dependencies=task_config.get("dependencies"),
            estimated_duration=task_config.get("estimated_duration"),
            deliverables=task_config.get("deliverables"),
            stakeholders=task_config.get("stakeholders"),
        )
    
    def get_crew(self, crew_name: str) -> Crew:
        """Get a crew by name.
        
        Args:
            crew_name: Name of the crew in the configuration.
            
        Returns:
            Crew instance.
            
        Raises:
            ValueError: If the crew is not found in the configuration.
        """
        if crew_name not in self.crews_config:
            raise ValueError(f"Crew '{crew_name}' not found in configuration.")
        
        crew_config = self.crews_config[crew_name]
        
        # Get agents
        agents = {}
        agent_instances = []
        for agent_name in crew_config["agents"]:
            agent = self.get_agent(agent_name)
            agents[agent_name] = agent
            agent_instances.append(agent)
        
        # Get tasks
        task_instances = []
        for task_name in crew_config["tasks"]:
            task = self.get_task(task_name, agents)
            task_instances.append(task)
        
        # Get process
        process_name = crew_config.get("process", "sequential")
        process = getattr(Process, process_name)
        
        return Crew(
            agents=agent_instances,
            tasks=task_instances,
            process=process,
            verbose=crew_config.get("verbose", False),
            project_name=crew_config.get("project_name"),
            project_code=crew_config.get("project_code"),
            project_methodology=crew_config.get("project_methodology"),
            project_phase=crew_config.get("project_phase"),
            organization=crew_config.get("organization"),
            portfolio=crew_config.get("portfolio"),
        )
