import unittest
from datetime import datetime

from pmoai.tools.pm_specific import (
    GanttChartTool,
    ProjectCharterTool,
    ResourceAllocationTool,
    RiskRegisterTool,
    StakeholderCommunicationTool,
)
from pmoai.tools.pm_specific.risk_register_tool import Risk
from pmoai.tools.pm_specific.resource_allocation_tool import Resource, Task as ResourceTask, ResourceAllocation
from pmoai.tools.pm_specific.gantt_chart_tool import GanttTask, GanttMilestone
from pmoai.tools.pm_specific.stakeholder_communication_tool import Stakeholder, CommunicationPlan


class TestPMTools(unittest.TestCase):
    def test_project_charter_tool(self):
        """Test that the ProjectCharterTool generates a charter document."""
        tool = ProjectCharterTool()
        
        charter = tool._run(
            project_name="Test Project",
            project_purpose="To test the ProjectCharterTool",
            project_objectives="Verify that the tool works correctly",
            project_scope="Testing the tool functionality",
            project_stakeholders="Test Team",
            project_timeline="1 week",
            project_budget="$1000",
            project_risks="None identified",
            project_success_criteria="Tool generates a charter document"
        )
        
        self.assertIn("# PROJECT CHARTER", charter)
        self.assertIn("## Project Name\nTest Project", charter)
        self.assertIn("## Project Purpose\nTo test the ProjectCharterTool", charter)
    
    def test_risk_register_tool(self):
        """Test that the RiskRegisterTool generates a risk register."""
        tool = RiskRegisterTool()
        
        risks = [
            Risk(
                id="R-001",
                description="Test Risk",
                category="Technical",
                probability="Medium",
                impact="High",
                severity="High",
                mitigation_strategy="Test mitigation",
                contingency_plan="Test contingency",
                owner="Test Owner",
                status="Open"
            )
        ]
        
        risk_register = tool._run(
            project_name="Test Project",
            risks=risks
        )
        
        self.assertIn("# RISK REGISTER", risk_register)
        self.assertIn("## Project Name\nTest Project", risk_register)
        self.assertIn("| R-001 | Test Risk | Technical | Medium | High | High | Test mitigation | Test contingency | Test Owner | Open |", risk_register)
    
    def test_resource_allocation_tool(self):
        """Test that the ResourceAllocationTool generates a resource allocation plan."""
        tool = ResourceAllocationTool()
        
        resources = [
            Resource(
                id="R-001",
                name="Test Resource",
                role="Developer",
                skills=["Python", "JavaScript"],
                availability=80.0,
                cost_rate=100.0,
                location="Remote"
            )
        ]
        
        tasks = [
            ResourceTask(
                id="T-001",
                name="Test Task",
                description="A test task",
                duration=40.0,
                required_skills=["Python"],
                dependencies=[],
                priority="High"
            )
        ]
        
        allocations = [
            ResourceAllocation(
                task_id="T-001",
                resource_id="R-001",
                allocation_percentage=50.0,
                start_date="2023-01-01",
                end_date="2023-01-05"
            )
        ]
        
        allocation_plan = tool._run(
            project_name="Test Project",
            resources=resources,
            tasks=tasks,
            allocations=allocations
        )
        
        self.assertIn("# RESOURCE ALLOCATION PLAN", allocation_plan)
        self.assertIn("## Project Name\nTest Project", allocation_plan)
        self.assertIn("| R-001 | Test Resource | Developer | Python, JavaScript | 80.0% | $100.0/hr | Remote |", allocation_plan)
        self.assertIn("| T-001 | Test Task | A test task | 40.0 | Python | None | High |", allocation_plan)
        self.assertIn("| Test Task | Test Resource | 50.0% | 2023-01-01 | 2023-01-05 | 20.0 hours |", allocation_plan)
    
    def test_gantt_chart_tool(self):
        """Test that the GanttChartTool generates a Gantt chart."""
        tool = GanttChartTool()
        
        tasks = [
            GanttTask(
                id="T-001",
                name="Test Task",
                start_date="2023-01-01",
                end_date="2023-01-05",
                progress=50.0,
                dependencies=None,
                assignee="Test Assignee"
            )
        ]
        
        milestones = [
            GanttMilestone(
                id="M-001",
                name="Test Milestone",
                date="2023-01-05",
                description="A test milestone"
            )
        ]
        
        gantt_chart = tool._run(
            project_name="Test Project",
            tasks=tasks,
            milestones=milestones,
            start_date="2023-01-01",
            end_date="2023-01-10"
        )
        
        self.assertIn("# GANTT CHART", gantt_chart)
        self.assertIn("## Project Name\nTest Project", gantt_chart)
        self.assertIn("T-001: Test Task [Test Assignee] (2023-01-01 to 2023-01-05, 5 days, 50.0% complete)", gantt_chart)
        self.assertIn("M-001: Test Milestone (2023-01-05) - A test milestone", gantt_chart)
    
    def test_stakeholder_communication_tool(self):
        """Test that the StakeholderCommunicationTool generates a communication plan."""
        tool = StakeholderCommunicationTool()
        
        stakeholders = [
            Stakeholder(
                id="S-001",
                name="Test Stakeholder",
                role="Executive",
                organization="Test Org",
                influence="High",
                interest="High",
                communication_preference="Email",
                communication_frequency="Weekly",
                key_concerns=["Budget", "Timeline"],
                expectations=["On-time delivery", "Within budget"]
            )
        ]
        
        communication_plans = [
            CommunicationPlan(
                stakeholder_id="S-001",
                communication_type="Status Report",
                frequency="Weekly",
                method="Email",
                responsible="Project Manager",
                content="Project status and issues",
                purpose="Keep stakeholder informed"
            )
        ]
        
        communication_plan = tool._run(
            project_name="Test Project",
            stakeholders=stakeholders,
            communication_plans=communication_plans
        )
        
        self.assertIn("# STAKEHOLDER COMMUNICATION PLAN", communication_plan)
        self.assertIn("## Project Name\nTest Project", communication_plan)
        self.assertIn("| S-001 | Test Stakeholder | Executive | Test Org | High | High | Email | Weekly |", communication_plan)
        self.assertIn("| Test Stakeholder | Status Report | Weekly | Email | Project Manager | Project status and issues | Keep stakeholder informed |", communication_plan)


if __name__ == "__main__":
    unittest.main()
