import os
from dotenv import load_dotenv

from pmoai.config import ConfigLoader

# Load environment variables from .env file
load_dotenv()

# Ensure you have set your OpenAI API key in the .env file or as an environment variable
# Example: OPENAI_API_KEY=your-api-key

def main():
    # Load configurations
    config_loader = ConfigLoader()
    
    # Print available agents, tasks, and crews
    print("=== Available Agents ===")
    for agent_name in config_loader.agents_config:
        print(f"- {agent_name}: {config_loader.agents_config[agent_name]['role']}")
    
    print("\n=== Available Tasks ===")
    for task_name in config_loader.tasks_config:
        print(f"- {task_name}: {config_loader.tasks_config[task_name]['description'][:50]}...")
    
    print("\n=== Available Crews ===")
    for crew_name in config_loader.crews_config:
        print(f"- {crew_name}")
    
    # Create a project initiation crew
    print("\n=== Creating Project Initiation Crew ===")
    crew = config_loader.get_crew("project_initiation_crew")
    
    # Update crew properties for this specific project
    crew.project_name = "E-commerce Website Development"
    crew.project_code = "EWD-2023"
    crew.organization = "Online Retail Inc."
    crew.portfolio = "Digital Transformation"
    
    # Execute the crew
    print("\n=== Executing Project Initiation Crew ===")
    print("This will use your OpenAI API key to generate content.")
    print("Press Ctrl+C to cancel or Enter to continue...")
    input()
    
    result = crew.kickoff()
    
    # Print the results
    print("\n=== Project Initiation Results ===\n")
    print(result.raw)
    
    # Save the results to files
    print("\n=== Saving Results to Files ===")
    for i, task_output in enumerate(result.tasks_output):
        filename = f"output_{i+1}_{task_output.task.description.split()[0].lower()}.md"
        with open(filename, "w") as f:
            f.write(task_output.raw)
        print(f"Saved {filename}")


if __name__ == "__main__":
    main()
