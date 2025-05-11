"""
Simple script to use CrewAI directly.
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

# Create a simple agent
agent = Agent(
    role="Test Agent",
    goal="Test the CrewAI installation",
    backstory="I am a test agent created to verify the CrewAI installation.",
    verbose=True
)

# Create a simple task
task = Task(
    description="Test task",
    expected_output="Test output",
    agent=agent
)

# Create a simple crew
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

print("CrewAI objects created successfully!")
print(f"Agent: {agent.role}")
print(f"Task: {task.description}")
print(f"Crew: {crew.id}")

# Check if we have an API key before running the crew
if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"]:
    print("\nAPI key found. Running the crew...")
    try:
        # Run the crew and get the results
        result = crew.kickoff()

        # Print the results
        print("\n" + "="*50)
        print("CREW RESULTS:")
        print("="*50)
        print(result)
        print("="*50)
    except Exception as e:
        print(f"\nError running the crew: {e}")
        print("Please check your API key and internet connection.")
else:
    # We don't have an API key, so we can't run the crew
    print("\nNo API key available. Skipping crew execution.")
    print("To run the crew, you would need to set your OpenAI API key and call crew.kickoff()")
    print("Example: crew.kickoff()")
