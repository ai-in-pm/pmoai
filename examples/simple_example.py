import os
from dotenv import load_dotenv

from pmoai import Agent, Task, Crew, Process
from pmoai.tools.pm_specific import ProjectCharterTool

# Load environment variables from .env file
load_dotenv()

# Ensure you have set your OpenAI API key in the .env file or as an environment variable
# Example: OPENAI_API_KEY=your-api-key

def main():
    # Create a project manager agent
    project_manager = Agent(
        role="Project Manager",
        goal="Successfully plan and execute the project",
        backstory="You are an experienced project manager with PMP certification and 10 years of experience in software development projects.",
        pm_methodology="Agile",
        certifications=["PMP", "CSM"],
        industry_expertise=["Software Development", "IT"],
        verbose=True
    )

    # Create a project charter task
    charter_task = Task(
        description="Create a project charter for a new website development project for a small business. The website should include an about page, services page, contact form, and blog.",
        expected_output="A comprehensive project charter document",
        agent=project_manager,
        tools=[ProjectCharterTool()],
        pm_phase="Initiation",
        priority="High",
        estimated_duration=2.0,
        deliverables=["Project Charter Document"],
        stakeholders=["Business Owner", "Marketing Team", "IT Department"]
    )

    # Create a project crew
    project_crew = Crew(
        agents=[project_manager],
        tasks=[charter_task],
        process=Process.sequential,
        verbose=True,
        project_name="Small Business Website Development",
        project_code="SBWD-2023",
        project_methodology="Agile",
        project_phase="Initiation",
        organization="Small Business Inc.",
        portfolio="Digital Transformation"
    )

    # Execute the crew
    result = project_crew.kickoff()
    
    # Print the results
    print("\n\n=== PROJECT CHARTER ===\n")
    print(result.raw)
    
    # Save the results to a file
    with open("project_charter.md", "w") as f:
        f.write(result.raw)
    
    print("\nProject charter has been saved to project_charter.md")


if __name__ == "__main__":
    main()
