import unittest

from pmoai import Agent, Crew, Process, Task
from pmoai.tools.pm_specific import ProjectCharterTool


class TestPMOAICore(unittest.TestCase):
    def test_agent_creation(self):
        """Test that a PM agent can be created with PM-specific attributes."""
        agent = Agent(
            role="Project Manager",
            goal="Successfully plan and execute the project",
            backstory="You are an experienced project manager with PMP certification.",
            pm_methodology="Agile",
            certifications=["PMP", "CSM"],
            industry_expertise=["Software Development", "IT"]
        )
        
        self.assertEqual(agent.role, "Project Manager")
        self.assertEqual(agent.goal, "Successfully plan and execute the project")
        self.assertEqual(agent.pm_methodology, "Agile")
        self.assertEqual(agent.certifications, ["PMP", "CSM"])
        self.assertEqual(agent.industry_expertise, ["Software Development", "IT"])
    
    def test_task_creation(self):
        """Test that a PM task can be created with PM-specific attributes."""
        task = Task(
            description="Create a project charter",
            expected_output="A comprehensive project charter document",
            pm_phase="Initiation",
            priority="High",
            estimated_duration=4.0,
            deliverables=["Project Charter Document"],
            stakeholders=["Executive Team", "Project Team"]
        )
        
        self.assertEqual(task.description, "Create a project charter")
        self.assertEqual(task.expected_output, "A comprehensive project charter document")
        self.assertEqual(task.pm_phase, "Initiation")
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.estimated_duration, 4.0)
        self.assertEqual(task.deliverables, ["Project Charter Document"])
        self.assertEqual(task.stakeholders, ["Executive Team", "Project Team"])
    
    def test_crew_creation(self):
        """Test that a PM crew can be created with PM-specific attributes."""
        agent = Agent(
            role="Project Manager",
            goal="Successfully plan and execute the project",
            backstory="You are an experienced project manager with PMP certification."
        )
        
        task = Task(
            description="Create a project charter",
            expected_output="A comprehensive project charter document",
            agent=agent
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            project_name="Test Project",
            project_code="TP-2023",
            project_methodology="Agile",
            project_phase="Initiation",
            organization="Test Organization",
            portfolio="Test Portfolio"
        )
        
        self.assertEqual(crew.project_name, "Test Project")
        self.assertEqual(crew.project_code, "TP-2023")
        self.assertEqual(crew.project_methodology, "Agile")
        self.assertEqual(crew.project_phase, "Initiation")
        self.assertEqual(crew.organization, "Test Organization")
        self.assertEqual(crew.portfolio, "Test Portfolio")
    
    def test_process_enum(self):
        """Test that the Process enum includes PM-specific processes."""
        self.assertEqual(Process.sequential, "sequential")
        self.assertEqual(Process.hierarchical, "hierarchical")
        self.assertEqual(Process.agile, "agile")
        self.assertEqual(Process.waterfall, "waterfall")
        self.assertEqual(Process.kanban, "kanban")
        self.assertEqual(Process.hybrid, "hybrid")
    
    def test_project_charter_tool(self):
        """Test that the ProjectCharterTool can be instantiated."""
        tool = ProjectCharterTool()
        self.assertEqual(tool.name, "Project Charter Generator")
        self.assertTrue("Creates a comprehensive project charter document" in tool.description)


if __name__ == "__main__":
    unittest.main()
