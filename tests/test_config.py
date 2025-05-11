import os
import unittest
import tempfile
import yaml

from pmoai.config import ConfigLoader
from pmoai.agent import Agent
from pmoai.task import Task
from pmoai.crew import Crew
from pmoai.process import Process


class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test config files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create test config files
        self.create_test_config_files()
        
        # Create config loader
        self.config_loader = ConfigLoader(self.temp_dir.name)
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def create_test_config_files(self):
        """Create test configuration files."""
        # Create agents.yaml
        agents_config = {
            "test_agent": {
                "role": "Test Agent",
                "goal": "Test the config loader",
                "backstory": "You are a test agent created for unit testing.",
                "pm_methodology": "Agile",
                "certifications": ["Test Cert"],
                "industry_expertise": ["Testing"],
                "verbose": True,
                "allow_delegation": True
            }
        }
        
        with open(os.path.join(self.temp_dir.name, "agents.yaml"), "w") as f:
            yaml.dump(agents_config, f)
        
        # Create tasks.yaml
        tasks_config = {
            "test_task": {
                "description": "Test task for unit testing",
                "expected_output": "Test output",
                "agent": "test_agent",
                "pm_phase": "Testing",
                "priority": "High",
                "estimated_duration": 1.0,
                "deliverables": ["Test Deliverable"],
                "stakeholders": ["Test Stakeholder"]
            }
        }
        
        with open(os.path.join(self.temp_dir.name, "tasks.yaml"), "w") as f:
            yaml.dump(tasks_config, f)
        
        # Create crews.yaml
        crews_config = {
            "test_crew": {
                "agents": ["test_agent"],
                "tasks": ["test_task"],
                "process": "sequential",
                "verbose": True,
                "project_name": "Test Project",
                "project_code": "TP-2023",
                "project_methodology": "Agile",
                "project_phase": "Testing",
                "organization": "Test Org",
                "portfolio": "Test Portfolio"
            }
        }
        
        with open(os.path.join(self.temp_dir.name, "crews.yaml"), "w") as f:
            yaml.dump(crews_config, f)
    
    def test_load_configs(self):
        """Test that configurations are loaded correctly."""
        self.assertIn("test_agent", self.config_loader.agents_config)
        self.assertIn("test_task", self.config_loader.tasks_config)
        self.assertIn("test_crew", self.config_loader.crews_config)
    
    def test_get_agent(self):
        """Test that an agent can be retrieved correctly."""
        agent = self.config_loader.get_agent("test_agent")
        
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.role, "Test Agent")
        self.assertEqual(agent.goal, "Test the config loader")
        self.assertEqual(agent.pm_methodology, "Agile")
        self.assertEqual(agent.certifications, ["Test Cert"])
        self.assertEqual(agent.industry_expertise, ["Testing"])
        self.assertTrue(agent.verbose)
        self.assertTrue(agent.allow_delegation)
    
    def test_get_task(self):
        """Test that a task can be retrieved correctly."""
        # Create agent dictionary
        agent = self.config_loader.get_agent("test_agent")
        agents = {"test_agent": agent}
        
        # Get task
        task = self.config_loader.get_task("test_task", agents)
        
        self.assertIsInstance(task, Task)
        self.assertEqual(task.description, "Test task for unit testing")
        self.assertEqual(task.expected_output, "Test output")
        self.assertEqual(task.agent, agent)
        self.assertEqual(task.pm_phase, "Testing")
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.estimated_duration, 1.0)
        self.assertEqual(task.deliverables, ["Test Deliverable"])
        self.assertEqual(task.stakeholders, ["Test Stakeholder"])
    
    def test_get_crew(self):
        """Test that a crew can be retrieved correctly."""
        crew = self.config_loader.get_crew("test_crew")
        
        self.assertIsInstance(crew, Crew)
        self.assertEqual(len(crew.agents), 1)
        self.assertEqual(len(crew.tasks), 1)
        self.assertEqual(crew.process, Process.sequential)
        self.assertTrue(crew.verbose)
        self.assertEqual(crew.project_name, "Test Project")
        self.assertEqual(crew.project_code, "TP-2023")
        self.assertEqual(crew.project_methodology, "Agile")
        self.assertEqual(crew.project_phase, "Testing")
        self.assertEqual(crew.organization, "Test Org")
        self.assertEqual(crew.portfolio, "Test Portfolio")
    
    def test_get_nonexistent_agent(self):
        """Test that getting a nonexistent agent raises an error."""
        with self.assertRaises(ValueError):
            self.config_loader.get_agent("nonexistent_agent")
    
    def test_get_nonexistent_task(self):
        """Test that getting a nonexistent task raises an error."""
        with self.assertRaises(ValueError):
            self.config_loader.get_task("nonexistent_task")
    
    def test_get_nonexistent_crew(self):
        """Test that getting a nonexistent crew raises an error."""
        with self.assertRaises(ValueError):
            self.config_loader.get_crew("nonexistent_crew")


if __name__ == "__main__":
    unittest.main()
