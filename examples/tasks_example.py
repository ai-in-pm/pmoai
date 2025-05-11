"""Example of using the tasks module in PMOAI."""

from pmoai.agent import Agent
from pmoai.llm import LLM
from pmoai.task import Task
from pmoai.tasks import (
    ConditionalTask,
    LLMGuardrail,
    OutputFormat,
    TaskOutput,
)


def main():
    """Run the tasks example."""
    # Initialize an LLM
    llm = LLM(provider="openai")
    
    # Create agents
    project_manager = Agent(
        role="Project Manager",
        goal="Ensure the project is completed on time and within budget",
        backstory="You are an experienced project manager with a track record of successful projects.",
        llm=llm,
    )
    
    business_analyst = Agent(
        role="Business Analyst",
        goal="Gather and analyze requirements from stakeholders",
        backstory="You are a skilled business analyst with expertise in requirements gathering and analysis.",
        llm=llm,
    )
    
    # Create a regular task
    requirements_task = Task(
        description="Gather requirements for the new project management system",
        expected_output="A comprehensive list of functional and non-functional requirements",
        agent=business_analyst,
    )
    
    # Create a task with JSON output format
    json_task = Task(
        description="Create a project timeline with key milestones",
        expected_output="A JSON object with project milestones and dates",
        agent=project_manager,
        output_format=OutputFormat.JSON,
    )
    
    # Create a conditional task that only executes if the requirements task output contains "user authentication"
    def check_auth_requirement(task_output: TaskOutput) -> bool:
        return "user authentication" in task_output.raw.lower()
    
    auth_task = ConditionalTask(
        description="Design the user authentication system",
        expected_output="A detailed design document for the authentication system",
        agent=project_manager,
        condition=check_auth_requirement,
    )
    
    # Create a guardrail for validating task output
    budget_guardrail = LLMGuardrail(
        description="The budget must be between $100,000 and $500,000",
        llm=llm,
    )
    
    # Example of task execution and guardrail validation
    print("Task Example:")
    print(f"Task: {requirements_task.description}")
    print(f"Agent: {requirements_task.agent.role}")
    print(f"Expected Output: {requirements_task.expected_output}")
    
    print("\nConditional Task Example:")
    print(f"Task: {auth_task.description}")
    print(f"Condition: Task output must contain 'user authentication'")
    
    # Example of a task output
    task_output = TaskOutput(
        description=requirements_task.description,
        expected_output=requirements_task.expected_output,
        raw="""
        Functional Requirements:
        1. User authentication and authorization
        2. Project creation and management
        3. Task assignment and tracking
        4. Resource allocation
        5. Gantt chart visualization
        6. Budget tracking
        
        Non-functional Requirements:
        1. Performance: The system should respond within 2 seconds
        2. Scalability: Support up to 1000 concurrent users
        3. Security: Data encryption and secure authentication
        4. Usability: Intuitive user interface
        """,
        agent=business_analyst.role,
        output_format=OutputFormat.RAW,
    )
    
    print("\nTask Output Example:")
    print(f"Raw Output: {task_output.raw[:100]}...")
    
    # Check if conditional task should execute
    should_execute = auth_task.should_execute(task_output)
    print(f"\nShould execute auth task? {should_execute}")
    
    # Example of guardrail validation
    budget_output = TaskOutput(
        description="Prepare project budget",
        raw="The total project budget is $600,000",
        agent=project_manager.role,
        output_format=OutputFormat.RAW,
    )
    
    print("\nGuardrail Example:")
    print(f"Budget Output: {budget_output.raw}")
    print("Validating against budget guardrail...")
    # Note: In a real scenario, this would call the LLM
    print("Expected result: Invalid - budget exceeds maximum of $500,000")


if __name__ == "__main__":
    main()
