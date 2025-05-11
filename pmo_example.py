"""
Example script demonstrating how to use CrewAI for Project Management Office (PMO) tasks.
"""

from crewai import Agent, Task, Crew
import os

# Set the OpenAI API key from environment variable
# If you've set the API key using the 'set' command in the terminal, it should be available
# If not, uncomment and set it directly:
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Check if API key is set
if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
    print("Warning: OPENAI_API_KEY environment variable not found or empty.")
    print("You can set it directly in this script or use the 'set' command in your terminal.")
    print("Example: set OPENAI_API_KEY=your-api-key-here")
    api_key = input("Enter your OpenAI API key to continue (or press Enter to skip running the crew): ")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

# Create PMO agents
project_manager = Agent(
    role="Project Manager",
    goal="Ensure the project is completed on time and within budget",
    backstory="""You are an experienced project manager with a track record of successful project deliveries.
    You excel at planning, coordination, and risk management. You have a PMP certification and
    10+ years of experience managing software development projects.""",
    verbose=True
)

business_analyst = Agent(
    role="Business Analyst",
    goal="Gather and document requirements from stakeholders",
    backstory="""You are a skilled business analyst with expertise in requirements gathering and documentation.
    You have a knack for understanding business needs and translating them into technical requirements.
    You have 8+ years of experience working on enterprise software projects.""",
    verbose=True
)

risk_manager = Agent(
    role="Risk Manager",
    goal="Identify and mitigate project risks",
    backstory="""You are a detail-oriented risk manager with expertise in risk assessment and mitigation.
    You have a strong background in project management and risk analysis. You have 7+ years of
    experience managing risks for complex software projects.""",
    verbose=True
)

# Create PMO tasks
project_planning_task = Task(
    description="""Create a comprehensive project plan for a new CRM implementation project.
    The plan should include:
    1. Project scope and objectives
    2. Timeline with key milestones
    3. Resource allocation
    4. Budget estimation
    5. Communication plan""",
    expected_output="A detailed project plan document with all the required components",
    agent=project_manager
)

requirements_gathering_task = Task(
    description="""Gather and document requirements for the CRM implementation project.
    You should:
    1. Identify key stakeholders
    2. Conduct stakeholder interviews
    3. Document functional requirements
    4. Document non-functional requirements
    5. Create user stories""",
    expected_output="A comprehensive requirements document with user stories",
    agent=business_analyst
)

risk_assessment_task = Task(
    description="""Perform a risk assessment for the CRM implementation project.
    You should:
    1. Identify potential risks
    2. Assess the likelihood and impact of each risk
    3. Develop mitigation strategies
    4. Create a risk register
    5. Define risk monitoring procedures""",
    expected_output="A detailed risk assessment document with mitigation strategies",
    agent=risk_manager
)

# Create the PMO crew
pmo_crew = Crew(
    agents=[project_manager, business_analyst, risk_manager],
    tasks=[project_planning_task, requirements_gathering_task, risk_assessment_task],
    verbose=True
)

print("PMO Crew created successfully!")
print(f"Agents: {[agent.role for agent in pmo_crew.agents]}")
print(f"Tasks: {[task.description.split('.')[0] for task in pmo_crew.tasks]}")
print(f"Crew ID: {pmo_crew.id}")

# Check if we have an API key before running the crew
if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"]:
    print("\nAPI key found. Running the PMO crew...")
    try:
        # Run the crew and get the results
        result = pmo_crew.kickoff()

        # Print the results
        print("\n" + "="*50)
        print("PMO CREW RESULTS:")
        print("="*50)
        print(result)
        print("="*50)
    except Exception as e:
        print(f"\nError running the crew: {e}")
        print("Please check your API key and internet connection.")
else:
    # We don't have an API key, so we can't run the crew
    print("\nNo API key available. Skipping crew execution.")
    print("To run the PMO crew, you would need to set your OpenAI API key and call pmo_crew.kickoff()")
    print("Example: result = pmo_crew.kickoff()")
