"""
Example script to use CrewAI directly.
"""

from crewai import Agent, Task, Crew

# Create a project manager agent
project_manager = Agent(
    role="Project Manager",
    goal="Ensure the project is completed on time and within budget",
    backstory="You are an experienced project manager with a track record of successful project deliveries.",
    verbose=True
)

# Create a developer agent
developer = Agent(
    role="Developer",
    goal="Implement high-quality code that meets the requirements",
    backstory="You are a skilled developer with expertise in multiple programming languages and frameworks.",
    verbose=True
)

# Create a tester agent
tester = Agent(
    role="Quality Assurance Tester",
    goal="Ensure the software is bug-free and meets quality standards",
    backstory="You are a detail-oriented tester with a knack for finding edge cases and bugs.",
    verbose=True
)

# Create tasks for the project
planning_task = Task(
    description="Create a project plan with milestones and deadlines",
    expected_output="A detailed project plan with timeline and resource allocation",
    agent=project_manager
)

development_task = Task(
    description="Implement the core features of the application",
    expected_output="Working code that implements the required features",
    agent=developer
)

testing_task = Task(
    description="Test the application for bugs and issues",
    expected_output="A test report with findings and recommendations",
    agent=tester
)

# Create a crew with the agents and tasks
crew = Crew(
    agents=[project_manager, developer, tester],
    tasks=[planning_task, development_task, testing_task],
    verbose=True
)

# Run the crew
result = crew.kickoff()

print("\nFinal Result:")
print(result)
