from pmoai import Agent, Crew, Process, Task
from pmoai.project import CrewBase, agent, crew, task
from pmoai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class {{crew_name}}():
    """{{crew_name}} crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    # Project Management specific properties
    project_name: str = "Project Name"
    project_code: str = "PRJ-001"
    project_methodology: str = "Agile"
    project_phase: str = "Planning"
    organization: str = "Organization Name"
    portfolio: str = "Portfolio Name"

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['project_manager'], # type: ignore[index]
            verbose=True
        )

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_analyst'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def requirements_gathering_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirements_gathering_task'], # type: ignore[index]
        )

    @task
    def project_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_planning_task'], # type: ignore[index]
            output_file='project_plan.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the {{crew_name}} crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
