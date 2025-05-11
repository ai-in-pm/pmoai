import os
from dotenv import load_dotenv

from pmoai import Agent, Crew, Process, Task
from pmoai.tools.pm_specific import ProjectCharterTool, RiskRegisterTool, StakeholderCommunicationTool

# Load environment variables from .env file
load_dotenv()

# Ensure you have set your OpenAI API key in the .env file or as an environment variable
# Example: OPENAI_API_KEY=your-api-key

def main():
    # Create PM-specific agents
    project_manager = Agent(
        role="Project Manager",
        goal="Successfully plan and execute the project",
        backstory="You are an experienced project manager with PMP certification and 10 years of experience in software development projects.",
        pm_methodology="Agile",
        certifications=["PMP", "CSM"],
        industry_expertise=["Software Development", "IT"],
        verbose=True
    )

    risk_analyst = Agent(
        role="Risk Analyst",
        goal="Identify and analyze project risks",
        backstory="You specialize in risk management for complex projects with a focus on software development risks.",
        pm_methodology="Agile",
        certifications=["PMI-RMP"],
        industry_expertise=["Software Development", "Cybersecurity"],
        verbose=True
    )

    stakeholder_manager = Agent(
        role="Stakeholder Manager",
        goal="Manage stakeholder expectations and communications",
        backstory="You are an expert in stakeholder management with experience in aligning diverse stakeholder interests.",
        pm_methodology="Agile",
        certifications=["CBAP"],
        industry_expertise=["Software Development", "Business Analysis"],
        verbose=True
    )

    # Create PM tasks
    charter_task = Task(
        description="Create a project charter for a new mobile banking application development project. The project aims to develop a secure and user-friendly mobile banking application for a mid-sized bank. The application should allow customers to check balances, transfer funds, pay bills, and deposit checks via mobile capture.",
        expected_output="A comprehensive project charter document",
        agent=project_manager,
        tools=[ProjectCharterTool()],
        pm_phase="Initiation",
        priority="High",
        estimated_duration=4.0,
        deliverables=["Project Charter Document"],
        stakeholders=["Bank Executive Team", "IT Department", "Compliance Officer", "Customer Representatives"]
    )

    risk_task = Task(
        description="Identify potential risks for the mobile banking application development project. Consider technical risks, security risks, compliance risks, resource risks, and schedule risks.",
        expected_output="A risk register with at least 5 key risks and mitigation strategies",
        agent=risk_analyst,
        tools=[RiskRegisterTool()],
        pm_phase="Initiation",
        priority="High",
        dependencies=["Project Charter"],
        estimated_duration=3.0,
        deliverables=["Risk Register"],
        stakeholders=["Project Manager", "Bank Executive Team", "IT Security Team", "Compliance Officer"]
    )

    stakeholder_task = Task(
        description="Create a stakeholder communication plan for the mobile banking application development project. Identify key stakeholders, their interests, influence, and appropriate communication strategies.",
        expected_output="A comprehensive stakeholder communication plan",
        agent=stakeholder_manager,
        tools=[StakeholderCommunicationTool()],
        pm_phase="Initiation",
        priority="Medium",
        dependencies=["Project Charter"],
        estimated_duration=2.5,
        deliverables=["Stakeholder Communication Plan"],
        stakeholders=["Project Manager", "Bank Executive Team", "IT Department", "Marketing Team", "Customer Service Team"]
    )

    # Create a PM crew
    project_crew = Crew(
        agents=[project_manager, risk_analyst, stakeholder_manager],
        tasks=[charter_task, risk_task, stakeholder_task],
        process=Process.sequential,
        verbose=True,
        project_name="Mobile Banking Application Development",
        project_code="MBAD-2023",
        project_methodology="Agile",
        project_phase="Initiation",
        organization="Mid-Size Bank",
        portfolio="Digital Transformation"
    )

    # Execute the crew
    result = project_crew.kickoff()
    
    # Print the results
    print("\n\n=== PROJECT INITIATION RESULTS ===\n")
    print(result.raw)
    
    # Save the results to files
    with open("project_charter.md", "w") as f:
        f.write(result.tasks_output[0].raw)
    
    with open("risk_register.md", "w") as f:
        f.write(result.tasks_output[1].raw)
    
    with open("stakeholder_communication_plan.md", "w") as f:
        f.write(result.tasks_output[2].raw)
    
    print("\nResults have been saved to files: project_charter.md, risk_register.md, stakeholder_communication_plan.md")


if __name__ == "__main__":
    main()
